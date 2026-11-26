"""
Regional 3D forward gravity computation for Northeast India (Phase 3, Part 4).

Builds buffered (19-30N, 87-98E) Airy and Pratt tesseroids from WGM2012 ETOPO1
and evaluates predicted gravity on the core (22-27N, 90-95E) physical surface
(z = max(0, h)), then compares against observed WGM2012 Complete Bouguer Anomaly.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from src.gravity.forward import (
    build_airy_tesseroids,
    build_pratt_tesseroids,
    compute_tesseroid_gravity,
)
from src.isostasy import compute_airy_isostasy, compute_pratt_isostasy, load_model_parameters


def _stats_row(name: str, units: str, arr: np.ndarray) -> dict:
    v = arr[np.isfinite(arr)]
    return {
        "quantity": name,
        "units": units,
        "n_valid": int(v.size),
        "min": float(np.min(v)),
        "max": float(np.max(v)),
        "mean": float(np.mean(v)),
        "std": float(np.std(v)),
        "median": float(np.median(v)),
        "rms": float(np.sqrt(np.mean(v**2))),
    }


def run_phase3_regional(project_root: str | Path = ".") -> tuple[xr.Dataset, pd.DataFrame]:
    root = Path(project_root)
    params = load_model_parameters(root / "config/model_parameters.yaml")

    t0_km = float(params["airy"]["reference_thickness_T0"]["value"])
    rho_c = float(params["densities"]["crust"]["value"])
    rho_m = float(params["densities"]["mantle"]["value"])
    rho_w = float(params["densities"]["seawater"]["value"])
    d_km = float(params["pratt"]["compensation_depth_D"]["value"])
    rho_0 = float(params["pratt"]["reference_density_rho0"]["value"])

    with xr.open_dataset(root / "data/processed/gravity/WGM2012_ETOPO1_buffer_19_30N_87_98E.nc") as ds_buf:
        lon_buf = ds_buf["x"].values
        lat_buf = ds_buf["y"].values
        elev_buf = ds_buf["z"].values

    with xr.open_dataset(root / "data/processed/gravity/WGM2012_ETOPO1_core_22_27N_90_95E.nc") as ds_core_e:
        lon_core = ds_core_e["x"].values
        lat_core = ds_core_e["y"].values
        elev_core = ds_core_e["z"].values

    with xr.open_dataset(root / "data/processed/gravity/WGM2012_Bouguer_core_22_27N_90_95E.nc") as ds_boug:
        bouguer_core = ds_boug["z"].values.astype(np.float64)

    obs_lon, obs_lat = np.meshgrid(lon_core, lat_core)
    obs_elev_m = np.maximum(0.0, elev_core)

    print("Building buffered Airy tesseroids...")
    t_airy, d_airy = build_airy_tesseroids(
        lon_buf, lat_buf, elev_buf, t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w
    )
    print(f"Evaluating Airy gravity ({len(t_airy)} tesseroids -> {obs_lon.size} obs pts)...")
    g_airy = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev_m, t_airy, d_airy)

    print("Building buffered Pratt tesseroids...")
    t_pratt, d_pratt = build_pratt_tesseroids(
        lon_buf, lat_buf, elev_buf, d_km=d_km, rho_0=rho_0, rho_w=rho_w
    )
    print(f"Evaluating Pratt gravity ({len(t_pratt)} tesseroids -> {obs_lon.size} obs pts)...")
    g_pratt = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev_m, t_pratt, d_pratt)

    res_airy = bouguer_core - g_airy
    res_pratt = bouguer_core - g_pratt

    airy_iso = compute_airy_isostasy(elev_core, t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w)
    pratt_iso = compute_pratt_isostasy(elev_core, d_km=d_km, rho_0=rho_0, rho_w=rho_w)

    ds_out = xr.Dataset(
        {
            "elevation_m": (("y", "x"), elev_core.astype(np.float64), {"units": "m"}),
            "bouguer_obs_mgal": (("y", "x"), bouguer_core, {"units": "mGal"}),
            "g_airy_pred_mgal": (("y", "x"), g_airy, {"units": "mGal"}),
            "g_pratt_pred_mgal": (("y", "x"), g_pratt, {"units": "mGal"}),
            "residual_airy_mgal": (("y", "x"), res_airy, {"units": "mGal"}),
            "residual_pratt_mgal": (("y", "x"), res_pratt, {"units": "mGal"}),
            "airy_root_km": (("y", "x"), airy_iso["root_thickness_km"], {"units": "km"}),
            "airy_moho_depth_sl_km": (("y", "x"), airy_iso["moho_depth_sl_km"], {"units": "km"}),
            "airy_total_crust_km": (("y", "x"), airy_iso["total_crustal_thickness_km"], {"units": "km"}),
            "pratt_density_kgm3": (("y", "x"), pratt_iso["pratt_density_kgm3"], {"units": "kg/m^3"}),
            "pratt_delta_rho_kgm3": (("y", "x"), pratt_iso["density_anomaly_kgm3"], {"units": "kg/m^3"}),
        },
        coords={"y": lat_core, "x": lon_core},
        attrs={
            "title": "Phase 3 Airy & Pratt 3D Forward Gravity Results (Core 22-27N, 90-95E)",
            "tesseroid_buffer": "19-30N, 87-98E",
            "t0_km": t0_km,
            "rho_c_kgm3": rho_c,
            "rho_m_kgm3": rho_m,
            "rho_w_kgm3": rho_w,
            "pratt_d_km": d_km,
            "pratt_rho0_kgm3": rho_0,
        },
    )
    out_nc = root / "data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc"
    ds_out.to_netcdf(out_nc)

    stats_df = pd.DataFrame(
        [
            _stats_row("ETOPO1 Elevation", "m", elev_core),
            _stats_row("Observed WGM2012 Bouguer", "mGal", bouguer_core),
            _stats_row("Airy Predicted Gravity", "mGal", g_airy),
            _stats_row("Pratt Predicted Gravity", "mGal", g_pratt),
            _stats_row("Airy Bouguer Residual (Obs - Airy)", "mGal", res_airy),
            _stats_row("Pratt Bouguer Residual (Obs - Pratt)", "mGal", res_pratt),
        ]
    )
    tables_dir = root / "results/tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    stats_df.to_csv(tables_dir / "phase3_gravity_summary_stats.csv", index=False)

    # Extract N-S profile at ~91.87E (Shillong Plateau transect) and E-W profile at ~25.5N
    ns_sub = ds_out.sel(x=91.87, method="nearest")
    ew_sub = ds_out.sel(y=25.5, method="nearest")
    df_ns = ns_sub.to_dataframe().reset_index().assign(profile="NS_91.87E")
    df_ew = ew_sub.to_dataframe().reset_index().assign(profile="EW_25.50N")
    pd.concat([df_ns, df_ew], ignore_index=True).to_csv(
        tables_dir / "phase3_profiles.csv", index=False
    )

    corr_airy = float(np.corrcoef(bouguer_core.ravel(), g_airy.ravel())[0, 1])
    corr_pratt = float(np.corrcoef(bouguer_core.ravel(), g_pratt.ravel())[0, 1])
    print(f"Saved {out_nc}")
    print(f"Correlation(Bouguer, Airy_pred) = {corr_airy:.4f}")
    print(f"Correlation(Bouguer, Pratt_pred) = {corr_pratt:.4f}")
    return ds_out, stats_df


if __name__ == "__main__":
    _, df_stats = run_phase3_regional(".")
    print(df_stats.to_string(index=False))
