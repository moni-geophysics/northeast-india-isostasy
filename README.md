# Northeast India Isostasy: Airy–Heiskanen and Pratt–Hayford Models

A reproducible Python geophysics framework investigating local **Airy–Heiskanen** (crustal-thickness) and **Pratt–Hayford** (lateral-density) isostatic compensation across Northeast India and adjoining transboundary regions using 3D spherical tesseroid forward gravity modeling, global gravity/topography grids, and regional seismological constraints.

---

## 1. Project Overview

### Study Region
The core analysis window spans **22.0°N–27.0°N, 90.0°E–95.0°E** (`EPSG:4326`, centered at `24.5°N, 92.5°E`), encompassing:
- **Shillong Plateau & Mikir Hills** (uplifted Precambrian basement block)
- **Brahmaputra / Assam Valley** (Himalayan foreland basin)
- **Bengal Basin / Surma Basin** (thick Neogene sedimentary wedge and Meghna coastal estuary)
- **Indo-Burma Ranges** (eastern convergence and subduction-accretion wedge)
- Adjoining territories of **Bangladesh**, **Bhutan**, and **Myanmar**

To eliminate boundary edge effects during 3D forward gravity integration, subsurface density anomalies are modeled over an extended **3° buffered domain** (**19.0°N–30.0°N, 87.0°E–98.0°E**).

### Scientific Motivation & Datasets
1. How well do classical local Airy and Pratt compensation mechanisms predict the regional gravity field over Northeast India's contrasting cratonic, foreland, and convergent provinces?
2. Where do gravity residuals diverge from local hydrostatic balance due to flexural rigidity, thick sedimentary cover, or unmodeled intracrustal density variations?
3. How do theoretical Airy Moho depths compare against independent receiver-function Moho determinations and global crustal models?

**Primary Datasets:**
- **Gravity & Co-Registered Topography:** BGI **WGM2012** 2-arc-minute global grids (`Bouguer`, `Freeair`, `ETOPO1`, `Isostatic` reference only; Balmino et al., 2012).
- **High-Resolution Topography:** **Earth2014** `TBI2014` 1-arc-minute topography/bathymetry/ice grid.
- **Global Crustal Model:** **CRUST1.0** $1^\circ \times 1^\circ$ 8-layer seismic velocity and model-derived density grid (Laske et al., 2013).
- **Regional Seismology:** 25 audited receiver-function records (21 unique core stations) compiled from Agrawal et al. (2021), Mitra et al. (2018), and Borah et al. (2016).

---

## 2. Methodology

### 2.1 Data Ingestion & Quality Control (`src/data/`)
- Deterministic subsetting of WGM2012 (`2'`, node-registered) and Earth2014 (`1'`, pixel-registered) into buffered (`19–30°N, 87–98°E`) and core (`22–27°N, 90–95°E`) NetCDF grids without resampling or altering raw files.
- Explicit identification of negative-elevation marine/estuarine cells (`572` core / `15,288` buffer cells in WGM2012 ETOPO1; `2,035` core / `60,341` buffer cells in Earth2014).
- Layer-level fill-value masking (`9.96921e+36`) for CRUST1.0 prior to computing crustal thickness and surface elevation.

### 2.2 Local Isostasy Formulations (`src/isostasy/`)
All equations are derived from equal mass per unit area at a common compensation depth below Mean Sea Level ($z = 0$, positive upward). Separate land ($h \ge 0$) and marine ($h < 0$, water depth $d_w = -h > 0$, seawater density $\rho_w = 1030\text{ kg/m}^3$) formulations are implemented:

- **Airy–Heiskanen** ($T_0 = 35.0\text{ km}$, $\rho_c = 2750\text{ kg/m}^3$, $\rho_m = 3350\text{ kg/m}^3$):
  - Land root ($h \ge 0$): $b = \frac{\rho_c}{\rho_m - \rho_c}\, h \ge 0$
  - Marine anti-root ($h < 0$): $b = \frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, h = -\frac{\rho_c - \rho_w}{\rho_m - \rho_c}\, d_w < 0$
  - Strict datum separation: $D_{\text{Moho,SL}} = T_0 + b$, $z_{\text{Moho}} = -(T_0 + b)$, and solid crustal thickness $T_c = h + T_0 + b$.
- **Pratt–Hayford** ($D = 100.0\text{ km}$, $\rho_0 = 3100\text{ kg/m}^3$):
  - Land ($h \ge 0$): $\rho_{\text{Pratt}} = \rho_0 \frac{D}{D + h}$
  - Marine ($h < 0$): $\rho_{\text{Pratt}} = \frac{\rho_0 D - \rho_w d_w}{D - d_w}$

### 2.3 3D Spherical Tesseroid Forward Gravity (`src/gravity/`)
- Geocentric spherical tesseroids ($R = 6,371,000\text{ m}$) are built over the `19–30°N, 87–98°E` buffer and evaluated on the physical Earth surface $r_{\text{obs}} = R + \max(0, h)$ across the `22–27°N, 90–95°E` core using `harmonica.tesseroid_gravity`.
- Numerical validation includes an infinite horizontal slab benchmark, a Cartesian Nagy prism benchmark, sign-reversal tests, zero-topography identity, land–marine transitions, and buffer edge-effect sensitivity tests.

---

## 3. Repository Structure

```text
northeast-india-isostasy/
├── config/
│   ├── study_area.yaml                # Study window (22-27N, 90-95E) & EPSG:4326 metadata
│   └── model_parameters.yaml          # Literature-grounded Airy & Pratt parameters + DOIs
├── data/
│   ├── README.md                      # Raw data immutability & versioning policy
│   ├── metadata/                      # Source metadata documentation (BGI WGM2012)
│   ├── raw/                           # Excluded from Git (WGM2012, Earth2014, CRUST1.0)
│   └── processed/
│       ├── data_inventory.csv         # Machine-readable summary statistics inventory
│       └── seismic/                   # CRUST1.0 summaries & audited RF station table
├── reports/                           # Phase reports, metadata validations & scientific audits
├── results/
│   ├── figures/                       # Cross-sections & scatter comparison plots
│   ├── maps/                          # Cartographic anomaly & seismic maps
│   └── tables/                        # Gravity summary statistics & profile CSVs
├── src/
│   ├── data/
│   │   ├── loaders.py                 # Grid loading, subsetting, and marine/stats inspection
│   │   ├── crust1.py                  # CRUST1.0 rasterio ingestion & fill-value masking
│   │   └── preprocess.py              # Reproducible Phase 1 pipeline
│   ├── isostasy/
│   │   ├── airy.py                    # Airy-Heiskanen land & marine models
│   │   └── pratt.py                   # Pratt-Hayford land & marine models
│   ├── gravity/
│   │   ├── forward.py                 # Harmonica 3D spherical tesseroid forward models
│   │   └── regional.py                # Regional buffered gravity & residual calculation
│   └── visualization/
│       └── phase3_plots.py            # Publication-quality maps, transects, and plots
└── tests/
    ├── test_data_preprocessing.py     # Phase 1 data integrity & CRUST1.0 tests
    ├── test_isostasy.py               # Phase 2 equal-mass, datum & analytical tests
    └── test_gravity.py                # Phase 3 slab, prism & edge-effect benchmarks
```

---

## 4. Installation and Reproducibility

### Environment Setup
Requires **Python 3.10+** (verified on Python 3.13.3).

```bash
# Create and activate virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Raw Data Retrieval (Excluded from Git)
Large raw grids (`~1.4 GB` total) and intermediate `.nc` subsets are excluded via `.gitignore`. To reproduce from scratch, place the original files in `data/raw/`:
- `data/raw/gravity/WGM2012_{Bouguer,ETOPO1,Freeair,Isostatic}_ponc_2min.grd` — [BGI SEDOO Catalogue (DOI: 10.18168/bgi.23)](https://doi.org/10.18168/bgi.23)
- `data/raw/topography/Earth2014.TBI2014.1min.geod.grd` — [Curtin Earth2014 1-min GMT archive](https://ddfe.curtin.edu.au/models/Earth2014/data_1min/GMT/Earth2014.TBI2014.1min.geod.grd)
- `data/raw/seismic/CRUST1.0-{vp,vs,rho}.r0.1-n4c.nc` — [EarthScope EMC CRUST1.0](https://data.earthscope.org/products/emc/CRUST1.0/model/)

### Running the Pipeline and Tests
```bash
# 1. Run Phase 1 preprocessing & CRUST1.0 summary generation
python -m src.data.preprocess

# 2. Run Phase 3 regional 3D forward gravity (~5-6 min on full 2-arc-min buffer)
python -m src.gravity.regional

# 3. Generate Phase 3 maps, cross-sections, and comparison plots
python -m src.visualization.phase3_plots

# 4. Run the complete unit and validation test suite
pytest -v
```

Generated outputs are written to `data/processed/data_inventory.csv`, `results/tables/`, `results/maps/`, and `results/figures/`.

---

## 5. Current Project Status

| Phase | Scope | Status | Documentation |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Data inspection, buffered/core extraction, CRUST1.0 fill-value repair | **Complete & Validated** | [`reports/phase1_data_validation.md`](reports/phase1_data_validation.md) |
| **Phase 2** | Literature parameter selection, Airy & Pratt land/marine implementation | **Complete & Audited** | [`reports/phase2_isostasy_methodology.md`](reports/phase2_isostasy_methodology.md), [`reports/phase2_scientific_audit.md`](reports/phase2_scientific_audit.md) |
| **Phase 3** | 3D spherical tesseroid forward gravity & Bouguer comparison | **Initial Implementation Complete; Audit Pending Resolution** | [`reports/phase3_forward_gravity_methodology.md`](reports/phase3_forward_gravity_methodology.md), [`reports/phase3_scientific_consistency_audit.md`](reports/phase3_scientific_consistency_audit.md) |
| **Phase 4** | Independent seismic Moho validation, $V_p$–$\rho$ analysis, sensitivity/uncertainty & final synthesis | **Pending** | — |

> **Important Note:** While Phase 3's forward modeling pipeline is implemented and passes all 21 automated tests, its independent scientific consistency audit ([`reports/phase3_scientific_consistency_audit.md`](reports/phase3_scientific_consistency_audit.md)) identified a Pratt Bouguer-stripping mismatch and minor reporting items that remain to be resolved prior to Phase 4 seismic validation.

---

## 6. Scientific Limitations

1. **Local Isostasy ($T_e = 0$):** Both Airy and Pratt assume column-by-column hydrostatic equilibrium and neglect lithospheric flexural rigidity, which is significant across the Shillong Plateau and Himalayan foreland.
2. **Single-Layer Uniform Crust:** Classical models omit thick low-density Neogene sediments in the Bengal/Surma Basin (`~10–15 km`) and dense lower-crustal/granulitic bodies.
3. **Bouguer Stripping Density Mismatch:** WGM2012 Bouguer strips topography at $\rho_B = 2670\text{ kg/m}^3$, whereas Airy uses $\rho_c = 2750\text{ kg/m}^3$ and Pratt uses $\rho_{\text{Pratt}} \approx 3017\text{–}3100\text{ kg/m}^3$ (see [`reports/phase3_scientific_consistency_audit.md`](reports/phase3_scientific_consistency_audit.md)).
4. **Effective Gravity Resolution:** Although WGM2012 grids are sampled at `2'`, the underlying EGM2008 gravity field is limited to spherical harmonic degree/order `2160` (`~5'` half-wavelength).
5. **Non-Uniqueness:** Gravity residuals alone cannot uniquely distinguish compensation state from intracrustal or sub-lithospheric density anomalies.

---

## 7. References

- **Agrawal, M., Das, M. K., Kumar, S., & Pulliam, J. (2021).** Mapping lithospheric seismic structure beneath the Shillong plateau (India) and adjoining regions by jointly fitting receiver functions and surface wave dispersion. *Geophysical Journal International*, 226(3), 1645–1675. DOI: [10.1093/gji/ggab146](https://doi.org/10.1093/gji/ggab146)
- **Balmino, G., Vales, N., Bonvalot, S., & Briais, A. (2012).** Spherical harmonic modeling to ultra-high degree of Bouguer and isostatic anomalies. *Journal of Geodesy*, 86(7), 499–520. DOI: [10.1007/s00190-011-0533-4](https://doi.org/10.1007/s00190-011-0533-4)
- **Bonvalot, S., et al. (2012).** *World Gravity Map WGM2012*. BGI–CGMW–CNES–IRD. DOI: [10.18168/bgi.23](https://doi.org/10.18168/bgi.23)
- **Borah, K., Bora, D. K., Goyal, A., & Kumar, R. (2016).** Crustal structure beneath northeast India inferred from receiver function modeling. *Physics of the Earth and Planetary Interiors*, 258, 15–27. DOI: [10.1016/j.pepi.2016.07.005](https://doi.org/10.1016/j.pepi.2016.07.005)
- **Christensen, N. I., & Mooney, W. D. (1995).** Seismic velocity structure and composition of the continental crust: A global view. *Journal of Geophysical Research: Solid Earth*, 100(B7), 9761–9788. DOI: [10.1029/95JB00259](https://doi.org/10.1029/95JB00259)
- **Laske, G., Masters, G., Ma, Z., & Pasyanos, M. (2013).** Update on CRUST1.0 — A 1-degree Global Model of Earth's Crust. *Geophysical Research Abstracts*, 15, EGU2013-2658. URL: [https://igppweb.ucsd.edu/~gabi/crust1.html](https://igppweb.ucsd.edu/~gabi/crust1.html)
- **Mitra, S., Priestley, K. F., Borah, K., & Gaur, V. K. (2018).** Crustal Structure and Evolution of the Eastern Himalayan Plate Boundary System, Northeast India. *Journal of Geophysical Research: Solid Earth*, 123(1), 621–640. DOI: [10.1002/2017JB014714](https://doi.org/10.1002/2017JB014714)
- **Turcotte, D. L., & Schubert, G. (2014).** *Geodynamics* (3rd ed.). Cambridge University Press.
- **Uieda, L., et al. (2013–2024).** Harmonica: Forward modeling, inversion, and processing gravity and magnetic data. *Fatiando a Terra*. URL: [https://www.fatiando.org/harmonica](https://www.fatiando.org/harmonica)
