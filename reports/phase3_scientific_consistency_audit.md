# Phase 3 Scientific Consistency Audit

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Audited Files:** `src/gravity/forward.py`, `src/gravity/regional.py`, `reports/phase3_forward_gravity_methodology.md`, `tests/test_gravity.py`, `config/model_parameters.yaml`  
**Date:** 2026-11-26  
**Audit Mode:** Strictly read-only (no implementation, data, or parameter files modified).

---

## 1. Summary of Findings by Severity

| Severity | Finding | Location |
| :--- | :--- | :--- |
| **Major** | **Pratt Bouguer-stripping inconsistency:** `build_pratt_tesseroids` models $\Delta\rho = \rho_{\text{Pratt}} - \rho_0$ only below $z = 0$ (land) / $z = h$ (marine), omitting the $(\rho_{\text{Pratt}} - \rho_B)$ residual topographic mass in $[0, h]$ ($\sim +347\text{ to }+430\text{ kg/m}^3$ for $\rho_0 = 3100\text{ kg/m}^3$, $\rho_B = 2670\text{ kg/m}^3$) and $(\rho_B - \rho_0)$ in marine $[h, 0]$. | `src/gravity/forward.py` (L111–149), `phase3_forward_gravity_methodology.md` |
| **Minor** | **Airy Bouguer-stripping mismatch (documented but unmodeled):** Airy uses $\rho_c = 2750\text{ kg/m}^3$ vs. WGM2012 $\rho_B = 2670\text{ kg/m}^3$ ($+80\text{ kg/m}^3$ over $[0, h]$, $\sim +1.4\text{ mGal}$ mean, $\sim +9\text{ mGal}$ peak). | `src/gravity/forward.py` (L42–109) |
| **Minor** | **Tesseroid count discrepancy:** Execution summary stated `109,561` buffered tesseroids (total `331×331` grid cells), whereas `regional.py` and the Phase 3 report correctly state `109,417` (`109,561 - 144` zero-elevation cells). | Phase 3 execution summary |
| **Minor** | **Slab test reporting error:** Report L40 states `-122.53 mGal` (`2.6%`) with a draft `"within 2.5% tolerance?"` typo; actual `12°×12°` test in `tests/test_gravity.py` yields `-124.95 mGal` vs. `-125.81 mGal` (`0.68%` difference). | `reports/phase3_forward_gravity_methodology.md` (L40) |
| **Minor** | **Over-interpretation of `+87.9 mGal` residual:** Attributing the positive mean residual to Shillong Plateau / Indian Shield dense crust is a hypothesis, not yet demonstrated from Phase 3 gravity+topography alone. | `reports/phase3_forward_gravity_methodology.md` (L64) |
| **Minor** | **Missing EGM2008 `5'` resolution caveat:** WGM2012 gravity is limited by EGM2008 (`n_max = 2160`, `~5'` half-wavelength) despite `2'` grid sampling. | `reports/phase3_forward_gravity_methodology.md` |
| **Acceptable** | **Airy tesseroid geometry & sign conventions**, **WGM2012 surface evaluation radius**, **finite-prism benchmark independence**, and **variance-reduction terminology**. | `src/gravity/forward.py`, `tests/test_gravity.py` |

---

## 2. WGM2012 Reference-Surface Consistency (Balmino et al., 2012)

Per Balmino et al. (2012, *J. Geodesy*, DOI: `10.1007/s00190-011-0533-4`) and BGI WGM2012 documentation:
1. **Gravity & Terrain Spectral Content:** Free-air anomalies are synthesized from **EGM2008** (maximum degree/order `2160`, effective half-wavelength `~5' ≈ 9 km`), whereas spherical Bouguer and terrain corrections are computed from **ETOPO1** (`1'×1'`) expanded in spherical harmonics to degree `10800`, then sampled on a `2'×2'` global grid.
2. **Evaluation Surface & Atmospheric Correction:** WGM2012 Surface Free-Air (Molodenski) and Complete Spherical Bouguer anomalies are evaluated on the **physical Earth surface** ($r_{\text{obs}} = R + \max(0, h)$) relative to GRS80, with atmospheric mass corrections applied.
3. **Land Topography ($h \ge 0$):** All topographic masses above the geoid ($z \in [0, h]$) are modeled in full spherical geometry (inherently including spherical terrain corrections) at $\rho_B = 2670\text{ kg/m}^3$ (with lakes/ice densities where applicable) and **removed**.
4. **Ocean Bathymetry ($h < 0$):** Seawater ($\rho_w = 1030\text{ kg/m}^3$) in $z \in [h, 0]$ is **replaced** by crustal rock of density $\rho_B = 2670\text{ kg/m}^3$ (adding $\Delta\rho = \rho_B - \rho_w = +1640\text{ kg/m}^3$ in $z \in [h, 0]$).
5. **Masses Retained:** All subsurface density anomalies below the geoid (and below seafloor in oceans), plus any real-Earth deviation of topographic rock density from $\rho_B = 2670\text{ kg/m}^3$.

---

## 3. Audit of Airy & Pratt Tesseroid Geometries

### 3.1 Airy–Heiskanen Geometry (`src/gravity/forward.py` L42–109)
- **Derivation:** Relative to the reference column ($\rho_c$ in $[-T_0, 0]$, $\rho_m$ in $[-Z_{\text{comp}}, -T_0]$):
  - **Land ($h \ge 0$, $b > 0$):** Root occupies $[-(T_0+b), -T_0]$ (`bottom = R - (T0+b)`, `top = R - T0`) with $\Delta\rho = \rho_c - \rho_m = -600\text{ kg/m}^3 < 0$. Lies **entirely below the geoid**.
  - **Marine ($h < 0$, $b < 0$):** Anti-root occupies $[-T_0, -(T_0+b)]$ (`bottom = R - T0`, `top = R - (T0+b)`) with $\Delta\rho = \rho_m - \rho_c = +600\text{ kg/m}^3 > 0$. Lies **entirely below the geoid**.
  - **Observation Radius:** `r_obs = R + max(0, h)`, consistent with WGM2012 physical surface evaluation.
  - **Topographic Mass Check:** No surface mass above $z = 0$ is reintroduced. However, Airy uses $\rho_c = 2750\text{ kg/m}^3$ while WGM2012 stripped topography at $\rho_B = 2670\text{ kg/m}^3$, leaving a minor unmodeled $+80\text{ kg/m}^3$ topographic residual ($\sim 3.35\text{ mGal/km}$).

### 3.2 Pratt–Hayford Geometry (`src/gravity/forward.py` L111–149)
- **What is actually implemented:** `forward.py` L135–136 sets `r_bottom = R - D` and `r_top = R + min(0, h)` — i.e., **Land: `R - D` to `R`** (NOT `R + h`) and **Marine: `R - D` to `R + h`**. Thus it does **not** extend above the geoid.
- **Physical Consistency with WGM2012 Bouguer:**
  - The **full physical Pratt column** (relative to reference $\rho_0$ in $[-D, 0]$) consists of:
    - Land ($h \ge 0$): $\rho_{\text{Pratt}}$ in $[0, +h]$ **plus** $(\rho_{\text{Pratt}} - \rho_0)$ in $[-D, 0]$ (net mass anomaly $= 0$).
    - Marine ($h < 0$): $(\rho_w - \rho_0)$ in $[h, 0]$ **plus** $(\rho_{\text{Pratt}} - \rho_0)$ in $[-D, h]$ (net mass anomaly $= 0$).
  - Applying **WGM2012 Bouguer reduction** (subtracting $\rho_B = 2670\text{ kg/m}^3$ in $[0, h]$ on land; adding $\rho_B - \rho_w = +1640\text{ kg/m}^3$ in $[h, 0]$ on marine) yields the **Bouguer-consistent Pratt anomaly**:
    - **Land ($h \ge 0$):** $(\rho_{\text{Pratt}} - \rho_B)$ in $[0, h]$ **plus** $(\rho_{\text{Pratt}} - \rho_0)$ in $[-D, 0]$.
    - **Marine ($h < 0$):** $(\rho_B - \rho_0)$ in $[h, 0]$ **plus** $(\rho_{\text{Pratt}} - \rho_0)$ in $[-D, h]$.
  - Because $\rho_0 = 3100\text{ kg/m}^3$ (lithospheric column) differs substantially from $\rho_B = 2670\text{ kg/m}^3$, omitting $(\rho_{\text{Pratt}} - \rho_B) \approx +347\text{ to }+430\text{ kg/m}^3$ over $[0, h]$ underestimates land Pratt gravity by $\sim +6.8\text{ mGal}$ on average (`h = 409 m`) and up to $\sim +40\text{ mGal}$ at `2739 m`.

### 3.3 Direct Comparison: Current vs. Bouguer-Consistent Geometry

| Model & Case | Current Implementation (`forward.py`) | Bouguer-Consistent Formulation |
| :--- | :--- | :--- |
| **Airy Land ($h \ge 0$)** | $[-(T_0+b), -T_0]$ at $\rho_c - \rho_m = -600$ | Same, plus optional $(\rho_c - \rho_B) = +80$ in $[0, h]$ (or $\rho_c = 2670$ sensitivity) |
| **Airy Marine ($h < 0$)** | $[-T_0, -(T_0+b)]$ at $\rho_m - \rho_c = +600$ | Same (water $[h, 0]$ already replaced to $\rho_B$) |
| **Pratt Land ($h \ge 0$)** | $[-D, 0]$ at $\rho_{\text{Pratt}} - \rho_0$ | $[-D, 0]$ at $\rho_{\text{Pratt}} - \rho_0$ **+** $[0, h]$ at $\rho_{\text{Pratt}} - \rho_B$ |
| **Pratt Marine ($h < 0$)** | $[-D, h]$ at $\rho_{\text{Pratt}} - \rho_0$ | $[-D, h]$ at $\rho_{\text{Pratt}} - \rho_0$ **+** $[h, 0]$ at $\rho_B - \rho_0$ |

---

## 4. Numerical & Reporting Consistency Checks

1. **`109,561` vs. `109,417` Tesseroids:** Buffer grid is `331 × 331 = 109,561` cells, of which `144` have `elevation == 0.0 m` and are skipped, yielding `109,417` active tesseroids. The Phase 3 execution summary misstated `109,561`.
2. **Slab Benchmark (`2.6%` vs. `<2.5%`):** Direct execution of the `12°×12°` test in `tests/test_gravity.py` gives `-124.952 mGal` vs. `-125.808 mGal` (**`0.6801%`** difference), confirming the test genuinely passes `< 2.5%`. Line 40 of `phase3_forward_gravity_methodology.md` erroneously retained `-122.53 mGal (2.6%)` from an earlier `10°×10°` check.
3. **Finite-Prism Benchmark Independence:** Comparing `hm.tesseroid_gravity` (spherical Gauss-Legendre quadrature) against `hm.prism_gravity` (Cartesian Nagy analytical formula) scaled to mid-depth radius is a genuinely independent mathematical check (`< 0.5%` agreement).
4. **Variance Reduction Terminology:** Spatial std drops from `56.55` to `41.66 mGal` (`26.3%` std reduction; `45.7%` variance reduction), which is accurately stated.
5. **Positive Mean Residual Attribution:** In Phase 3 alone, attributing `+87.86 mGal` to Shillong Plateau / Indian Shield dense crust goes beyond Phase 3 data and must be stated as a **hypothesis for Phase 4 seismic/density testing** rather than a Phase 3 result.
6. **WGM2012 `5'` Effective Resolution:** Should be explicitly noted in `phase3_forward_gravity_methodology.md` so `2'` short-wavelength residuals are not over-interpreted.

---

## 5. Interpretability of Existing Outputs & Minimal Correction Plan

- **Scientific Interpretability:** Existing Phase 3 Airy maps, residuals, and statistics remain **scientifically valid and interpretable** (subject to the documented `+80 kg/m³` $\rho_c$ vs. $\rho_B$ offset). Existing Pratt maps represent the *sub-sea-level compensating mass* only; their `+92.54 mGal` mean residual would shift by `~ -7 mGal` (to `~ +85 mGal`) if the $[0, h]$ $(\rho_{\text{Pratt}} - \rho_B)$ term were included, so qualitative patterns (`r = 0.677`) remain robust, but quantitative Pratt Bouguer comparison requires the correction below.
- **Affected Files & Functions (for minimal correction):**
  - `src/gravity/forward.py`: `build_pratt_tesseroids` (add $[0, h]$ layer at $\rho_{\text{Pratt}} - \rho_B$ for land and $[h, 0]$ layer at $\rho_B - \rho_0$ for marine, with `rho_bouguer=2670.0` parameter).
  - `src/gravity/regional.py`: `run_phase3_regional` (pass `rho_bouguer=2670.0` and re-run regional Pratt grid).
  - `reports/phase3_forward_gravity_methodology.md`: Fix L40 (`0.68%`), add `5'` EGM2008 resolution caveat, and frame Shillong/Shield attribution as a Phase 4 hypothesis.

---

## 6. Final Recommendation

**Recommendation: APPROVE AFTER MINOR/MAJOR CORRECTIONS (or proceed to Phase 4 if Pratt Bouguer stripping is updated cleanly).**  
Specifically: Airy forward gravity is **approved as-is**; Pratt forward gravity should be updated with the Bouguer-consistent `[0, h]` / `[h, 0]` stripping-mismatch term (or explicitly labeled as sub-sea-level compensation only) and the minor reporting errors in `reports/phase3_forward_gravity_methodology.md` should be corrected before final submission.
