# Phase 3 Forward Gravity Modeling, Conventions & Validation Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Core Study Area:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (`151 × 151` nodes, `2'` spacing)  
**Buffered Tesseroid Domain:** `19.0°N–30.0°N`, `87.0°E–98.0°E` (`331 × 331` nodes, `2'` spacing; `109,561` total grid cells, `109,417` non-zero elevation cells after skipping `144` cells with $h = 0\text{ m}$)  
**Revision:** Bouguer-consistent formulation (v2, superseding `*_uncorrected_v1` backups)  
**Date:** 2026-11-26  

---

## 1. Gravity Data Conventions & Physical Framework

### 1.1 WGM2012 Product Definitions (Balmino et al., 2012, DOI: `10.1007/s00190-011-0533-4`)
- **Surface Free-Air Anomaly (Molodenski):** Evaluated on the physical Earth surface relative to GRS80 normal gravity; retains both surface topographic masses and subsurface density anomalies.
- **Complete Spherical Bouguer Anomaly ($\Delta g_B$):** Evaluated on the physical Earth surface relative to GRS80 with atmospheric corrections and full spherical harmonic terrain corrections (ETOPO1 expanded to degree `10800`):
  - **Land ($h \ge 0$):** Topographic masses in $z \in [0, h]$ are stripped using $\rho_B = 2670\text{ kg/m}^3$.
  - **Ocean ($h < 0$, water depth $d = -h > 0$):** Seawater ($\rho_w = 1030\text{ kg/m}^3$) in $z \in [h, 0]$ is replaced by $\rho_B = 2670\text{ kg/m}^3$ ($+\Delta\rho = +1640\text{ kg/m}^3$).
- **Effective Spectral Resolution Caveat:** Although WGM2012 grids are sampled at `2'`, the underlying **EGM2008** gravity field is limited to spherical harmonic degree/order `2160` (**$\approx 5'$ half-wavelength**, `~9 km`), limiting short-wavelength interpretation of `2'` residuals.
- **WGM2012 Isostatic Anomaly:** Precomputed BGI product ($T_c = 30\text{ km}$, $\Delta\rho = 600\text{ kg/m}^3$); **not** used as independent validation.

### 1.2 Bouguer-Consistent Forward Model Conventions (Harmonica `v0.7.0`)
Derived in [`reports/phase3_pratt_bouguer_mass_balance_derivation.md`](reports/phase3_pratt_bouguer_mass_balance_derivation.md) with $R = 6,371,000\text{ m}$, $G = 6.67430 \times 10^{-11}\text{ m}^3\text{kg}^{-1}\text{s}^{-2}$, and $\rho_B = 2670.0\text{ kg/m}^3$:
- **Observation Surface:** Evaluated at $r_{\text{obs}} = R + \max(0, h) + 1.0\text{ m}$ (`g_z` downward-positive in `mGal`). The `1.0 m` numerical offset prevents Harmonica's `ZeroDivisionError` when observation points sit directly on shallow tesseroid top faces (`dz = 0.1 m` vs. `1.0 m` differs by `< 0.002 mGal`).
- **Airy–Heiskanen (2 layers per non-zero cell, `218,834` tesseroids):**
  - Land ($h > 0$): root $[R - (T_0 + b),\, R - T_0]$ at $\rho_c - \rho_m = -600\text{ kg/m}^3$ **+** stripping mismatch $[R,\, R + h]$ at $\rho_c - \rho_B = +80\text{ kg/m}^3$ (net mass $= -\rho_B h$).
  - Marine ($h < 0$): anti-root $[R - T_0,\, R - (T_0 + b)]$ at $\rho_m - \rho_c = +600\text{ kg/m}^3$ **+** water-fill mismatch $[R + h,\, R]$ at $\rho_B - \rho_c = -80\text{ kg/m}^3$ (net mass $= +(\rho_B - \rho_w)d$).
- **Pratt–Hayford (2 layers per non-zero cell, `218,834` tesseroids):**
  - Land ($h > 0$): sub-geoid $[R - D,\, R]$ at $\rho_{\text{Pratt}} - \rho_0$ **+** stripping mismatch $[R,\, R + h]$ at $\rho_{\text{Pratt}} - \rho_B$ (net mass $= -\rho_B h$).
  - Marine ($h < 0$): sub-seafloor $[R - D,\, R + h]$ at $\rho_{\text{Pratt}} - \rho_0$ **+** water-replacement $[R + h,\, R]$ at $\rho_B - \rho_0 = -430\text{ kg/m}^3$ (net mass $= +(\rho_B - \rho_w)d$).

---

## 2. Numerical Validation & Convergence Results (`tests/test_gravity.py`)

All **23/23** unit tests (`5` Phase 1 + `10` Phase 2 + `8` Phase 3) passed (`pytest -v`):
1. **Infinite Horizontal Slab:** `12°×12°` spherical shell (`0.25°` cells, $H = 5\text{ km}$, $\Delta\rho = -600\text{ kg/m}^3$) yielded `-124.95 mGal` vs. analytical flat slab `-125.81 mGal` (**`0.6801%`** difference, within `2.5%` tolerance).
2. **Finite Rectangular Prism (Nagy Closed-Form):** `0.1°×0.1°` tesseroid at `35–40 km` depth matched Harmonica's analytical `prism_gravity` scaled to mid-depth radius within `< 0.5%`.
3. **Bouguer Mass Balance (Land & Marine):** Independent verification that total column mass $\sum \Delta z \cdot \Delta\rho$ equals $-\rho_B h$ on land and $+(\rho_B - \rho_w)d$ on marine to `1e-12` relative tolerance, with `bottom < top` for all tesseroids.
4. **Shallow-Layer Convergence:** A `2'` shallow tesseroid `[R, R+2000]` evaluated at its top face (`radial_adaptive_discretization=False`) converged within **`0.212%`** (`< 0.5%`) of an `8×8×4` refined sub-mesh (`3.9075` vs. `3.8992 mGal`). On the full core grid, `dz = 0.1 m` and `dz = 1.0 m` agreed to `0.0002 mGal` in mean (`-34.4567` vs. `-34.4565 mGal`).
5. **Sign Contrasts, Zero Topography, Coastline Transition & Buffer Sensitivity:** All verified; unbuffered core plateau loses `> 30%` of signal at the `90.0°E` boundary.

---

## 3. Regional Forward Gravity & Residual Results (`22–27°N, 90–95°E`)

Executed via [`src/gravity/regional.py`](src/gravity/regional.py) (`218,834` buffered tesseroids onto `22,801` core surface points). Corrected outputs are saved to [`data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc`](data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc) and [`results/tables/phase3_gravity_summary_stats.csv`](results/tables/phase3_gravity_summary_stats.csv) (original v1 outputs preserved with `_uncorrected_v1` suffix).

| Quantity | Units | Min | Max | Mean | Std Dev | Median | RMS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ETOPO1 Elevation** | `m` | `-38.00` | `2739.00` | `409.06` | `505.18` | `160.00` | `650.03` |
| **Observed WGM2012 Bouguer** | `mGal` | `-159.21` | `165.83` | `27.58` | `56.55` | `36.50` | `62.92` |
| **Airy Predicted Gravity (v2)** | `mGal` | `-186.01` | `-4.46` | `-58.84` | `32.81` | `-62.72` | `67.37` |
| **Pratt Predicted Gravity (v2)** | `mGal` | `-184.99` | `-4.33` | `-57.86` | `30.43` | `-62.01` | `65.37` |
| **Airy Residual (Obs − Airy)** | `mGal` | `-49.46` | `238.40` | `86.42` | `41.66` | `95.61` | `95.93` |
| **Pratt Residual (Obs − Pratt)** | `mGal` | `-52.76` | `239.30` | `85.44` | `41.98` | `95.81` | `95.19` |

- **Spatial Correlation with Observed Bouguer:** Airy $r = 0.6842$; Pratt $r = 0.6862$.
- **Unresolved Regional Offset:** Both models exhibit a strong positive mean residual (`+86.42 mGal` for Airy; `+85.44 mGal` for Pratt) because observed Bouguer gravity has a positive regional mean (`+27.58 mGal`) while compensating roots under positive topography (`mean +409.06 m`) produce negative gravity (`-58.84` and `-57.86 mGal`). Potential geological causes (such as dense uncompensated crust beneath the Shillong Plateau / Indian Shield, flexural support, or Bengal Basin sediments) are **hypotheses to be tested in Phase 4** with independent seismic and density constraints, not established findings from Phase 3 alone. Neither model is claimed superior from gravity correlation alone.

---

## 4. Generated Figures
- [`results/maps/phase3_bouguer_observed.png`](results/maps/phase3_bouguer_observed.png)
- [`results/maps/phase3_airy_predicted_gravity.png`](results/maps/phase3_airy_predicted_gravity.png)
- [`results/maps/phase3_pratt_predicted_gravity.png`](results/maps/phase3_pratt_predicted_gravity.png)
- [`results/maps/phase3_airy_residual.png`](results/maps/phase3_airy_residual.png)
- [`results/maps/phase3_pratt_residual.png`](results/maps/phase3_pratt_residual.png)
- [`results/figures/phase3_cross_sections.png`](results/figures/phase3_cross_sections.png)
- [`results/figures/phase3_gravity_comparison.png`](results/figures/phase3_gravity_comparison.png)
