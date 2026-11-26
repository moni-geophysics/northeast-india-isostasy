"""
3D spherical tesseroid forward gravity modeling for Airy and Pratt isostatic
compensation using Harmonica.

Conventions:
- Coordinates: geocentric spherical (longitude deg, latitude deg, radius m),
  with mean Earth radius R = 6,371,000 m.
- Output field: g_z (downward vertical component of gravitational acceleration
  in mGal; positive downward, negative upward).
- Bouguer-consistent subsurface modeling:
  - Airy: root (b > 0, delta_rho = rho_c - rho_m < 0) below -T0, and marine
    anti-root (b < 0, delta_rho = rho_m - rho_c > 0) above -T0.
  - Pratt: sub-sea-level / sub-seafloor lateral density contrast
    delta_rho = rho_pratt - rho_0 over [-D, min(0, h)].
"""

from __future__ import annotations

import harmonica as hm
import numpy as np

from src.isostasy.airy import compute_airy_isostasy
from src.isostasy.pratt import compute_pratt_isostasy

EARTH_MEAN_RADIUS_M = 6_371_000.0
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2


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


def build_airy_tesseroids(
    lon_1d: np.ndarray,
    lat_1d: np.ndarray,
    elevation_m: np.ndarray,
    t0_km: float = 35.0,
    rho_c: float = 2750.0,
    rho_m: float = 3350.0,
    rho_w: float = 1030.0,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Construct 3D tesseroids [w, e, s, n, bottom_m, top_m] and density contrasts
    (kg/m^3) for Airy roots (b > 0) and marine anti-roots (b < 0) relative to T0.
    """
    airy = compute_airy_isostasy(
        elevation_m, t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w
    )
    b_m = airy["root_thickness_km"] * 1000.0

    lon_w, lon_e = _grid_cell_edges_1d(np.asarray(lon_1d, dtype=np.float64))
    lat_s, lat_n = _grid_cell_edges_1d(np.asarray(lat_1d, dtype=np.float64))
    w2d, s2d = np.meshgrid(lon_w, lat_s)
    e2d, n2d = np.meshgrid(lon_e, lat_n)

    r_t0 = earth_radius_m - t0_km * 1000.0
    r_moho = r_t0 - b_m

    valid = np.isfinite(b_m) & (np.abs(b_m) > 1e-6)
    root_mask = valid & (b_m > 0.0)
    anti_mask = valid & (b_m < 0.0)

    tesseroid_list = []
    density_list = []

    if np.any(root_mask):
        t_root = np.column_stack(
            [
                w2d[root_mask],
                e2d[root_mask],
                s2d[root_mask],
                n2d[root_mask],
                r_moho[root_mask],
                np.full(int(np.sum(root_mask)), r_t0),
            ]
        )
        tesseroid_list.append(t_root)
        density_list.append(np.full(int(np.sum(root_mask)), rho_c - rho_m, dtype=np.float64))

    if np.any(anti_mask):
        t_anti = np.column_stack(
            [
                w2d[anti_mask],
                e2d[anti_mask],
                s2d[anti_mask],
                n2d[anti_mask],
                np.full(int(np.sum(anti_mask)), r_t0),
                r_moho[anti_mask],
            ]
        )
        tesseroid_list.append(t_anti)
        density_list.append(np.full(int(np.sum(anti_mask)), rho_m - rho_c, dtype=np.float64))

    if not tesseroid_list:
        return np.empty((0, 6), dtype=np.float64), np.empty((0,), dtype=np.float64)

    return np.vstack(tesseroid_list), np.concatenate(density_list)


def build_pratt_tesseroids(
    lon_1d: np.ndarray,
    lat_1d: np.ndarray,
    elevation_m: np.ndarray,
    d_km: float = 100.0,
    rho_0: float = 3100.0,
    rho_w: float = 1030.0,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Construct 3D tesseroids [w, e, s, n, bottom_m, top_m] and density contrasts
    (kg/m^3) for Pratt subsurface compensating density anomalies relative to rho_0:
      - Land (h >= 0): column from -D to 0 m with delta_rho = rho_pratt - rho_0 < 0
      - Marine (h < 0): column from -D to h with delta_rho = rho_pratt - rho_0 > 0
    """
    elev = np.asarray(elevation_m, dtype=np.float64)
    pratt = compute_pratt_isostasy(elev, d_km=d_km, rho_0=rho_0, rho_w=rho_w)
    delta_rho = pratt["density_anomaly_kgm3"]

    lon_w, lon_e = _grid_cell_edges_1d(np.asarray(lon_1d, dtype=np.float64))
    lat_s, lat_n = _grid_cell_edges_1d(np.asarray(lat_1d, dtype=np.float64))
    w2d, s2d = np.meshgrid(lon_w, lat_s)
    e2d, n2d = np.meshgrid(lon_e, lat_n)

    r_bottom = earth_radius_m - d_km * 1000.0
    r_top = earth_radius_m + np.minimum(0.0, elev)

    valid = np.isfinite(delta_rho) & (np.abs(delta_rho) > 1e-9) & (r_top > r_bottom)
    if not np.any(valid):
        return np.empty((0, 6), dtype=np.float64), np.empty((0,), dtype=np.float64)

    tesseroids = np.column_stack(
        [
            w2d[valid],
            e2d[valid],
            s2d[valid],
            n2d[valid],
            np.full(int(np.sum(valid)), r_bottom),
            r_top[valid],
        ]
    )
    densities = delta_rho[valid].astype(np.float64)
    return tesseroids, densities


def compute_tesseroid_gravity(
    obs_lon: np.ndarray,
    obs_lat: np.ndarray,
    obs_elev_m: np.ndarray,
    tesseroids: np.ndarray,
    density: np.ndarray,
    earth_radius_m: float = EARTH_MEAN_RADIUS_M,
) -> np.ndarray:
    """
    Compute vertical gravity (g_z in mGal, positive downward) at observation
    points (obs_lon, obs_lat, earth_radius_m + obs_elev_m) using Harmonica.
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
        radial_adaptive_discretization=False,
    )
    return np.asarray(g_z, dtype=np.float64).reshape(np.asarray(obs_lon).shape)
