# Final Project Summary: Northeast India Airy–Pratt Isostasy Analysis

**Project:** Northeast India Isostasy: Airy–Heiskanen and Pratt–Hayford Models  
**Study Window:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (Buffered Modeling Domain: `19.0°N–30.0°N`, `87.0°E–98.0°E`)  
**Horizontal CRS:** `EPSG:4326` (WGS84) | **Vertical Datum:** Mean Sea Level (MSL, $z = 0$)  
**Project Status:** Formally closed at completed **Phase 3** (Phase 4 not undertaken; independent seismic validation remains incomplete).  
**Date:** 2026-11-26  

---

## 1. Project Objectives & Methodology

The objective of this project is to formulate, implement, numerically verify, and compare classical local **Airy–Heiskanen** (crustal-thickness compensation) and **Pratt–Hayford** (lateral-density compensation) models against observed gravity over Northeast India (`22–27°N, 90–95°E`), spanning the Shillong Plateau, Brahmaputra/Assam Valley, Bengal/Surma Basin, and Indo-Burma Ranges.

### Three-Phase Executed Workflow
1. **Phase 1 — Data Inspection & Preprocessing (`src/data/`):**
   - Subsetted global WGM2012 (`2'`, node-registered) and Earth2014 `TBI2014` (`1'`, pixel-registered) grids into buffered (`19–30°N, 87–98°E`) and core (`22–27°N, 90–95°E`) NetCDF files without resampling or altering raw sources.
   - Identified negative-elevation marine/estuarine cells (`572` core / `15,288` buffer cells in WGM2012 ETOPO1; `2,035` core / `60,341` buffer cells in Earth2014).
   - Repaired an unmasked `9.96921e+36` fill-value bug in CRUST1.0's study-area summary CSV.
2. **Phase 2 — Isostatic Modeling (`src/isostasy/`):**
   - Derived land ($h \ge 0$) and marine ($h < 0$, water depth $d = -h > 0$) Airy and Pratt equations from equal mass per unit area at a common compensation depth.
   - Strictly separated root/anti-root thickness ($b$), Moho depth below sea level ($D_{\text{Moho,SL}} = T_0 + b$), Moho elevation ($z_{\text{Moho}} = -(T_0 + b)$), and solid crustal thickness ($T_c = h + T_0 + b$).
3. **Phase 3 — Bouguer-Consistent 3D Forward Gravity (`src/gravity/`):**
   - Derived and implemented two-layer Bouguer-consistent spherical tesseroids (`harmonica.tesseroid_gravity`, $R = 6,371,000\text{ m}$, $\rho_B = 2670\text{ kg/m}^3$) over `218,834` buffered tesseroids (`2 × 109,417` non-zero elevation cells) evaluated at `22,801` core surface points ($r_{\text{obs}} = R + \max(0, h) + 1.0\text{ m}$).

---

## 2. Data Sources

- **BGI WGM2012 (`2'`):** Complete spherical Bouguer (`WGM2012_Bouguer_ponc_2min.grd`), Surface Free-Air, ETOPO1 topography/bathymetry, and reference Isostatic grids (Balmino et al., 2012, DOI: `10.1007/s00190-011-0533-4`; BGI DOI: `10.18168/bgi.23`).
- **Earth2014 `TBI2014` (`1'`):** High-resolution topography/bathymetry/ice reference grid.
- **CRUST1.0 (`1°`):** Global 8-layer seismic velocity and model-derived density model (Laske et al., 2013; EarthScope EMC).
- **Regional Receiver Functions:** 25 audited station records (`21` unique core stations) compiled from Agrawal et al. (2021, DOI: `10.1093/gji/ggab146`), Mitra et al. (2018, DOI: `10.1002/2017JB014714`), and Borah et al. (2016, DOI: `10.1016/j.pepi.2016.07.005`). *(Compiled and audited in Phase 1/2; quantitative comparison against Airy/Pratt predictions was deferred to Phase 4 and not executed.)*

---

## 3. Model Equations & Parameters

All parameters are stored in [`config/model_parameters.yaml`](../config/model_parameters.yaml):
- **Airy–Heiskanen:** $T_0 = 35.0\text{ km}$, $\rho_c = 2750\text{ kg/m}^3$ (matching CRUST1.0 25-cell thickness-weighted mean `2750.9 kg/m³`), $\rho_m = 3350\text{ kg/m}^3$ ($\Delta\rho = 600\text{ kg/m}^3$), $\rho_w = 1030\text{ kg/m}^3$.
  - Land ($h \ge 0$): $b = \frac{\rho_c}{\rho_m - \rho_c} h$; root $[R-(T_0+b), R-T_0]$ at $\rho_c - \rho_m$ + mismatch $[R, R+h]$ at $\rho_c - \rho_B$.
  - Marine ($h < 0$): $b = \frac{\rho_c - \rho_w}{\rho_m - \rho_c} h$; anti-root $[R-T_0, R-(T_0+b)]$ at $\rho_m - \rho_c$ + mismatch $[R+h, R]$ at $\rho_B - \rho_c$.
- **Pratt–Hayford:** $D = 100.0\text{ km}$, $\rho_0 = 3100\text{ kg/m}^3$, $\rho_w = 1030\text{ kg/m}^3$.
  - Land ($h \ge 0$): $\rho_{\text{Pratt}} = \rho_0 \frac{D}{D+h}$; sub-geoid $[R-D, R]$ at $\rho_{\text{Pratt}} - \rho_0$ + mismatch $[R, R+h]$ at $\rho_{\text{Pratt}} - \rho_B$.
  - Marine ($h < 0$): $\rho_{\text{Pratt}} = \frac{\rho_0 D + \rho_w h}{D+h}$; sub-seafloor $[R-D, R+h]$ at $\rho_{\text{Pratt}} - \rho_0$ + water-replacement $[R+h, R]$ at $\rho_B - \rho_0$.

---

## 4. Main Corrected Phase 3 Results (`22–27°N, 90–95°E`, $N = 22,801$)

| Quantity | Units | Min | Max | Mean | Std Dev | Median | RMS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ETOPO1 Elevation** | `m` | `-38.00` | `2739.00` | `409.06` | `505.18` | `160.00` | `650.03` |
| **Observed WGM2012 Bouguer** | `mGal` | `-159.21` | `165.83` | `27.58` | `56.55` | `36.50` | `62.92` |
| **Airy Predicted Gravity (v2)** | `mGal` | `-186.01` | `-4.46` | `-58.84` | `32.81` | `-62.72` | `67.37` |
| **Pratt Predicted Gravity (v2)** | `mGal` | `-184.99` | `-4.33` | `-57.86` | `30.43` | `-62.01` | `65.37` |
| **Airy Residual (Obs − Airy)** | `mGal` | `-49.46` | `238.40` | `86.42` | `41.66` | `95.61` | `95.93` |
| **Pratt Residual (Obs − Pratt)** | `mGal` | `-52.76` | `239.30` | `85.44` | `41.98` | `95.81` | `95.19` |

- **Spatial Correlations:** Airy $r = 0.6842$; Pratt $r = 0.6862$.
- **Traceability:** Original uncorrected v1 outputs are preserved in `*_uncorrected_v1.*` files.

---

## 5. Numerical Validation

All **23/23** automated tests pass (`pytest -v`):
- **Phase 1 (5 tests):** Core/buffer NetCDF integrity, zero NaNs, marine cell counts, CRUST1.0 fill-value fix, and inventory completeness.
- **Phase 2 (10 tests):** Zero-topography identity, $+1200\text{ m}$ and $-2000\text{ m}$ analytical benchmarks, land–marine continuity, equal-mass balance (`rel=1e-12`), vertical datum consistency, `NaN` preservation, and coordinate preservation.
- **Phase 3 (8 tests):** `12°×12°` infinite horizontal slab (`0.6801%` vs. flat slab), finite Cartesian Nagy prism (`< 0.5%`), land/marine Bouguer mass balance (`rel=1e-12`), shallow-layer `8×8×4` mesh convergence (`0.212%`), sign reversal, zero topography, and `3°` buffer edge-effect verification.

---

## 6. Interpretation, Limitations & Future Research Directions

- **Unresolved Positive Regional Offset:** Observed Bouguer gravity (`mean +27.58 mGal`) and predicted compensating gravity (`-58.84` / `-57.86 mGal`) produce large positive mean residuals (`+86.42` / `+85.44 mGal`), while reducing spatial standard deviation from `56.55` to `41.66–41.98 mGal`. Neither model is claimed superior from gravity alone.
- **Key Limitations:**
  1. **No Independent Seismic Validation Executed:** Phase 4 (comparing predicted Airy $T_c$ / $D_{\text{Moho,SL}}$ against the 21 unique core receiver-function stations and CRUST1.0) was not undertaken.
  2. **Local Isostasy ($T_e = 0$):** Neglects lithospheric flexural rigidity.
  3. **Single-Layer Uniform Crust:** Unmodeled Bengal Basin sediments (`~10–15 km`) and lateral crustal density heterogeneities.
  4. **Effective Gravity Resolution:** WGM2012 gravity is limited by EGM2008 degree/order `2160` (`~5'` half-wavelength).
- **Future Directions (Phase 4+):** Quantitative station-by-station seismic Moho validation, $V_p$–$\rho$ empirical scaling against CRUST1.0, parameter sensitivity sweeps ($T_0, \rho_c, \rho_m, D, \rho_0$), and flexural ($T_e > 0$) + sedimentary-corrected 3D gravity modeling.
