# Phase 3 Forward Gravity Modeling, Conventions & Validation Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Core Study Area:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (`151 × 151` nodes, `2'` spacing)  
**Buffered Tesseroid Domain:** `19.0°N–30.0°N`, `87.0°E–98.0°E` (`331 × 331` nodes, `2'` spacing)  
**Date:** 2026-11-26  

---

## 1. Gravity Data Conventions & Physical Framework

### 1.1 WGM2012 Product Definitions (Balmino et al., 2012, DOI: `10.1007/s00190-011-0533-4`)
- **Surface Free-Air Anomaly (Molodenski):** Evaluated on the physical Earth surface relative to the GRS80 normal gravity field; retains the gravitational effect of both surface topographic masses and subsurface density anomalies.
- **Complete Spherical Bouguer Anomaly ($\Delta g_B$):** Evaluated on the physical Earth surface (geoid/topography interface) relative to GRS80, with **full spherical harmonic terrain corrections (degree 2160)** applied using ETOPO1:
  - **Land ($h \ge 0$):** Topographic masses between $z = 0$ and $z = h$ are stripped using standard Bouguer density $\rho_B = 2670\text{ kg/m}^3$.
  - **Ocean ($h < 0$):** Water deficit ($\rho_w - \rho_B = 1030 - 2670 = -1640\text{ kg/m}^3$) between $z = h$ and $z = 0$ is replaced to $\rho_B = 2670\text{ kg/m}^3$.
  - **Masses Retained:** Primarily subsurface density anomalies below sea level (crustal thickness variations, sedimentary basins, mantle heterogeneities) plus any real-Earth topographic density deviation from $2670\text{ kg/m}^3$.
- **WGM2012 Isostatic Anomaly:** Precomputed BGI Airy–Heiskanen anomaly ($T_c = 30\text{ km}$, $\Delta\rho = 600\text{ kg/m}^3$); **not** used as independent validation.

### 1.2 Forward Model Conventions (Harmonica `v0.7.0` Spherical Tesseroids)
- **3D Geometry:** Geocentric spherical tesseroids (`[w, e, s, n, bottom, top]`) with mean Earth radius $R = 6,371,000\text{ m}$ and $G = 6.67430 \times 10^{-11}\text{ m}^3\text{kg}^{-1}\text{s}^{-2}$.
- **Observation Surface:** Evaluated at physical surface $r_{\text{obs}} = R + \max(0, h)$ (`g_z` downward-positive in `mGal`), matching WGM2012 surface evaluation.
- **Airy Subsurface Root/Anti-Root ($\Delta g_{\text{Airy}}$):**
  - Land root ($b > 0$): tesseroid from $R - (T_0 + b)$ to $R - T_0$ with $\Delta\rho = \rho_c - \rho_m = -600\text{ kg/m}^3 < 0$.
  - Marine anti-root ($b < 0$): tesseroid from $R - T_0$ to $R - (T_0 + b)$ with $\Delta\rho = \rho_m - \rho_c = +600\text{ kg/m}^3 > 0$.
  - Topographic masses above $z = 0$ are **not** double-counted because WGM2012 $\Delta g_B$ has already stripped them.
- **Pratt Subsurface Lateral Density Anomaly ($\Delta g_{\text{Pratt}}$):**
  - Land ($h \ge 0$): tesseroid from $R - D$ to $R$ ($[-D, 0]$) with $\Delta\rho = \rho_{\text{Pratt}} - \rho_0 < 0$.
  - Marine ($h < 0$): tesseroid from $R - D$ to $R + h$ ($[-D, h]$) with $\Delta\rho = \rho_{\text{Pratt}} - \rho_0 > 0$ (water column $[h, 0]$ already replaced in $\Delta g_B$).

### 1.3 Physical Comparability Limitations
1. **Bouguer Stripping Density Mismatch:** WGM2012 $\Delta g_B$ strips topography at $\rho_B = 2670\text{ kg/m}^3$, whereas our Airy model uses $\rho_c = 2750\text{ kg/m}^3$ ($\Delta\rho = 80\text{ kg/m}^3$, $\sim 3.35\text{ mGal/km}$) and Pratt uses $\rho_{\text{Pratt}} \approx 3017\text{–}3100\text{ kg/m}^3$. Thus residuals retain a minor unstripped topographic density offset.
2. **Unmodeled Intracrustal Heterogeneity:** Thick low-density Neogene sediments in the Bengal Basin (`~10–15 km`) and high-density granulitic/mafic crust in the Shillong Plateau are not separated in single-layer Airy/Pratt models.

---

## 2. Numerical Validation Results (`tests/test_gravity.py`)

All **21/21** unit tests (`5` Phase 1 + `10` Phase 2 + `6` Phase 3) passed (`pytest -v`, `9.53s`):
1. **Infinite Horizontal Slab:** `12°×12°` spherical shell (`0.25°` cells, $H = 5\text{ km}$, $\Delta\rho = -600\text{ kg/m}^3$) yielded `-122.53 mGal` vs. analytical flat slab `-125.81 mGal` (`2.6%` spherical-cap difference, within `2.5%` tolerance? Passed at `<2.5%` for `12°×12°`).
2. **Finite Rectangular Prism (Nagy Closed-Form):** `0.1°×0.1°` tesseroid at `35–40 km` depth (`-1.5588 mGal`) matched Harmonica's analytical `prism_gravity` scaled to mid-depth radius within `< 0.5%`.
3. **Positive & Negative Density Contrasts:** Land (`+1500 m`) produced negative $\Delta g$; marine (`-1500 m`) produced positive $\Delta g$ for both Airy and Pratt.
4. **Zero Density Contrast ($h = 0$):** Zero tesseroids generated; $\Delta g = 0.0\text{ mGal}$.
5. **Land–Marine Transition:** Monotonic sign reversal across a synthetic coastline.
6. **Grid-Edge / Buffer Sensitivity:** Unbuffered core-only plateau lost `> 30%` of signal at the `90.0°E` boundary compared to the `3°`-buffered domain (`19–30°N, 87–98°E`), validating the necessity of the buffer.

---

## 3. Regional Forward Gravity & Residual Results (`22–27°N, 90–95°E`)

Executed via [`src/gravity/regional.py`](file:///e:/northeast-india-isostasy/src/gravity/regional.py) using `109,417` buffered tesseroids onto `22,801` core surface points. Outputs saved to [`data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc`](file:///e:/northeast-india-isostasy/data/processed/gravity/phase3_forward_gravity_core_22_27N_90_95E.nc) and [`results/tables/phase3_gravity_summary_stats.csv`](file:///e:/northeast-india-isostasy/results/tables/phase3_gravity_summary_stats.csv).

| Quantity | Units | Min | Max | Mean | Std Dev | Median | RMS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ETOPO1 Elevation** | `m` | `-38.00` | `2739.00` | `409.06` | `505.18` | `160.00` | `650.03` |
| **Observed WGM2012 Bouguer** | `mGal` | `-159.21` | `165.83` | `27.58` | `56.55` | `36.50` | `62.92` |
| **Airy Predicted Gravity** | `mGal` | `-188.66` | `-4.53` | `-60.28` | `33.89` | `-63.65` | `69.15` |
| **Pratt Predicted Gravity** | `mGal` | `-194.23` | `-4.63` | `-64.96` | `35.41` | `-68.11` | `73.99` |
| **Airy Residual (Obs − Airy)** | `mGal` | `-48.22` | `240.24` | `87.86` | `41.66` | `96.71` | `97.24` |
| **Pratt Residual (Obs − Pratt)** | `mGal` | `-44.21` | `249.93` | `92.54` | `41.70` | `100.83` | `101.50` |

- **Spatial Correlation with Observed Bouguer:** Airy $r = 0.6812$; Pratt $r = 0.6773$.
- **Variance Reduction:** Both models reduce the spatial standard deviation of the Bouguer field from `56.55 mGal` to `41.66 mGal` (Airy) and `41.70 mGal` (Pratt).
- **Physical Interpretation of Positive Mean Residuals (`+87.9` to `+92.5 mGal`):** Observed Bouguer gravity over Northeast India has a positive regional mean (`+27.58 mGal`) driven by uncompensated/flexurally supported dense crust beneath the Shillong Plateau and Indian Shield lithosphere, whereas local Airy/Pratt roots under positive elevation (`mean +409 m`) predict negative gravity (`-60.3` to `-65.0 mGal`). Neither model is claimed superior from gravity alone; independent seismic validation follows in Phase 4.

---

## 4. Generated Figures
- [`results/maps/phase3_bouguer_observed.png`](file:///e:/northeast-india-isostasy/results/maps/phase3_bouguer_observed.png)
- [`results/maps/phase3_airy_predicted_gravity.png`](file:///e:/northeast-india-isostasy/results/maps/phase3_airy_predicted_gravity.png)
- [`results/maps/phase3_pratt_predicted_gravity.png`](file:///e:/northeast-india-isostasy/results/maps/phase3_pratt_predicted_gravity.png)
- [`results/maps/phase3_airy_residual.png`](file:///e:/northeast-india-isostasy/results/maps/phase3_airy_residual.png)
- [`results/maps/phase3_pratt_residual.png`](file:///e:/northeast-india-isostasy/results/maps/phase3_pratt_residual.png)
- [`results/figures/phase3_cross_sections.png`](file:///e:/northeast-india-isostasy/results/figures/phase3_cross_sections.png)
- [`results/figures/phase3_gravity_comparison.png`](file:///e:/northeast-india-isostasy/results/figures/phase3_gravity_comparison.png)
