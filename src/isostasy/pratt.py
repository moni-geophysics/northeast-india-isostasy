"""
Classical Pratt-Hayford Local Isostasy (Land and Marine Formulations).

All equations are derived from equal mass per unit area above a common
compensation depth z = -D below Mean Sea Level (z = 0, positive upward).
"""

from __future__ import annotations

import numpy as np
import xarray as xr


def _validate_pratt_params(d_km: float, rho_0: float, rho_w: float) -> None:
    if d_km <= 0.0:
        raise ValueError(f"Compensation depth d_km must be > 0, got {d_km}")
    if not (0.0 < rho_w < rho_0):
        raise ValueError(f"Require 0 < rho_w < rho_0; got rho_w={rho_w}, rho_0={rho_0}")


def pratt_density_land(
    elevation_m: np.ndarray | float,
    d_km: float = 100.0,
    rho_0: float = 3100.0,
) -> np.ndarray | float:
    """
    Pratt column density (kg/m^3) for subaerial topography (h >= 0):
        rho(h) = rho_0 * D / (D + h_km)
    Preserves NaNs; raises ValueError if any finite input is < 0.
    """
    if d_km <= 0.0 or rho_0 <= 0.0:
        raise ValueError(f"Require d_km > 0 and rho_0 > 0; got d_km={d_km}, rho_0={rho_0}")
    h_km = np.asarray(elevation_m, dtype=np.float64) / 1000.0
    finite = np.isfinite(h_km)
    if np.any(h_km[finite] < 0.0):
        raise ValueError("pratt_density_land received negative elevation (marine cell). Use pratt_density_marine.")
    rho = rho_0 * (d_km / (d_km + h_km))
    return float(rho) if np.ndim(elevation_m) == 0 else rho


def pratt_density_marine(
    elevation_m: np.ndarray | float,
    d_km: float = 100.0,
    rho_0: float = 3100.0,
    rho_w: float = 1030.0,
) -> np.ndarray | float:
    """
    Pratt sub-seafloor rock column density (kg/m^3) for marine bathymetry
    (h < 0, water depth d_w = -h_km > 0, requiring d_w < D):
        rho(h) = (rho_0 * D + rho_w * h_km) / (D + h_km)
               = (rho_0 * D - rho_w * d_w) / (D - d_w)
    Preserves NaNs; raises ValueError if any finite input is > 0 or d_w >= D.
    """
    _validate_pratt_params(d_km=d_km, rho_0=rho_0, rho_w=rho_w)
    h_km = np.asarray(elevation_m, dtype=np.float64) / 1000.0
    finite = np.isfinite(h_km)
    if np.any(h_km[finite] > 0.0):
        raise ValueError("pratt_density_marine received positive elevation (land cell). Use pratt_density_land.")
    if np.any((d_km + h_km[finite]) <= 0.0):
        raise ValueError("Water depth (-h_km) must be strictly less than compensation depth d_km.")
    rho = (rho_0 * d_km + rho_w * h_km) / (d_km + h_km)
    return float(rho) if np.ndim(elevation_m) == 0 else rho


def compute_pratt_isostasy(
    elevation_m: xr.DataArray | np.ndarray | float,
    d_km: float = 100.0,
    rho_0: float = 3100.0,
    rho_w: float = 1030.0,
) -> xr.Dataset | dict[str, np.ndarray | float]:
    """
    Compute Pratt-Hayford lateral density distribution and density anomaly
    relative to reference column density rho_0 for mixed land/marine grids.

    Preserves xarray coordinates and attributes if elevation_m is an xr.DataArray.
    """
    _validate_pratt_params(d_km=d_km, rho_0=rho_0, rho_w=rho_w)

    is_da = isinstance(elevation_m, xr.DataArray)
    raw_vals = elevation_m.values if is_da else elevation_m
    h_arr = np.asarray(raw_vals, dtype=np.float64)
    h_km = h_arr / 1000.0

    valid = np.isfinite(h_km)
    land_mask = valid & (h_km >= 0.0)
    marine_mask = valid & (h_km < 0.0)

    rho_pratt = np.full_like(h_km, np.nan, dtype=np.float64)
    if np.any(land_mask):
        rho_pratt[land_mask] = pratt_density_land(h_arr[land_mask], d_km=d_km, rho_0=rho_0)
    if np.any(marine_mask):
        rho_pratt[marine_mask] = pratt_density_marine(h_arr[marine_mask], d_km=d_km, rho_0=rho_0, rho_w=rho_w)

    delta_rho = np.where(valid, rho_pratt - rho_0, np.nan)

    if np.ndim(h_arr) == 0 and not is_da:
        return {
            "elevation_km": float(h_km),
            "pratt_density_kgm3": float(rho_pratt),
            "density_anomaly_kgm3": float(delta_rho),
            "is_marine": bool(marine_mask),
        }

    if is_da:
        coords = elevation_m.coords
        dims = elevation_m.dims
        ds = xr.Dataset(
            {
                "elevation_km": (dims, h_km, {"units": "km", "long_name": "Surface/seafloor elevation relative to MSL"}),
                "pratt_density_kgm3": (dims, rho_pratt, {"units": "kg/m^3", "long_name": "Pratt compensated rock column density"}),
                "density_anomaly_kgm3": (dims, delta_rho, {"units": "kg/m^3", "long_name": "Pratt density anomaly relative to rho_0"}),
                "is_marine": (dims, marine_mask, {"long_name": "Marine cell indicator (elevation < 0)"}),
            },
            coords=coords,
            attrs={
                "model": "Pratt-Hayford Local Isostasy",
                "d_km": d_km,
                "rho_0_kgm3": rho_0,
                "rho_w_kgm3": rho_w,
            },
        )
        return ds

    return {
        "elevation_km": h_km,
        "pratt_density_kgm3": rho_pratt,
        "density_anomaly_kgm3": delta_rho,
        "is_marine": marine_mask,
    }
