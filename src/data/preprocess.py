"""
Reproducible Phase 1 preprocessing pipeline for Northeast India Isostasy:
1. Inspect and subset WGM2012 gravity/topography and Earth2014 topography
   for both the buffered (19-30N, 87-98E) and core (22-27N, 90-95E) domains.
2. Save processed NetCDF subsets with full provenance metadata.
3. Regenerate CRUST1.0 study-area summary CSV with proper fill-value masking
   (backing up the previous buggy CSV first).
4. Generate a machine-readable data inventory at data/processed/data_inventory.csv.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.data.crust1 import (
    build_crust1_summary,
    load_crust1_raw_merged,
    subset_crust1_study_area,
)
from src.data.loaders import (
    BUFFER_BOUNDS,
    CORE_BOUNDS,
    compute_grid_stats,
    load_grid,
    subset_grid,
)

GRID_SPECS = [
    {
        "dataset_id": "WGM2012_Bouguer",
        "raw_path": "data/raw/gravity/WGM2012_Bouguer_ponc_2min.grd",
        "out_dir": "data/processed/gravity",
        "out_prefix": "WGM2012_Bouguer",
        "quantity": "Complete spherical Bouguer gravity anomaly",
        "units": "mGal",
        "vertical_datum": "GRS80 reference ellipsoid; terrain reduction rho_c=2670, rho_w=1030 kg/m3",
        "registration": "node-registered (2 arc-min)",
    },
    {
        "dataset_id": "WGM2012_ETOPO1",
        "raw_path": "data/raw/gravity/WGM2012_ETOPO1_ponc_2min.grd",
        "out_dir": "data/processed/gravity",
        "out_prefix": "WGM2012_ETOPO1",
        "quantity": "ETOPO1 topography/bathymetry (co-registered to WGM2012)",
        "units": "m",
        "vertical_datum": "Mean Sea Level (ETOPO1 geoid/MSL reference)",
        "registration": "node-registered (2 arc-min)",
    },
    {
        "dataset_id": "WGM2012_Freeair",
        "raw_path": "data/raw/gravity/WGM2012_Freeair_ponc_2min.grd",
        "out_dir": "data/processed/gravity",
        "out_prefix": "WGM2012_Freeair",
        "quantity": "Surface free-air gravity anomaly (Molodenski)",
        "units": "mGal",
        "vertical_datum": "Physical Earth surface relative to GRS80",
        "registration": "node-registered (2 arc-min)",
    },
    {
        "dataset_id": "WGM2012_Isostatic",
        "raw_path": "data/raw/gravity/WGM2012_Isostatic_ponc_2min.grd",
        "out_dir": "data/processed/gravity",
        "out_prefix": "WGM2012_Isostatic",
        "quantity": "Complete spherical Airy-Heiskanen isostatic anomaly (Tc=30 km, reference only)",
        "units": "mGal",
        "vertical_datum": "GRS80 reference ellipsoid (BGI Tc=30 km, delta_rho=600 kg/m3)",
        "registration": "node-registered (2 arc-min)",
    },
    {
        "dataset_id": "Earth2014_TBI2014",
        "raw_path": "data/raw/topography/Earth2014.TBI2014.1min.geod.grd",
        "out_dir": "data/processed/topography",
        "out_prefix": "Earth2014_TBI2014",
        "quantity": "Earth2014 Topography-Bathymetry-Ice (TBI2014) elevation",
        "units": "m",
        "vertical_datum": "EGM2008 geoid / MSL (orthometric height, 1 arc-min)",
        "registration": "pixel-registered (1 arc-min)",
    },
]


def run_phase1_preprocessing(project_root: str | Path = ".") -> pd.DataFrame:
    """Execute full Phase 1 preprocessing and return the data inventory DataFrame."""
    root = Path(project_root)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    inventory_rows: list[dict] = []

    # 1. Process WGM2012 and Earth2014 grids
    for spec in GRID_SPECS:
        raw_path = root / spec["raw_path"]
        out_dir = root / spec["out_dir"]
        out_dir.mkdir(parents=True, exist_ok=True)

        ds = load_grid(raw_path)
        var_name = list(ds.data_vars)[0]

        for region_name, bounds, suffix in [
            ("buffer", BUFFER_BOUNDS, "buffer_19_30N_87_98E"),
            ("core", CORE_BOUNDS, "core_22_27N_90_95E"),
        ]:
            sub = subset_grid(
                ds,
                lat_min=bounds["lat_min"],
                lat_max=bounds["lat_max"],
                lon_min=bounds["lon_min"],
                lon_max=bounds["lon_max"],
                region_label=region_name,
            )
            sub.attrs["source_file"] = spec["raw_path"]
            sub.attrs["units"] = spec["units"]
            sub.attrs["vertical_datum"] = spec["vertical_datum"]
            sub.attrs["horizontal_crs"] = "EPSG:4326"
            sub.attrs["processed_utc"] = timestamp

            out_path = out_dir / f"{spec['out_prefix']}_{suffix}.nc"
            sub.to_netcdf(out_path)

            stats = compute_grid_stats(sub[var_name])
            inventory_rows.append(
                {
                    "dataset_id": spec["dataset_id"],
                    "region": region_name,
                    "processed_path": str(out_path.relative_to(root)).replace("\\", "/"),
                    "raw_path": spec["raw_path"],
                    "quantity": spec["quantity"],
                    "units": spec["units"],
                    "horizontal_crs": "EPSG:4326",
                    "vertical_datum": spec["vertical_datum"],
                    "registration": spec["registration"],
                    **stats,
                }
            )
        ds.close()

    # 2. Fix CRUST1.0 summary CSV from raw NetCDF (preserving backup)
    seismic_proc_dir = root / "data/processed/seismic"
    summary_csv = seismic_proc_dir / "crust1_study_area_summary.csv"
    backup_csv = seismic_proc_dir / "crust1_study_area_summary.csv.bak"
    if summary_csv.exists() and not backup_csv.exists():
        shutil.copy2(summary_csv, backup_csv)

    ds_crust_raw = load_crust1_raw_merged(root / "data/raw/seismic")
    ds_crust_sub = subset_crust1_study_area(
        ds_crust_raw,
        lat_min=CORE_BOUNDS["lat_min"],
        lat_max=CORE_BOUNDS["lat_max"],
        lon_min=CORE_BOUNDS["lon_min"],
        lon_max=CORE_BOUNDS["lon_max"],
    )
    df_crust_summary = build_crust1_summary(ds_crust_sub)
    df_crust_summary.to_csv(summary_csv, index=False)
    ds_crust_raw.close()

    # Record CRUST1.0 and Regional RF station datasets in inventory
    inventory_rows.append(
        {
            "dataset_id": "CRUST1.0_summary",
            "region": "core",
            "processed_path": "data/processed/seismic/crust1_study_area_summary.csv",
            "raw_path": "data/raw/seismic/CRUST1.0-{vp,vs,rho}.r0.1-n4c.nc",
            "quantity": "CRUST1.0 1-deg cell summary (crustal thickness, Moho depth, layer Vp/rho)",
            "units": "km, km/s, g/cm3",
            "horizontal_crs": "EPSG:4326",
            "vertical_datum": "Mean Sea Level (MSL, 0.0 km)",
            "registration": "cell-centred (1.0 deg)",
            "n_lat": 5,
            "n_lon": 5,
            "total_cells": len(df_crust_summary),
            "valid_cells": int(df_crust_summary["total_crustal_thickness_km"].notna().sum()),
            "nan_cells": int(df_crust_summary["total_crustal_thickness_km"].isna().sum()),
            "lat_min": float(df_crust_summary["latitude"].min()),
            "lat_max": float(df_crust_summary["latitude"].max()),
            "lon_min": float(df_crust_summary["longitude"].min()),
            "lon_max": float(df_crust_summary["longitude"].max()),
            "dx_deg": 1.0,
            "dy_deg": 1.0,
            "min": float(df_crust_summary["total_crustal_thickness_km"].min()),
            "max": float(df_crust_summary["total_crustal_thickness_km"].max()),
            "mean": float(df_crust_summary["total_crustal_thickness_km"].mean()),
            "std": float(df_crust_summary["total_crustal_thickness_km"].std()),
            "negative_count": int((df_crust_summary["surface_elevation_km"] < 0).sum()),
            "zero_count": int((df_crust_summary["surface_elevation_km"] == 0).sum()),
        }
    )

    rf_csv = seismic_proc_dir / "regional_receiver_function_stations.csv"
    df_rf = pd.read_csv(rf_csv)
    rf_core = df_rf[df_rf["in_core_study_area"] == True]
    inventory_rows.append(
        {
            "dataset_id": "Regional_RF_Stations",
            "region": "core+context",
            "processed_path": "data/processed/seismic/regional_receiver_function_stations.csv",
            "raw_path": "Agrawal2021; Mitra2018; Borah2016",
            "quantity": "Audited receiver-function Moho depth & Vp/Vs",
            "units": "km, dimensionless",
            "horizontal_crs": "EPSG:4326",
            "vertical_datum": "Surface-referenced H and MSL-referenced D_Moho_SL both tabulated",
            "registration": "point stations (25 records; 21 unique in core)",
            "n_lat": int(len(df_rf)),
            "n_lon": int(len(df_rf)),
            "total_cells": int(len(df_rf)),
            "valid_cells": int(df_rf["preferred_moho_depth_surface_km"].notna().sum()),
            "nan_cells": int(df_rf["preferred_moho_depth_surface_km"].isna().sum()),
            "lat_min": float(rf_core["latitude"].min()),
            "lat_max": float(rf_core["latitude"].max()),
            "lon_min": float(rf_core["longitude"].min()),
            "lon_max": float(rf_core["longitude"].max()),
            "dx_deg": float("nan"),
            "dy_deg": float("nan"),
            "min": float(rf_core["preferred_moho_depth_surface_km"].min()),
            "max": float(rf_core["preferred_moho_depth_surface_km"].max()),
            "mean": float(rf_core["preferred_moho_depth_surface_km"].mean()),
            "std": float(rf_core["preferred_moho_depth_surface_km"].std()),
            "negative_count": int((df_rf["elevation_m"] < 0).sum()),
            "zero_count": int((df_rf["elevation_m"] == 0).sum()),
        }
    )

    inv_df = pd.DataFrame(inventory_rows)
    inv_path = root / "data/processed/data_inventory.csv"
    inv_df.to_csv(inv_path, index=False)
    return inv_df


if __name__ == "__main__":
    df_inv = run_phase1_preprocessing(".")
    print(f"Phase 1 preprocessing complete. Inventory written ({len(df_inv)} entries).")
