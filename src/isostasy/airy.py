"""
Classical Airy-Heiskanen Local Isostasy (Land and Marine Formulations).

All equations are derived from equal mass per unit area at a common
compensation depth z = -Z_comp below Mean Sea Level (z = 0, positive upward).
"""

from __future__ import annotations

import numpy as np
import xarray as xr


def _validate_airy_params(t0_km: float, rho_c: float, rho_m: float, rho_w: float) -> None:
    if t0_km <= 0.0:
        raise ValueError(f"Reference crustal thickness t0_km must be > 0, got {t0_km}")
    if not (0.0 < rho_w < rho_c < rho_m):
        raise ValueError(
            f"Require 0 < rho_w < rho_c < rho_m; got rho_w={rho_w}, rho_c={rho_c}, rho_m={rho_m}"
        )


def airy_root_land(
    elevation_m: np.ndarray | float,
    rho_c: float = 2750.0,
    rho_m: float = 3350.0,
) -> np.ndarray | float:
    """
    Additional Airy crustal root b (km) below reference depth T0 for subaerial
    topography (h >= 0):
        b = [rho_c / (rho_m - rho_c)] * h_km
    Preserves NaNs; raises ValueError if any finite input is < 0.
    """
    if rho_c <= 0.0 or rho_m <= rho_c:
        raise ValueError(f"Require 0 < rho_c < rho_m; got rho_c={rho_c}, rho_m={rho_m}")
    h_km = np.asarray(elevation_m, dtype=np.float64) / 1000.0
    finite = np.isfinite(h_km)
    if np.any(h_km[finite] < 0.0):
        raise ValueError("airy_root_land received negative elevation (marine cell). Use airy_root_marine.")
    b_km = (rho_c / (rho_m - rho_c)) * h_km
    return float(b_km) if np.ndim(elevation_m) == 0 else b_km


def airy_root_marine(
    elevation_m: np.ndarray | float,
    rho_c: float = 2750.0,
    rho_m: float = 3350.0,
    rho_w: float = 1030.0,
) -> np.ndarray | float:
    """
    Airy crustal anti-root b (km, negative) relative to reference depth T0 for
    marine bathymetry (h < 0, water depth d_w = -h > 0):
        b = [(rho_c - rho_w) / (rho_m - rho_c)] * h_km
    Preserves NaNs; raises ValueError if any finite input is > 0.
    """
    if not (0.0 < rho_w < rho_c < rho_m):
        raise ValueError(
            f"Require 0 < rho_w < rho_c < rho_m; got rho_w={rho_w}, rho_c={rho_c}, rho_m={rho_m}"
        )
    h_km = np.asarray(elevation_m, dtype=np.float64) / 1000.0
    finite = np.isfinite(h_km)
    if np.any(h_km[finite] > 0.0):
        raise ValueError("airy_root_marine received positive elevation (land cell). Use airy_root_land.")
    b_km = ((rho_c - rho_w) / (rho_m - rho_c)) * h_km
    return float(b_km) if np.ndim(elevation_m) == 0 else b_km


def compute_airy_isostasy(
    elevation_m: xr.DataArray | np.ndarray | float,
    t0_km: float = 35.0,
    rho_c: float = 2750.0,
    rho_m: float = 3350.0,
    rho_w: float = 1030.0,
) -> xr.Dataset | dict[str, np.ndarray | float]:
    """
    Compute complete Airy-Heiskanen isostatic quantities for mixed land/marine grids.

    Separates:
      - root_thickness_km (b): root (>0) or anti-root (<0) relative to T0 below sea level
      - moho_depth_sl_km (D_Moho,SL = T0 + b): Moho depth below sea level (positive down)
      - moho_elevation_km (z_Moho = -(T0 + b)): Moho elevation relative to sea level (negative down)
      - total_crustal_thickness_km (T_c = h_km + T0 + b): solid crust thickness (surface/seafloor to Moho)
      - is_marine: True where elevation_m < 0 (NaN preserved as False in mask, NaN in outputs)

    Preserves xarray coordinates and attributes if elevation_m is an xr.DataArray.
    """
    _validate_airy_params(t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w)

    is_da = isinstance(elevation_m, xr.DataArray)
    raw_vals = elevation_m.values if is_da else elevation_m
    h_arr = np.asarray(raw_vals, dtype=np.float64)
    h_km = h_arr / 1000.0

    valid = np.isfinite(h_km)
    land_mask = valid & (h_km >= 0.0)
    marine_mask = valid & (h_km < 0.0)

    b_km = np.full_like(h_km, np.nan, dtype=np.float64)
    if np.any(land_mask):
        b_km[land_mask] = airy_root_land(h_arr[land_mask], rho_c=rho_c, rho_m=rho_m)
    if np.any(marine_mask):
        b_km[marine_mask] = airy_root_marine(h_arr[marine_mask], rho_c=rho_c, rho_m=rho_m, rho_w=rho_w)

    moho_depth_sl_km = np.where(valid, t0_km + b_km, np.nan)
    moho_elevation_km = np.where(valid, -moho_depth_sl_km, np.nan)
    total_crustal_thickness_km = np.where(valid, h_km + moho_depth_sl_km, np.nan)

    if np.ndim(h_arr) == 0 and not is_da:
        return {
            "elevation_km": float(h_km),
            "root_thickness_km": float(b_km),
            "moho_depth_sl_km": float(moho_depth_sl_km),
            "moho_elevation_km": float(moho_elevation_km),
            "total_crustal_thickness_km": float(total_crustal_thickness_km),
            "is_marine": bool(marine_mask),
        }

    if is_da:
        coords = elevation_m.coords
        dims = elevation_m.dims
        ds = xr.Dataset(
            {
                "elevation_km": (dims, h_km, {"units": "km", "long_name": "Surface/seafloor elevation relative to MSL"}),
                "root_thickness_km": (dims, b_km, {"units": "km", "long_name": "Airy root (>0) or anti-root (<0) relative to T0"}),
                "moho_depth_sl_km": (dims, moho_depth_sl_km, {"units": "km", "long_name": "Moho depth below sea level (positive down)"}),
                "moho_elevation_km": (dims, moho_elevation_km, {"units": "km", "long_name": "Moho elevation relative to sea level (negative down)"}),
                "total_crustal_thickness_km": (dims, total_crustal_thickness_km, {"units": "km", "long_name": "Solid crustal thickness from surface/seafloor to Moho"}),
                "is_marine": (dims, marine_mask, {"long_name": "Marine cell indicator (elevation < 0)"}),
            },
            coords=coords,
            attrs={
                "model": "Airy-Heiskanen Local Isostasy",
                "t0_km": t0_km,
                "rho_c_kgm3": rho_c,
                "rho_m_kgm3": rho_m,
                "rho_w_kgm3": rho_w,
            },
        )
        return ds

    return {
        "elevation_km": h_km,
        "root_thickness_km": b_km,
        "moho_depth_sl_km": moho_depth_sl_km,
        "moho_elevation_km": moho_elevation_km,
        "total_crustal_thickness_km": total_crustal_thickness_km,
        "is_marine": marine_mask,
    }
