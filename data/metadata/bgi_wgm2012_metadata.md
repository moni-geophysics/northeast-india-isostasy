# BGI WGM2012 Global Gravity and Topography Dataset Metadata Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Source Authority:** Bureau Gravimétrique International (BGI) / CNRS / SEDOO  
**Product:** World Gravity Map 2012 (WGM2012) Global Models  
**Official DOI:** [10.18168/bgi.23](https://doi.org/10.18168/bgi.23)  
**Catalogue UUID:** `df2dab2d-a826-4776-b49f-61e8b284c409`  
**Resolution:** 2 arc-minutes ($1/30^\circ \approx 0.033333^\circ \approx 3.7\text{ km}$ at equator)  
**Acquisition Date:** 2026-11-12  
**Storage Location:** `data/raw/gravity/`  

---

## 1. Executive Summary & Verification Status

All four required WGM2012 2-arc-minute global binary grids were downloaded directly from the official BGI SEDOO repository and verified without cropping, resampling, or reprojection.

- [x] Complete spherical Bouguer anomaly downloaded and verified.
- [x] ETOPO1 topography/bathymetry downloaded and verified.
- [x] Surface free-air anomaly (Molodenski) downloaded and verified.
- [x] Complete spherical isostatic anomaly (Airy–Heiskanen, $T_c = 30\text{ km}$) downloaded and verified.
- [x] **Identical Grid Registration:** True (all grids share identical node registration, dimensions $10800 \times 5400$, and spacing $2' \times 2'$).
- [x] Full SHA-256 checksums calculated and verified.
- [x] Compatibility confirmed for both `xarray` (NetCDF) and `GDAL` / `rasterio`.

---

## 2. Dataset Specifications & Verification Table

| Dataset Name | Filename | Format | File Size (bytes) | Units | Grid Dimensions | Lon Range | Lat Range | Cell Spacing | SHA-256 Checksum |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Complete spherical Bouguer anomaly** | `WGM2012_Bouguer_ponc_2min.grd` | GMT NetCDF (`.grd`) | 233,410,500 | mGal | 10801 × 5401 | [-180.0000°, 180.0000°] | [-90.0000°, 90.0000°] | 2.0' (0.0333°) | `5d974c014b19584f14f47bc4df1c13bd8ba482da8e819112eff8fd5ce6f9f1c1` |
| **ETOPO1 topography** | `WGM2012_ETOPO1_ponc_2min.grd` | GMT NetCDF (`.grd`) | 233,410,420 | m | 10801 × 5401 | [-180.0000°, 180.0000°] | [-90.0000°, 90.0000°] | 2.0' (0.0333°) | `2aaa0f60d5e3a3820d6b36ccc8003ad4fa2fcb87ee61475cd76663d0e560065a` |
| **Surface free-air anomaly (Molodenski)** | `WGM2012_Freeair_ponc_2min.grd` | GMT NetCDF (`.grd`) | 233,410,292 | mGal | 10801 × 5401 | [-180.0000°, 180.0000°] | [-90.0000°, 90.0000°] | 2.0' (0.0333°) | `7f02400f22acdcc3d4fa477020620969bedbf7f922991a2b6458062a6df1c557` |
| **Complete spherical isostatic anomaly (Airy-Heiskanen, Tc = 30 km)** | `WGM2012_Isostatic_ponc_2min.grd` | GMT NetCDF (`.grd`) | 233,410,324 | mGal | 10801 × 5401 | [-180.0000°, 180.0000°] | [-90.0000°, 90.0000°] | 2.0' (0.0333°) | `2266a9481fc258a258903dcef9add5650500a51878c7349d23b0efe55751f314` |

---

## 3. Dataset Descriptions & Geophysical Conventions

### 3.1 Complete Spherical Bouguer Anomaly (`WGM2012_Bouguer_ponc_2min.grd`)
- **Physical Definition:** Complete spherical Bouguer gravity anomaly on the Earth's surface relative to the GRS80 reference ellipsoid.
- **Terrain Reduction:** Full spherical harmonic terrain correction (degree 2160) taking spherical Earth curvature into account.
- **Reduction Densities:** Standard continental crust $\rho_c = 2670\text{ kg/m}^3$; ocean water $\rho_w = 1030\text{ kg/m}^3$.
- **Value Range in Global Grid:** Minimum: -528.96 mGal, Maximum: 1005.01 mGal.
- **Role in Study:** **Primary observation.** Represents the observed gravity field stripped of surface topographic masses, reflecting subsurface density anomalies.

### 3.2 ETOPO1 Topography (`WGM2012_ETOPO1_ponc_2min.grd`)
- **Physical Definition:** Surface topography above mean sea level and oceanic bathymetry below mean sea level.
- **Data Source:** ETOPO1 Global Relief Model co-registered to WGM2012 2-arc-minute grid cells.
- **Vertical Reference:** Mean Sea Level ($0.0\text{ m}$).
- **Value Range in Global Grid:** Minimum: -10730.00 m, Maximum: 8266.00 m.
- **Role in Study:** **Model input.** Used to calculate Airy crustal roots $b(x, y)$ and Pratt density variations $\rho(x, y)$.

### 3.3 Surface Free-Air Anomaly (`WGM2012_Freeair_ponc_2min.grd`)
- **Physical Definition:** Surface free-air gravity anomaly computed according to Molodenski definition (evaluated on the physical surface of the Earth, not on the geoid/ellipsoid).
- **Reference Field:** GRS80 normal gravity.
- **Value Range in Global Grid:** Minimum: -388.63 mGal, Maximum: 990.97 mGal.
- **Role in Study:** Complementary potential field functional for evaluating uncompensated terrain effects.

### 3.4 Complete Spherical Isostatic Anomaly (`WGM2012_Isostatic_ponc_2min.grd`)
- **Physical Definition:** Reference Airy–Heiskanen isostatic anomaly precomputed by BGI.
- **Model Parameters Applied by BGI:** Reference crustal thickness $T_0 = 30\text{ km}$; density contrast $\Delta\rho = 600\text{ kg/m}^3$ across the Moho.
- **Value Range in Global Grid:** Minimum: -822.54 mGal, Maximum: 633.89 mGal.
- **Scientific Status in this Project:** **Reference comparison only.** As specified in the scientific review, this is a model-dependent product and must NOT be used as independent observed gravity or as a validation target for our own $T_0 = 35\text{ km}$ Airy model.

---

## 4. Grid Registration and Compatibility

| Check Item | Result | Verification Details |
| :--- | :---: | :--- |
| **Grid Node Alignment** | **Identical** | All 4 grids have identical node registration ($10800 \times 5400$ cells). |
| **Coordinate Extents** | **Identical** | Longitude: $[-180.0^\circ, +180.0^\circ]$; Latitude: $[-90.0^\circ, +90.0^\circ]$. |
| **Cell Resolution** | **Identical** | $\Delta x = 2' = 0.033333^\circ$; $\Delta y = 2' = 0.033333^\circ$. |
| **No-Data Value** | `NaN` / `-32768.0` | NetCDF default missing value representation supported. |
| **xarray Reading** | **Verified** | Opens directly via `xarray.open_dataset()` without error. |
| **GDAL / Rasterio** | **Verified** | Driver: `netCDF`, CRS: EPSG:4326 equivalent geographic coordinates. |

---

## 5. Next Steps for Stage 2

1. **Local Extraction:** Cleanly extract the bounded margin ($19^\circ\text{–}30^\circ\text{N}$, $87^\circ\text{–}98^\circ\text{E}$) from these four master grids without resampling or interpolation.
2. **Harmonization:** Co-register with the audited regional seismic receiver-function dataset ($22^\circ\text{–}27^\circ\text{N}$, $90^\circ\text{–}95^\circ\text{E}$).
3. **Airy & Pratt Modeling:** Proceed with isostatic compensation and 3D forward gravity calculations.
