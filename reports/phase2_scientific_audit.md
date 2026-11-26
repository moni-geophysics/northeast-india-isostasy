# Phase 2 Strict Scientific Verification Audit

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Audit Scope:** `src/isostasy/airy.py`, `src/isostasy/pratt.py`, `config/model_parameters.yaml`, `reports/phase2_isostasy_methodology.md`, `tests/test_isostasy.py`  
**Date:** 2026-11-26  
**Audit Mode:** Strictly read-only on existing implementation and tests.

---

## A. Verified Equations

### 1. Airy–Heiskanen Local Isostasy (Independent Derivation & Verification)

Let $z = 0$ be Mean Sea Level (positive upward). A common compensation depth $z = -Z_{\text{comp}}$ lies below the deepest crustal root. The **reference column** ($h = 0$) has crust of thickness $T_0$ (density $\rho_c$) from $z = 0$ to $z = -T_0$, and mantle (density $\rho_m$) from $z = -T_0$ to $z = -Z_{\text{comp}}$:

$$M_{\text{ref}} = \rho_c T_0 + \rho_m (Z_{\text{comp}} - T_0)$$

- **Subaerial Land ($h \ge 0$):**
  Crust extends from $z = +h$ to $z = -(T_0 + b)$ (total crustal thickness $T_c = h + T_0 + b$), and mantle extends from $-(T_0 + b)$ to $-Z_{\text{comp}}$:
  $$M_{\text{land}} = \rho_c (h + T_0 + b) + \rho_m (Z_{\text{comp}} - T_0 - b) = M_{\text{ref}} \implies b = \frac{\rho_c}{\rho_m - \rho_c}\, h \ge 0$$
  Vertical datum quantities:
  - Moho depth below sea level: $D_{\text{Moho,SL}} = T_0 + b$
  - Moho elevation: $z_{\text{Moho}} = -(T_0 + b) = -D_{\text{Moho,SL}}$
  - Total crustal thickness: $T_c = h + T_0 + b = h + D_{\text{Moho,SL}}$
  - **Code check (`src/isostasy/airy.py`):** `airy_root_land` and `compute_airy_isostasy` match **exactly**.

- **Marine Bathymetry ($h < 0$, water depth $d = -h > 0$):**
  - **Water depth:** $d = -h > 0$ (from $z = 0$ down to $z = -d$).
  - **Reference Moho depth:** $T_0$ below sea level.
  - **Change in Moho depth:** $b$ (signed; negative for upward anti-root, i.e. anti-root magnitude $b_{\text{anti}} = -b$).
  - **Moho depth below sea level:** $D_{\text{Moho,SL}} = T_0 + b = T_0 - b_{\text{anti}}$.
  - **Actual solid crustal thickness:** From seafloor ($z = -d$) to Moho ($z = -(T_0 + b)$), $T_c = (T_0 + b) - d = T_0 + b + h$.
  - **Equal-mass balance at $z = -Z_{\text{comp}}$:**
    $$M_{\text{marine}} = \rho_w d + \rho_c (T_0 + b - d) + \rho_m (Z_{\text{comp}} - T_0 - b) = \rho_c T_0 + \rho_m (Z_{\text{comp}} - T_0)$$
    $$(\rho_w - \rho_c) d + (\rho_c - \rho_m) b = 0 \implies b = -\frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, d = \frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, h < 0$$
  - **Code check (`src/isostasy/airy.py`):** `airy_root_marine` computes `((rho_c - rho_w) / (rho_m - rho_c)) * h_km` (negative since `h_km < 0`), `moho_depth_sl_km = t0_km + b_km`, and `total_crustal_thickness_km = h_km + moho_depth_sl_km = T_0 + b - d`. Sign and variable interpretation are **mathematically exact**.

### 2. Pratt–Hayford Local Isostasy (Independent Derivation & Verification)

Compensation depth $D$ is measured downward from sea level ($z = -D$). Reference column ($h = 0$): $M_{\text{ref}} = \rho_0 D$.

- **Subaerial Land ($h \ge 0$):** Column thickness $D + h$, uniform density $\rho_{\text{Pratt}}$:
  $$\rho_{\text{Pratt}} (D + h) = \rho_0 D \implies \rho_{\text{Pratt}} = \rho_0 \frac{D}{D + h}$$
  **Code check (`src/isostasy/pratt.py`):** `pratt_density_land` matches **exactly**.

- **Marine Bathymetry ($h < 0$, $d = -h > 0$, $d < D$):** Water column ($\rho_w$, thickness $d$) over rock column ($\rho_{\text{Pratt}}$, thickness $D - d = D + h$):
  $$\rho_w d + \rho_{\text{Pratt}} (D - d) = \rho_0 D \implies \rho_{\text{Pratt}} = \frac{\rho_0 D - \rho_w d}{D - d} = \frac{\rho_0 D + \rho_w h}{D + h}$$
  **Code check (`src/isostasy/pratt.py`):** `pratt_density_marine` matches **exactly**, and enforces $D + h > 0$.

---

## B. Incorrect Equations

- **None in `src/isostasy/airy.py`, `src/isostasy/pratt.py`, or `reports/phase2_isostasy_methodology.md`.**
- **Note on stale `README.md`:** The repository root [`README.md`](file:///e:/northeast-india-isostasy/README.md) (from initial commit `69a4e87`) still states $T_{c,\text{Airy}} = T_0 + b$ and $D_{\text{Moho,SL}} = T_0 + b - h$, which was already identified and corrected in `reports/phase2_isostasy_methodology.md` and `src/isostasy/airy.py`.

---

## C. Parameter / Source Issues

1. **Pratt $\rho_0 = 3100\text{ kg/m}^3$ and $D = 100\text{ km}$:**
   - **Defensibility:** Physically defensible for a **lithospheric-scale** Pratt column (`35 km` crust at `2750` + `65 km` mantle at `3350` gives `3140 kg/m³`, matching Turcotte & Schubert's `3100 kg/m³` at $W = 100\text{ km}$).
   - **Caveat for Phase 4:** Because $\rho_0 = 3100\text{ kg/m}^3$ averages crust + lithospheric mantle, it must **not** be compared directly to CRUST1.0 *crustal* densities (`2675–2791 kg/m³`); comparisons must either use density anomalies ($\Delta\rho$) or also evaluate a crustal-scale Pratt depth ($D \approx 35\text{–}40\text{ km}$, $\rho_0 \approx 2750\text{ kg/m}^3$).
   - **Uncertainty range `[2750, 3200] kg/m³`:** Overly broad/mixed because `2750` corresponds to a crustal-scale column ($D \approx 35\text{ km}$), whereas `3100–3200` corresponds to a `100 km` lithospheric column. Changing $\rho_0$ without changing $D$ mixes two physical scales.
2. **Incomplete Bibliographic Citations in `config/model_parameters.yaml`:**
   - `Turcotte & Schubert, Geodynamics` lacks edition, year, chapter, and ISBN.
   - `Hayford (1909), The Figure of the Earth and Isostasy` lacks full title (*...from Measurements in the United States*, U.S. Coast and Geodetic Survey) and does not note that Hayford's original solution was `~113.7–122 km` (`70–76 miles`), whereas `100 km` is the modern textbook rounding.
3. **All other parameters ($T_0 = 35\text{ km}$, $\rho_c = 2750\text{ kg/m}^3$, $\rho_m = 3350\text{ kg/m}^3$, $\rho_w = 1030\text{ kg/m}^3$):** Properly sourced with DOIs/URLs, supported by the cited publications and CRUST1.0 statistics, and clearly distinguished as adopted references vs. regional observations.

---

## D. Test Coverage Gaps

Audit of [`tests/test_isostasy.py`](file:///e:/northeast-india-isostasy/tests/test_isostasy.py) (10 tests):
- **Strong independent checks:** `test_equal_mass_balance_at_compensation_depth` independently sums $\rho_w d_w + \rho_c T_c + \rho_m (Z_{\text{comp}} - D_{\text{Moho,SL}})$ and $\rho_w d_w + \rho_{\text{Pratt}}(D+h)$ against $M_{\text{ref}}$ (`rel=1e-12`). `test_positive_elevation_analytical_benchmark` uses independent hardcoded numbers.
- **Tautological benchmark:** In `test_negative_bathymetry_analytical_benchmark` (line 56), `expected_b` is computed using the same algebraic formula `((2750.0 - 1030.0) / 600.0) * (-2.0)` rather than an independent numerical literal (`-5.733333333333333`), though `test_equal_mass_balance_at_compensation_depth` catches formula errors independently.
- **Missing edge-case tests:**
  1. Invalid parameter guards (`rho_m <= rho_c`, `rho_c <= rho_w`, `t0_km <= 0`, `d_km <= 0`, `rho_0 <= rho_w`).
  2. Extreme bathymetry guard where $T_c \le 0$ (for baseline parameters, $d \ge 9.05\text{ km}$).
  3. Execution on `Earth2014_TBI2014_core_22_27N_90_95E.nc` (`2,035` marine cells) and buffered WGM2012 grid (`15,288` marine cells).

---

## E. Required Corrections (Prioritized by Severity)

| Priority | Item | Action Required |
| :---: | :--- | :--- |
| **Low** | Bibliographic completeness & Pratt $\rho_0$ uncertainty note in `config/model_parameters.yaml` | Add full citation details for Turcotte & Schubert and Hayford (1909), and tighten/annotate `rho_0` uncertainty (`[3000, 3200]` for $D=100\text{ km}$, or note coupled $(D, \rho_0)$ scaling). |
| **Low** | Hardcoded literal in `test_negative_bathymetry_analytical_benchmark` + parameter-validation tests in `tests/test_isostasy.py` | Replace formulaic `expected_b` with `-5.733333333333333` and add invalid-parameter / extreme-bathymetry tests. |
| **Low** | Stale Airy thickness equation in root `README.md` | Update `README.md` Section 3.1 to match $D_{\text{Moho,SL}} = T_0 + b$ and $T_c = h + T_0 + b$. |

*(No Critical, High, or Medium mathematical or implementation errors were found.)*

---

## F. Final Verdict

**Phase 2 is SCIENTIFICALLY ACCEPTABLE.**  
All governing Airy and Pratt equations (land and marine), sign conventions, vertical datum separations, and equal-mass balances are mathematically exact and verified both analytically and numerically (`15/15` tests passing). The minor documentation, citation, and test-hardening items listed in Section E can be folded cleanly into Phase 3 or a quick cleanup commit without blocking forward gravity modeling.
