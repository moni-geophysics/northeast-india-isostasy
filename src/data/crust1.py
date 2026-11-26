"""
CRUST1.0 loading, fill-value masking, spatial subsetting, and summary generation.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.errors import NotGeoreferencedWarning
import xarray as xr

# CRUST1.0 uses 9.96921e+36 as NetCDF fill value for absent layers (e.g., missing sediments)
CRUST1_FILL_THRESHOLD = 1.0e20

CRUST1_LAYERS = [
    "water",
    "ice",
    "upper_sediments",
    "middle_sediments",
    "lower_sediments",
    "upper_crust",
    "middle_crust",
    "lower_crust",
]

SEDIMENT_LAYERS = ["upper_sediments", "middle_sediments", "lower_sediments"]
CRYSTALLINE_LAYERS = ["upper_crust", "middle_crust", "lower_crust"]


def mask_crust1_fill_values(ds: xr.Dataset, threshold: float = CRUST1_FILL_THRESHOLD) -> xr.Dataset:
    """
    Replace CRUST1.0 NetCDF fill values (~9.96921e+36) with NaN at the
    individual variable/layer level before any arithmetic is performed.
    """
    masked = ds.copy()
    for var in masked.data_vars:
        arr = masked[var]
        masked[var] = arr.where(np.isfinite(arr) & (np.abs(arr) < threshold))
    return masked


def load_crust1_raw_merged(raw_seismic_dir: str | Path) -> xr.Dataset:
    """
    Load and merge the three official CRUST1.0 NetCDF-4 Classic files (vp, vs, rho)
    via rasterio/GDAL subdatasets and mask fill values at the individual layer level.
    """
    raw_dir = Path(raw_seismic_dir)
    files = [
        raw_dir / "CRUST1.0-vp.r0.1-n4c.nc",
        raw_dir / "CRUST1.0-vs.r0.1-n4c.nc",
        raw_dir / "CRUST1.0-rho.r0.1-n4c.nc",
    ]
    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"Missing CRUST1.0 raw file: {f}")

    lats = 89.5 - np.arange(180, dtype=np.float64)
    lons = -179.5 + np.arange(360, dtype=np.float64)
    data_vars: dict[str, tuple[tuple[str, str], np.ndarray]] = {}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", NotGeoreferencedWarning)
        for f in files:
            with rasterio.open(f) as container:
                subdatasets = container.subdatasets
            for sds in subdatasets:
                var_name = sds.split(":")[-1]
                if var_name in data_vars:
                    continue
                with rasterio.open(sds) as src:
                    arr = src.read(1).astype(np.float64)
                data_vars[var_name] = (("latitude", "longitude"), arr)

    merged = xr.Dataset(
        data_vars=data_vars,
        coords={"latitude": lats, "longitude": lons},
    )
    return mask_crust1_fill_values(merged)


def subset_crust1_study_area(
    ds: xr.Dataset,
    lat_min: float = 22.0,
    lat_max: float = 27.0,
    lon_min: float = 90.0,
    lon_max: float = 95.0,
) -> xr.Dataset:
    """Extract CRUST1.0 cell centres within the study window."""
    lats = ds["latitude"].values
    lons = ds["longitude"].values
    lat_slice = slice(lat_min, lat_max) if lats[0] < lats[-1] else slice(lat_max, lat_min)
    lon_slice = slice(lon_min, lon_max) if lons[0] < lons[-1] else slice(lon_max, lon_min)
    return ds.sel(latitude=lat_slice, longitude=lon_slice).copy(deep=True)


def _get_solid_surface_elevation_km(cell: xr.Dataset) -> float:
    """
    Determine solid-Earth surface elevation (km relative to MSL) from the top
    of the shallowest present non-water, non-ice layer.
    """
    for layer in SEDIMENT_LAYERS + CRYSTALLINE_LAYERS:
        thk = float(cell[f"{layer}_thickness"].values)
        top = float(cell[f"{layer}_top"].values)
        if np.isfinite(thk) and thk > 0.0 and np.isfinite(top):
            return top
    # Fallback to upper_crust_top if finite
    uc_top = float(cell["upper_crust_top"].values)
    return uc_top if np.isfinite(uc_top) else np.nan


def build_crust1_summary(ds_sub: xr.Dataset) -> pd.DataFrame:
    """
    Build the cell-by-cell CRUST1.0 summary DataFrame with proper fill-value
    masking at the individual layer level.
    """
    ds_masked = mask_crust1_fill_values(ds_sub)
    rows = []
    for lat in ds_masked["latitude"].values:
        for lon in ds_masked["longitude"].values:
            cell = ds_masked.sel(latitude=lat, longitude=lon)

            surf_elev_km = _get_solid_surface_elevation_km(cell)
            water_thk_km = float(np.nan_to_num(cell["water_thickness"].values, nan=0.0))

            sed_thk_km = sum(
                float(np.nan_to_num(cell[f"{lyr}_thickness"].values, nan=0.0))
                for lyr in SEDIMENT_LAYERS
            )
            cryst_thk_km = sum(
                float(np.nan_to_num(cell[f"{lyr}_thickness"].values, nan=0.0))
                for lyr in CRYSTALLINE_LAYERS
            )
            total_crust_thk_km = sed_thk_km + cryst_thk_km

            moho_elev_km = float(cell["mantle_top"].values)
            moho_depth_sl_km = -moho_elev_km if np.isfinite(moho_elev_km) else np.nan

            rows.append(
                {
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "surface_elevation_km": round(surf_elev_km, 4) if np.isfinite(surf_elev_km) else np.nan,
                    "surface_elevation_m": round(surf_elev_km * 1000.0, 2) if np.isfinite(surf_elev_km) else np.nan,
                    "water_thickness_km": round(water_thk_km, 4),
                    "total_sediment_thickness_km": round(sed_thk_km, 4),
                    "crystalline_crust_thickness_km": round(cryst_thk_km, 4),
                    "total_crustal_thickness_km": round(total_crust_thk_km, 4),
                    "moho_elevation_km": round(moho_elev_km, 4) if np.isfinite(moho_elev_km) else np.nan,
                    "moho_depth_below_sl_km": round(moho_depth_sl_km, 4) if np.isfinite(moho_depth_sl_km) else np.nan,
                    "upper_crust_vp_kms": round(float(cell["upper_crust_vp"].values), 4),
                    "middle_crust_vp_kms": round(float(cell["middle_crust_vp"].values), 4),
                    "lower_crust_vp_kms": round(float(cell["lower_crust_vp"].values), 4),
                    "upper_crust_rho_gcm3": round(float(cell["upper_crust_rho"].values), 4),
                    "middle_crust_rho_gcm3": round(float(cell["middle_crust_rho"].values), 4),
                    "lower_crust_rho_gcm3": round(float(cell["lower_crust_rho"].values), 4),
                    "mantle_vpn_kms": round(float(cell["mantle_vpn"].values), 4),
                    "mantle_vsn_kms": round(float(cell["mantle_vsn"].values), 4),
                    "mantle_rho_gcm3": round(float(cell["mantle_rho"].values), 4),
                    "mantle_rho_kgm3": round(float(cell["mantle_rho"].values) * 1000.0, 2),
                }
            )
    return pd.DataFrame(rows)
