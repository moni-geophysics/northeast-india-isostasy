"""
3D spherical tesseroid forward gravity modeling for Airy and Pratt isostatic
compensation using Harmonica, consistent with WGM2012 Complete Spherical
Bouguer conventions (rho_bouguer = 2670.0 kg/m^3).

Conventions:
- Coordinates: geocentric spherical (longitude deg, latitude deg, radius m),
  with mean Earth radius R = 6,371,000 m.
- Output field: g_z (downward vertical component of gravitational acceleration
  in mGal; positive downward, negative upward).
- Bouguer-consistent Airy formulation:
  - Land (h > 0): root [R-(T0+b), R-T0] at (rho_c - rho_m)
                  + stripping mismatch [R, R+h] at (rho_c - rho_bouguer)
  - Marine (h < 0): anti-root [R-T0, R-(T0+b)] at (rho_m - rho_c)
                    + water-replacement mismatch [R+h, R] at (rho_bouguer - rho_c)
- Bouguer-consistent Pratt formulation:
  - Land (h > 0): sub-geoid [R-D, R] at (rho_pratt - rho_0)
                  + stripping mismatch [R, R+h] at (rho_pratt - rho_bouguer)
  - Marine (h < 0): sub-seafloor [R-D, R+h] at (rho_pratt - rho_0)
                    + water-replacement [R+h, R] at (rho_bouguer - rho_0)
"""

from __future__ import annotations

import harmonica as hm
import numpy as np

from src.isostasy.airy import compute_airy_isostasy
from src.isostasy.pratt import compute_pratt_isostasy

EARTH_MEAN_RADIUS_M = 6_371_000.0
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
WGM2012_BOUGUER_DENSITY = 2670.0      # kg/m^3


def _grid_cell_edges_1d(centers: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute west/south and east/north cell edges from 1D ascending centers."""
    if len(centers) < 2:
        raise ValueError("Need at least 2 grid centers to infer cell spacing.")
    diffs = np.diff(centers)
    half_left = np.empty_like(centers, dtype=np.float64)
    half_right = np.empty_like(centers, dtype=np.float64)
    half_left[1:] = 0.5 * diffs
    half_left[0] = 0.5 * diffs[0]
    half_right[:-1] = 0.5 * diffs
    half_right[-1] = 0.5 * diffs[-1]
    return centers - half_left, centers + half_right


def _stack_masked_tesseroids(
    w2d: np.ndarray,
    e2d: np.ndarray,
    s2d: np.ndarray,
    n2d: np.ndarray,
    r_bot: np.ndarray | float,
    r_top: np.ndarray | float,
    delta_rho: np.ndarray | float,
    mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Build tesseroid and density arrays for cells selected by mask."""
    count = int(np.sum(mask))
    if count == 0:
        return np.empty((0, 6), dtype=np.float64), np.empty((0,), dtype=np.float64)
    bot_arr = r_bot[mask] if np.ndim(r_bot) > 0 else np.full(count, float(r_bot), dtype=np.float64)
    top_arr = r_top[mask] if np.ndim(r_top) > 0 else np.full(count, float(r_top), dtype=np.float64)
    rho_arr = delta_rho[mask] if np.ndim(delta_rho) > 0 else np.full(count, float(delta_rho), dtype=np.float64)
    tess = np.column_stack([w2d[mask], e2d[mask], s2d[mask], n2d[mask], bot_arr, top_arr])
    return tess, rho_arr.astype(np.float64)


def build_airy_tesseroids(
    lon_1d: np.ndarray,
    lat_1d: np.ndarray,
    elevation_m: np.ndarray,
    t0_km: float = 35.0,
    rho_c: float = 2750.0,
    rho_m: float = 3350.0,
    rho_w: float = 1030.0,
    rho_bouguer: float = WGM2012_BOUGUER_DENSITY,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Construct Bouguer-consistent 3D tesseroids [w, e, s, n, bottom_m, top_m]
    and density contrasts (kg/m^3) for Airy roots/anti-roots plus the
    topographic/water-fill stripping mismatch relative to rho_bouguer.
    """
    elev = np.asarray(elevation_m, dtype=np.float64)
    airy = compute_airy_isostasy(
        elev, t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w
    )
    b_m = airy["root_thickness_km"] * 1000.0

    lon_w, lon_e = _grid_cell_edges_1d(np.asarray(lon_1d, dtype=np.float64))
    lat_s, lat_n = _grid_cell_edges_1d(np.asarray(lat_1d, dtype=np.float64))
    w2d, s2d = np.meshgrid(lon_w, lat_s)
    e2d, n2d = np.meshgrid(lon_e, lat_n)

    r_t0 = earth_radius_m - t0_km * 1000.0
    r_moho = r_t0 - b_m

    tess_parts = []
    dens_parts = []

    # 1. Subsurface Airy root (b > 0) and marine anti-root (b < 0)
    valid_b = np.isfinite(b_m)
    t_root, d_root = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d, r_moho, r_t0, rho_c - rho_m, valid_b & (b_m > 1e-6)
    )
    t_anti, d_anti = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d, r_t0, r_moho, rho_m - rho_c, valid_b & (b_m < -1e-6)
    )
    for t_part, d_part in [(t_root, d_root), (t_anti, d_anti)]:
        if len(t_part) > 0:
            tess_parts.append(t_part)
            dens_parts.append(d_part)

    # 2. Bouguer stripping-mismatch layer between z = 0 and z = h
    if abs(rho_c - rho_bouguer) > 1e-9:
        valid_h = np.isfinite(elev)
        t_land_s, d_land_s = _stack_masked_tesseroids(
            w2d, e2d, s2d, n2d,
            earth_radius_m, earth_radius_m + elev,
            rho_c - rho_bouguer,
            valid_h & (elev > 1e-6),
        )
        t_mar_s, d_mar_s = _stack_masked_tesseroids(
            w2d, e2d, s2d, n2d,
            earth_radius_m + elev, earth_radius_m,
            rho_bouguer - rho_c,
            valid_h & (elev < -1e-6),
        )
        for t_part, d_part in [(t_land_s, d_land_s), (t_mar_s, d_mar_s)]:
            if len(t_part) > 0:
                tess_parts.append(t_part)
                dens_parts.append(d_part)

    if not tess_parts:
        return np.empty((0, 6), dtype=np.float64), np.empty((0,), dtype=np.float64)

    return np.vstack(tess_parts), np.concatenate(dens_parts)


def build_pratt_tesseroids(
    lon_1d: np.ndarray,
    lat_1d: np.ndarray,
    elevation_m: np.ndarray,
    d_km: float = 100.0,
    rho_0: float = 3100.0,
    rho_w: float = 1030.0,
    rho_bouguer: float = WGM2012_BOUGUER_DENSITY,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Construct Bouguer-consistent 3D tesseroids [w, e, s, n, bottom_m, top_m]
    and density contrasts (kg/m^3) for Pratt-Hayford compensation:
      - Land (h > 0):
          1. Sub-geoid [R-D, R] with contrast (rho_pratt - rho_0)
          2. Topographic stripping-mismatch [R, R+h] with contrast (rho_pratt - rho_bouguer)
      - Marine (h < 0):
          1. Sub-seafloor [R-D, R+h] with contrast (rho_pratt - rho_0)
          2. Water-replacement [R+h, R] with contrast (rho_bouguer - rho_0)
    """
    elev = np.asarray(elevation_m, dtype=np.float64)
    pratt = compute_pratt_isostasy(elev, d_km=d_km, rho_0=rho_0, rho_w=rho_w)
    rho_pratt = pratt["pratt_density_kgm3"]
    delta_rho_sub = pratt["density_anomaly_kgm3"]

    lon_w, lon_e = _grid_cell_edges_1d(np.asarray(lon_1d, dtype=np.float64))
    lat_s, lat_n = _grid_cell_edges_1d(np.asarray(lat_1d, dtype=np.float64))
    w2d, s2d = np.meshgrid(lon_w, lat_s)
    e2d, n2d = np.meshgrid(lon_e, lat_n)

    r_bottom = earth_radius_m - d_km * 1000.0
    valid = np.isfinite(elev) & np.isfinite(delta_rho_sub)
    land_mask = valid & (elev > 1e-6)
    marine_mask = valid & (elev < -1e-6) & ((earth_radius_m + elev) > r_bottom)

    tess_parts = []
    dens_parts = []

    # Land Layer 1: sub-geoid [R-D, R] at (rho_pratt - rho_0)
    t_l1, d_l1 = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d, r_bottom, earth_radius_m, delta_rho_sub, land_mask
    )
    # Land Layer 2: stripping mismatch [R, R+h] at (rho_pratt - rho_bouguer)
    t_l2, d_l2 = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d,
        earth_radius_m, earth_radius_m + elev,
        rho_pratt - rho_bouguer,
        land_mask & (np.abs(rho_pratt - rho_bouguer) > 1e-9),
    )
    # Marine Layer 1: sub-seafloor [R-D, R+h] at (rho_pratt - rho_0)
    t_m1, d_m1 = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d, r_bottom, earth_radius_m + elev, delta_rho_sub, marine_mask
    )
    # Marine Layer 2: water-replacement [R+h, R] at (rho_bouguer - rho_0)
    t_m2, d_m2 = _stack_masked_tesseroids(
        w2d, e2d, s2d, n2d,
        earth_radius_m + elev, earth_radius_m,
        rho_bouguer - rho_0,
        marine_mask & (abs(rho_bouguer - rho_0) > 1e-9),
    )

    for t_part, d_part in [(t_l1, d_l1), (t_l2, d_l2), (t_m1, d_m1), (t_m2, d_m2)]:
        if len(t_part) > 0:
            tess_parts.append(t_part)
            dens_parts.append(d_part)

    if not tess_parts:
        return np.empty((0, 6), dtype=np.float64), np.empty((0,), dtype=np.float64)

    return np.vstack(tess_parts), np.concatenate(dens_parts)


def compute_tesseroid_gravity(
    obs_lon: np.ndarray,
    obs_lat: np.ndarray,
    obs_elev_m: np.ndarray,
    tesseroids: np.ndarray,
    density: np.ndarray,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
    radial_adaptive_discretization: bool = False,
) -> np.ndarray:
    """
    Compute vertical gravity (g_z in mGal, positive downward) at observation
    points (obs_lon, obs_lat, earth_radius_m + obs_elev_m) using Harmonica.

    Note: radial_adaptive_discretization defaults to False because Harmonica raises
    ZeroDivisionError when observation points lie directly on a tesseroid top face
    (e.g., shallow [R, R+h] layers at r_obs = R+h). Convergence tests confirm
    2-arc-min non-adaptive tesseroids match 8x8x4 refined meshes within ~0.2%.
    """
    obs_lon_flat = np.asarray(obs_lon, dtype=np.float64).ravel()
    obs_lat_flat = np.asarray(obs_lat, dtype=np.float64).ravel()
    obs_r_flat = earth_radius_m + np.asarray(obs_elev_m, dtype=np.float64).ravel()

    if len(tesseroids) == 0:
        return np.zeros(np.asarray(obs_lon).shape, dtype=np.float64)

    g_z = hm.tesseroid_gravity(
        (obs_lon_flat, obs_lat_flat, obs_r_flat),
        tesseroids,
        density,
        field="g_z",
        parallel=True,
        radial_adaptive_discretization=radial_adaptive_discretization,
    )
    return np.asarray(g_z, dtype=np.float64).reshape(np.asarray(obs_lon).shape)
