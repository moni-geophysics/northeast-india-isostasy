"""
Publication-quality maps, cross-sections, and comparison plots for Phase 3
3D forward gravity modeling of Northeast India.
"""

from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "figure.dpi": 150,
        "savefig.dpi": 300,
    }
)


def _plot_geo_map(
    da_x: np.ndarray,
    da_y: np.ndarray,
    data: np.ndarray,
    title: str,
    cbar_label: str,
    out_path: Path,
    cmap: str = "RdBu_r",
    vmin: float | None = None,
    vmax: float | None = None,
) -> None:
    fig = plt.figure(figsize=(7.5, 6.2))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([90.0, 95.0, 22.0, 27.0], crs=ccrs.PlateCarree())

    im = ax.pcolormesh(
        da_x,
        da_y,
        data,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        shading="auto",
        transform=ccrs.PlateCarree(),
    )
    ax.add_feature(cfeature.BORDERS, linestyle="-", linewidth=0.8, edgecolor="0.25")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.9, edgecolor="0.15")
    gl = ax.gridlines(draw_labels=True, linewidth=0.4, color="0.6", alpha=0.6, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.04)
    cbar.set_label(cbar_label)
    ax.set_title(title, pad=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def generate_phase3_figures(project_root: str | Path = ".") -> None:
    root = Path(project_root)
    ds = xr.open_dataset(root / "data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc")
    df_prof = pd.read_csv(root / "results/tables/phase3_profiles.csv")

    maps_dir = root / "results/maps"
    figs_dir = root / "results/figures"
    maps_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    x = ds["x"].values
    y = ds["y"].values

    boug = ds["bouguer_obs_mgal"].values
    g_airy = ds["g_airy_pred_mgal"].values
    g_pratt = ds["g_pratt_pred_mgal"].values
    r_airy = ds["residual_airy_mgal"].values
    r_pratt = ds["residual_pratt_mgal"].values

    # Consistent symmetric scales
    obs_lim = float(np.nanmax(np.abs(boug)))
    pred_lim = float(max(np.nanmax(np.abs(g_airy)), np.nanmax(np.abs(g_pratt))))
    res_lim = float(max(np.nanmax(np.abs(r_airy)), np.nanmax(np.abs(r_pratt))))

    # 1. Observed Bouguer anomaly map
    _plot_geo_map(
        x, y, boug,
        "Observed WGM2012 Complete Spherical Bouguer Anomaly",
        "Bouguer Anomaly (mGal)",
        maps_dir / "phase3_bouguer_observed.png",
        vmin=-obs_lim, vmax=obs_lim,
    )
    # 2. Airy predicted gravity map
    _plot_geo_map(
        x, y, g_airy,
        "Airy-Heiskanen Predicted Compensating Root Gravity (T0=35 km, Δρ=600 kg/m³)",
        "Predicted Gravity (mGal)",
        maps_dir / "phase3_airy_predicted_gravity.png",
        vmin=-pred_lim, vmax=pred_lim,
    )
    # 3. Pratt predicted gravity map
    _plot_geo_map(
        x, y, g_pratt,
        "Pratt-Hayford Predicted Subsurface Gravity (D=100 km, ρ0=3100 kg/m³)",
        "Predicted Gravity (mGal)",
        maps_dir / "phase3_pratt_predicted_gravity.png",
        vmin=-pred_lim, vmax=pred_lim,
    )
    # 4. Airy residual map
    _plot_geo_map(
        x, y, r_airy,
        "Airy Isostatic Bouguer Residual (Observed Bouguer − Airy Predicted)",
        "Residual Anomaly (mGal)",
        maps_dir / "phase3_airy_residual.png",
        vmin=-res_lim, vmax=res_lim,
    )
    # 5. Pratt residual map
    _plot_geo_map(
        x, y, r_pratt,
        "Pratt Isostatic Bouguer Residual (Observed Bouguer − Pratt Predicted)",
        "Residual Anomaly (mGal)",
        maps_dir / "phase3_pratt_residual.png",
        vmin=-res_lim, vmax=res_lim,
    )

    # 6. Representative regional cross-sections
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), sharex="col")
    for col_idx, (prof_name, coord_col, xlabel, title_prefix) in enumerate([
        ("NS_91.87E", "y", "Latitude (°N)", "N–S Transect (~91.87°E: Bengal Basin → Shillong → Assam)"),
        ("EW_25.50N", "x", "Longitude (°E)", "E–W Transect (~25.50°N: Bengal Basin → Shillong → Indo-Burma)"),
    ]):
        sub = df_prof[df_prof["profile"] == prof_name].sort_values(coord_col)
        ax_top = axes[0, col_idx]
        ax_top.fill_between(sub[coord_col], 0, sub["elevation_m"], where=sub["elevation_m"] >= 0, color="0.75", label="Topography")
        ax_top.fill_between(sub[coord_col], 0, sub["elevation_m"], where=sub["elevation_m"] < 0, color="steelblue", alpha=0.5, label="Bathymetry")
        ax_top.plot(sub[coord_col], sub["elevation_m"], color="black", lw=1.0)
        ax_top.set_ylabel("Elevation (m)")
        ax_top.set_title(title_prefix, fontweight="bold")
        ax_top.grid(alpha=0.3)
        ax_top.legend(loc="upper right", fontsize=8)

        ax_bot = axes[1, col_idx]
        ax_bot.plot(sub[coord_col], sub["bouguer_obs_mgal"], color="black", lw=1.6, label="Observed Bouguer")
        ax_bot.plot(sub[coord_col], sub["g_airy_pred_mgal"], color="tab:blue", lw=1.4, ls="--", label="Airy Predicted")
        ax_bot.plot(sub[coord_col], sub["g_pratt_pred_mgal"], color="tab:red", lw=1.4, ls="-.", label="Pratt Predicted")
        ax_bot.axhline(0, color="0.5", lw=0.7, ls=":")
        ax_bot.set_xlabel(xlabel)
        ax_bot.set_ylabel("Gravity (mGal)")
        ax_bot.grid(alpha=0.3)
        ax_bot.legend(loc="best", fontsize=8)

    fig.tight_layout()
    fig.savefig(figs_dir / "phase3_cross_sections.png", bbox_inches="tight")
    plt.close(fig)

    # 7. Comparison scatter plots
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), sharey=True)
    b_flat = boug.ravel()
    for ax, pred, label, color in [
        (axes[0], g_airy.ravel(), "Airy Predicted Gravity (mGal)", "tab:blue"),
        (axes[1], g_pratt.ravel(), "Pratt Predicted Gravity (mGal)", "tab:red"),
    ]:
        r_val = float(np.corrcoef(b_flat, pred)[0, 1])
        rmse = float(np.sqrt(np.mean((b_flat - pred) ** 2)))
        ax.hexbin(pred, b_flat, gridsize=45, cmap="Blues" if color == "tab:blue" else "Reds", mincnt=1)
        lims = [min(pred.min(), b_flat.min()), max(pred.max(), b_flat.max())]
        ax.plot(lims, lims, "k--", lw=1.2, label="1:1 line")
        ax.axhline(0, color="0.6", lw=0.6)
        ax.axvline(0, color="0.6", lw=0.6)
        ax.set_xlabel(label)
        ax.set_title(f"Observed Bouguer vs. {label.split()[0]}\n(r = {r_val:.3f}, RMSE = {rmse:.1f} mGal)")
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Observed WGM2012 Bouguer (mGal)")
    fig.tight_layout()
    fig.savefig(figs_dir / "phase3_gravity_comparison.png", bbox_inches="tight")
    plt.close(fig)

    ds.close()
    print("Generated all 7 Phase 3 maps and figures.")


if __name__ == "__main__":
    generate_phase3_figures(".")
