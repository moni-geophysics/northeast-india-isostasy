# Phase 2 Isostasy Methodology, Parameter Selection & Verification Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Study Area:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (EPSG:4326)  
**Date:** 2026-11-26  

---

## 1. Literature Review & Parameter Selection

All baseline parameters in [`config/model_parameters.yaml`](file:///e:/northeast-india-isostasy/config/model_parameters.yaml) are grounded in regional seismological constraints across `22–27°N, 90–95°E`, CRUST1.0 statistics, and peer-reviewed geodynamic/gravity literature. **Regional measurements** are explicitly distinguished from **adopted reference parameters**.

### 1.1 Summary of Regional Seismic Constraints (Observed / Model-Derived)
- **Regional Receiver Functions ($N = 21$ unique core stations):** Audited from Agrawal et al. (2021, DOI: `10.1093/gji/ggab146`), Mitra et al. (2018, DOI: `10.1002/2017JB014714`), and Borah et al. (2016, DOI: `10.1016/j.pepi.2016.07.005`). Surface-referenced crustal thickness $H$ spans `28.9–48.0 km` (mean `36.30 km`), with low-elevation foreland/basin stations near `34–38 km` (`AGT: 36.0 km`, `BELO: 35.5 km`, `BOKO: 36.0 km`, `MND: 34.0 km`). Receiver functions do **not** directly measure rock density.
- **CRUST1.0 (`25` cells in `22–27°N, 90–95°E`, Laske et al., 2013, `https://igppweb.ucsd.edu/~gabi/crust1.html`):**
  - Total crustal thickness: `35.00–42.01 km` (mean `37.91 km`, std `2.26 km`); Moho depth below sea level: `34.84–41.87 km` (mean `37.50 km`).
  - Thickness-weighted whole-crust density (including sediments): `2675–2791 kg/m³` (mean `2750.9 kg/m³`, std `39.4 kg/m³`); crystalline-only mean `2783.1 kg/m³` (`upper: 2697`, `middle: 2759`, `lower: 2929 kg/m³`). Note: CRUST1.0 densities are **model-derived** from empirical velocity–density scaling (Christensen & Mooney, 1995), not direct density measurements.
  - Sub-Moho uppermost mantle density: `3330–3410 kg/m³` (mean `3365 kg/m³`, std `25 kg/m³`).

### 1.2 Selected Model Parameters

| Parameter | Symbol | Baseline Value | Uncertainty Range | Classification | Primary Source(s) & Justification |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Reference crustal thickness** | $T_0$ | `35.0 km` | `30.0–40.0 km` | **Adopted reference** (informed by regional RF) | Consistent with low-elevation Northeast India RF stations (`34–38 km`; Borah et al., 2016; Mitra et al., 2018; Agrawal et al., 2021) and intermediate between BGI WGM2012 (`30 km`; Balmino et al., 2012, DOI: `10.1007/s00190-011-0533-4`) and global continental averages (`39–41 km`; Christensen & Mooney, 1995, DOI: `10.1029/95JB00259`). |
| **Mean crustal density** | $\rho_c$ | `2750 kg/m³` | `2670–2850 kg/m³` | **Adopted regional-consistent mean** | Matches CRUST1.0 study-area thickness-weighted whole-crust mean (`2750.9 kg/m³`; Laske et al., 2013). Uncertainty spans standard Bouguer reduction density (`2670 kg/m³`; Balmino et al., 2012) to mafic-rich continental crust (`2850 kg/m³`; Christensen & Mooney, 1995). |
| **Upper mantle density** | $\rho_m$ | `3350 kg/m³` | `3270–3410 kg/m³` | **Adopted reference** (consistent with CRUST1.0) | Consistent with CRUST1.0 study-area mantle mean (`3365 kg/m³`) and standard geodynamic mantle values (`3300 kg/m³`; Turcotte & Schubert, *Geodynamics*). Yields baseline $\Delta\rho = \rho_m - \rho_c = 600\text{ kg/m}^3$, matching WGM2012's Moho contrast. |
| **Seawater density** | $\rho_w$ | `1030 kg/m³` | `1020–1035 kg/m³` | **Adopted global reference** (not locally measured) | Standard WGM2012 ocean reduction density (Balmino et al., 2012, DOI: `10.1007/s00190-011-0533-4`). |
| **Pratt compensation depth** | $D$ | `100.0 km` | `60.0–120.0 km` | **Adopted theoretical reference** (not locally measured) | Classical Pratt–Hayford lithospheric compensation depth (Hayford, 1909; Turcotte & Schubert, *Geodynamics*, $W = 100\text{ km}$). |
| **Pratt reference density** | $\rho_0$ | `3100 kg/m³` | `2750–3200 kg/m³` | **Adopted reference** (column-consistent) | Standard `100 km` lithospheric column density (Turcotte & Schubert, *Geodynamics*); physically consistent with `35 km` crust at `2750 kg/m³` + `65 km` mantle at `3350 kg/m³` (`3140 kg/m³`). |

---

## 2. Complete Mathematical Derivations

### 2.1 Vertical Datum & Variable Definitions
- **Vertical Datum:** Mean Sea Level (MSL) at $z = 0$ (positive upward, negative downward).
- **Elevation:** $h(x,y)$ in $\text{km}$ ($h \ge 0$ subaerial land; $h < 0$ marine bathymetry with water depth $d_w = -h > 0$).
- **Strictly Separated Output Quantities:**
  1. **Root / anti-root thickness ($b$):** Vertical displacement of the Moho below ($b > 0$) or above ($b < 0$) the reference Moho depth $T_0$ below sea level.
  2. **Moho depth below sea level ($D_{\text{Moho,SL}}$):** Positive-downward distance from $z = 0$ to the Moho: $D_{\text{Moho,SL}} = T_0 + b$.
  3. **Moho elevation ($z_{\text{Moho}}$):** Coordinate relative to $z = 0$: $z_{\text{Moho}} = -(T_0 + b) = -D_{\text{Moho,SL}}$.
  4. **Total solid crustal thickness ($T_c$):** Vertical thickness of solid crust from the surface/seafloor ($z = h$) down to the Moho ($z = -(T_0 + b)$): $T_c = h + T_0 + b = h + D_{\text{Moho,SL}}$.

---

### 2.2 Airy–Heiskanen Local Isostasy

Consider a common compensation depth $z = -Z_{\text{comp}}$ deeper than the deepest crustal root ($Z_{\text{comp}} > T_0 + \max(b)$). At $h = 0$, the **reference column** consists of crust of thickness $T_0$ ($\rho_c$) and mantle of thickness $Z_{\text{comp}} - T_0$ ($\rho_m$):

$$M_{\text{ref}} = \rho_c T_0 + \rho_m (Z_{\text{comp}} - T_0)$$

#### Case 1: Subaerial Land ($h \ge 0$)
Crust extends from $z = +h$ to $z = -(T_0 + b)$ (thickness $T_c = h + T_0 + b$), underlain by mantle from $-(T_0 + b)$ to $-Z_{\text{comp}}$:

$$M_{\text{land}} = \rho_c (h + T_0 + b) + \rho_m (Z_{\text{comp}} - T_0 - b)$$

Equating $M_{\text{land}} = M_{\text{ref}}$:

$$\rho_c h + (\rho_c - \rho_m) b = 0 \implies b(h) = \frac{\rho_c}{\rho_m - \rho_c}\, h \quad (h \ge 0)$$

> **Note on `README.md` Correction:** The initial `README.md` wrote $T_c = T_0 + b$ alongside $D_{\text{Moho,SL}} = T_0 + b - h$, which violates equal mass per unit area when $b = \frac{\rho_c}{\rho_m - \rho_c} h$. Exact hydrostatic balance requires $D_{\text{Moho,SL}} = T_0 + b$ and $T_c = h + T_0 + b$.

#### Case 2: Marine Bathymetry ($h < 0$, water depth $d_w = -h > 0$)
Seawater ($\rho_w$) occupies $z \in [h, 0]$ (thickness $d_w = -h$), solid crust ($\rho_c$) occupies $z \in [-(T_0 + b), h]$ (thickness $T_c = T_0 + b + h$), and mantle ($\rho_m$) occupies $[-Z_{\text{comp}}, -(T_0 + b)]$:

$$M_{\text{marine}} = \rho_w (-h) + \rho_c (T_0 + b + h) + \rho_m (Z_{\text{comp}} - T_0 - b)$$

Equating $M_{\text{marine}} = M_{\text{ref}}$:

$$(\rho_c - \rho_w) h + (\rho_c - \rho_m) b = 0 \implies b(h) = \frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, h = -\frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, d_w \quad (h < 0)$$

---

### 2.3 Pratt–Hayford Local Isostasy

Consider a flat compensation depth $z = -D$ below sea level ($D > 0$). At $h = 0$, the **reference column** has uniform density $\rho_0$ over thickness $D$:

$$M_{\text{ref}} = \rho_0 D$$

#### Case 1: Subaerial Land ($h \ge 0$)
Rock column of uniform density $\rho_{\text{Pratt}}$ extends from $z = +h$ to $z = -D$ (thickness $D + h$):

$$\rho_{\text{Pratt}} (D + h) = \rho_0 D \implies \rho_{\text{Pratt}}(h) = \rho_0 \frac{D}{D + h}, \quad \Delta\rho(h) = \rho_{\text{Pratt}} - \rho_0 = -\rho_0 \frac{h}{D + h}$$

#### Case 2: Marine Bathymetry ($h < 0$, $d_w = -h > 0$, $d_w < D$)
Water column ($\rho_w$) occupies $z \in [h, 0]$ (thickness $d_w = -h$), underlain by rock ($\rho_{\text{Pratt}}$) from $z = h$ to $z = -D$ (thickness $D + h = D - d_w$):

$$\rho_w (-h) + \rho_{\text{Pratt}} (D + h) = \rho_0 D \implies \rho_{\text{Pratt}}(h) = \frac{\rho_0 D + \rho_w h}{D + h} = \frac{\rho_0 D - \rho_w d_w}{D - d_w}$$

$$\Delta\rho(h) = \rho_{\text{Pratt}} - \rho_0 = \frac{(\rho_0 - \rho_w) d_w}{D - d_w} > 0$$

---

## 3. Implementation, Assumptions & Limitations

- **Implementation:** [`src/isostasy/airy.py`](file:///e:/northeast-india-isostasy/src/isostasy/airy.py) and [`src/isostasy/pratt.py`](file:///e:/northeast-india-isostasy/src/isostasy/pratt.py) provide separate land and marine functions plus unified array/xarray dispatchers that preserve coordinates and `NaN` values.
- **Assumptions & Limitations:**
  1. **Local (zero flexural rigidity) compensation:** Both Airy and Pratt assume $T_e = 0\text{ km}$ (column-by-column hydrostatic balance), neglecting lithospheric flexure across the Shillong Plateau and Himalayan foreland.
  2. **Uniform column densities:** Classical Airy uses a single mean $\rho_c$ (ignoring `~10–15 km` low-density Bengal Basin sediments), and Pratt distributes density anomalies uniformly over $D$.
  3. **No forward gravity or residual validation yet:** Gravity modeling and comparison against WGM2012 Bouguer and seismic Moho are deferred to Phases 3–4.

---

## 4. Unit-Test Verification Results

Executed `.\.venv\Scripts\python.exe -m pytest -v` across [`tests/test_data_preprocessing.py`](file:///e:/northeast-india-isostasy/tests/test_data_preprocessing.py) (5 tests) and [`tests/test_isostasy.py`](file:///e:/northeast-india-isostasy/tests/test_isostasy.py) (10 tests):
- **Result:** **15 passed in 1.95s** (0 failures, 0 skipped).
- **Verified Benchmarks:** Zero topography, $+1200\text{ m}$ land analytical benchmark ($b = 5.5\text{ km}$, $D_{\text{Moho,SL}} = 40.5\text{ km}$, $T_c = 41.7\text{ km}$), $-2000\text{ m}$ marine analytical benchmark ($b = -5.7333\text{ km}$, $\rho_{\text{Pratt}} = 3142.2449\text{ kg/m}^3$), exact equal-mass balance to `1e-12` relative tolerance, `NaN` preservation, and coordinate preservation on `WGM2012_ETOPO1_core_22_27N_90_95E.nc` (`572` marine cells).
