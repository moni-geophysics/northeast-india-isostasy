"""
Unit and validation tests for Phase 1 data loading, spatial subsetting,
fill-value masking, and CRUST1.0 summary generation.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from src.data.crust1 import load_crust1_raw_merged
from src.data.loaders import BUFFER_BOUNDS, CORE_BOUNDS, compute_grid_stats

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_processed_gravity_subsets_exist_and_valid():
    prefixes = [
        "WGM2012_Bouguer",
        "WGM2012_ETOPO1",
        "WGM2012_Freeair",
        "WGM2012_Isostatic",
    ]
    for prefix in prefixes:
        buf_path = PROJECT_ROOT / f"data/processed/gravity/{prefix}_buffer_19_30N_87_98E.nc"
        core_path = PROJECT_ROOT / f"data/processed/gravity/{prefix}_core_22_27N_90_95E.nc"
        assert buf_path.exists(), f"Missing {buf_path}"
        assert core_path.exists(), f"Missing {core_path}"

        with xr.open_dataset(buf_path) as ds_buf:
            stats_buf = compute_grid_stats(ds_buf["z"])
            assert stats_buf["n_lat"] == 331
            assert stats_buf["n_lon"] == 331
            assert stats_buf["nan_cells"] == 0
            assert stats_buf["lat_min"] == pytest.approx(BUFFER_BOUNDS["lat_min"], abs=1e-4)
            assert stats_buf["lat_max"] == pytest.approx(BUFFER_BOUNDS["lat_max"], abs=1e-4)
            assert stats_buf["lon_min"] == pytest.approx(BUFFER_BOUNDS["lon_min"], abs=1e-4)
            assert stats_buf["lon_max"] == pytest.approx(BUFFER_BOUNDS["lon_max"], abs=1e-4)

        with xr.open_dataset(core_path) as ds_core:
            stats_core = compute_grid_stats(ds_core["z"])
            assert stats_core["n_lat"] == 151
            assert stats_core["n_lon"] == 151
            assert stats_core["nan_cells"] == 0
            assert stats_core["lat_min"] == pytest.approx(CORE_BOUNDS["lat_min"], abs=1e-4)
            assert stats_core["lat_max"] == pytest.approx(CORE_BOUNDS["lat_max"], abs=1e-4)


def test_processed_earth2014_subsets_and_marine_cells():
    buf_path = PROJECT_ROOT / "data/processed/topography/Earth2014_TBI2014_buffer_19_30N_87_98E.nc"
    core_path = PROJECT_ROOT / "data/processed/topography/Earth2014_TBI2014_core_22_27N_90_95E.nc"
    assert buf_path.exists()
    assert core_path.exists()

    with xr.open_dataset(buf_path) as ds_buf:
        stats_buf = compute_grid_stats(ds_buf["z"])
        assert stats_buf["n_lat"] == 660
        assert stats_buf["n_lon"] == 660
        assert stats_buf["nan_cells"] == 0
        assert stats_buf["negative_count"] == 60341

    with xr.open_dataset(core_path) as ds_core:
        stats_core = compute_grid_stats(ds_core["z"])
        assert stats_core["n_lat"] == 300
        assert stats_core["n_lon"] == 300
        assert stats_core["nan_cells"] == 0
        assert stats_core["negative_count"] == 2035


def test_etopo1_marine_cells_detected():
    core_path = PROJECT_ROOT / "data/processed/gravity/WGM2012_ETOPO1_core_22_27N_90_95E.nc"
    with xr.open_dataset(core_path) as ds:
        stats = compute_grid_stats(ds["z"])
        assert stats["negative_count"] == 572
        assert stats["min"] == pytest.approx(-38.0)


def test_crust1_summary_no_fill_values_and_consistent():
    summary_path = PROJECT_ROOT / "data/processed/seismic/crust1_study_area_summary.csv"
    backup_path = PROJECT_ROOT / "data/processed/seismic/crust1_study_area_summary.csv.bak"
    assert summary_path.exists()
    assert backup_path.exists()

    df = pd.read_csv(summary_path)
    assert len(df) == 25
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    assert np.all(np.isfinite(df[numeric_cols].values))
    assert np.all(np.abs(df[numeric_cols].values) < 1e6)

    # Physical consistency: surface_elevation_km - moho_elevation_km == total_crustal_thickness_km
    diff = (df["surface_elevation_km"] - df["moho_elevation_km"]) - df["total_crustal_thickness_km"]
    assert np.all(np.abs(diff) < 0.02)

    # Verify against raw CRUST1.0 NetCDF at previously buggy cells
    ds_raw = load_crust1_raw_merged(PROJECT_ROOT / "data/raw/seismic")
    for lat, lon, expected_elev in [(25.5, 94.5, 1.35), (23.5, 93.5, 1.16)]:
        row = df[(df["latitude"] == lat) & (df["longitude"] == lon)].iloc[0]
        raw_uc_top = float(ds_raw["upper_crust_top"].sel(latitude=lat, longitude=lon).values)
        assert row["surface_elevation_km"] == pytest.approx(expected_elev, abs=1e-3)
        assert row["surface_elevation_km"] == pytest.approx(raw_uc_top, abs=1e-3)


def test_data_inventory_complete():
    inv_path = PROJECT_ROOT / "data/processed/data_inventory.csv"
    assert inv_path.exists()
    inv = pd.read_csv(inv_path)
    assert len(inv) == 12
    for col in ["dataset_id", "region", "processed_path", "valid_cells", "min", "max", "mean", "std"]:
        assert inv[col].notna().all(), f"Null values in inventory column {col}"
