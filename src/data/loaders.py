"""
Data loading, spatial subsetting, and statistical inspection utilities
for WGM2012 gravity/topography grids and Earth2014 topography.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import xarray as xr

# Study area and buffered modeling domain bounds (WGS84 / EPSG:4326)
CORE_BOUNDS: dict[str, float] = {
    "lat_min": 22.0,
    "lat_max": 27.0,
    "lon_min": 90.0,
    "lon_max": 95.0,
}

BUFFER_BOUNDS: dict[str, float] = {
    "lat_min": 19.0,
    "lat_max": 30.0,
    "lon_min": 87.0,
    "lon_max": 98.0,
}


def get_coord_names(ds_or_da: xr.Dataset | xr.DataArray) -> tuple[str, str]:
    """Return (lon_name, lat_name) for a Dataset or DataArray."""
    coords = ds_or_da.coords
    lon_name = "x" if "x" in coords else ("longitude" if "longitude" in coords else "lon")
    lat_name = "y" if "y" in coords else ("latitude" if "latitude" in coords else "lat")
    if lon_name not in coords or lat_name not in coords:
        raise ValueError(f"Could not identify lon/lat coordinate names in {list(coords)}")
    return lon_name, lat_name


def load_grid(path: str | Path) -> xr.Dataset:
    """Load a GMT .grd or NetCDF grid without modifying raw data."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Grid file not found: {p}")
    return xr.open_dataset(p)


def subset_grid(
    ds: xr.Dataset,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    region_label: str = "subset",
) -> xr.Dataset:
    """
    Extract a spatial subset cleanly without resampling or interpolation,
    handling ascending or descending coordinate arrays.
    """
    lon_name, lat_name = get_coord_names(ds)
    lons = ds[lon_name].values
    lats = ds[lat_name].values

    lon_slice = slice(lon_min, lon_max) if lons[0] < lons[-1] else slice(lon_max, lon_min)
    lat_slice = slice(lat_min, lat_max) if lats[0] < lats[-1] else slice(lat_max, lat_min)

    sub = ds.sel({lat_name: lat_slice, lon_name: lon_slice}).copy(deep=True)
    sub.attrs = dict(ds.attrs)
    sub.attrs["subset_region"] = region_label
    sub.attrs["subset_bounds_deg"] = f"lat=[{lat_min}, {lat_max}], lon=[{lon_min}, {lon_max}]"
    return sub


def compute_grid_stats(da: xr.DataArray) -> dict[str, Any]:
    """
    Compute exact summary statistics, resolution, and marine/negative-cell counts
    on a 2D DataArray while masking non-finite values.
    """
    lon_name, lat_name = get_coord_names(da)
    lons = da[lon_name].values
    lats = da[lat_name].values
    vals = da.values.astype(np.float64)

    valid_mask = np.isfinite(vals)
    valid_vals = vals[valid_mask]

    dx = float(np.median(np.abs(np.diff(lons)))) if len(lons) > 1 else np.nan
    dy = float(np.median(np.abs(np.diff(lats)))) if len(lats) > 1 else np.nan

    return {
        "n_lat": int(len(lats)),
        "n_lon": int(len(lons)),
        "total_cells": int(vals.size),
        "valid_cells": int(valid_mask.sum()),
        "nan_cells": int((~valid_mask).sum()),
        "lat_min": float(np.min(lats)),
        "lat_max": float(np.max(lats)),
        "lon_min": float(np.min(lons)),
        "lon_max": float(np.max(lons)),
        "dx_deg": dx,
        "dy_deg": dy,
        "min": float(np.min(valid_vals)) if valid_vals.size > 0 else np.nan,
        "max": float(np.max(valid_vals)) if valid_vals.size > 0 else np.nan,
        "mean": float(np.mean(valid_vals)) if valid_vals.size > 0 else np.nan,
        "std": float(np.std(valid_vals)) if valid_vals.size > 0 else np.nan,
        "negative_count": int(np.sum(valid_vals < 0.0)),
        "zero_count": int(np.sum(valid_vals == 0.0)),
    }
