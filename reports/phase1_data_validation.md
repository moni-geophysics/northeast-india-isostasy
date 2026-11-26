# Phase 1 Data Inspection, Preprocessing & Validation Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Core Study Area:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (EPSG:4326)  
**Buffered Modeling Domain:** `19.0°N–30.0°N`, `87.0°E–98.0°E` (EPSG:4326)  
**Date:** 2026-11-26  

---

## 1. Executive Summary

Phase 1 executed a full quantitative inspection, reproducible spatial subsetting, CRUST1.0 fill-value repair, and automated validation across all gravity, topography, and seismic datasets:
- **Reproducible Preprocessing:** Implemented in [`src/data/loaders.py`](file:///e:/northeast-india-isostasy/src/data/loaders.py), [`src/data/crust1.py`](file:///e:/northeast-india-isostasy/src/data/crust1.py), and [`src/data/preprocess.py`](file:///e:/northeast-india-isostasy/src/data/preprocess.py).
- **Processed NetCDF Subsets:** 10 clean NetCDF subsets generated (5 datasets $\times$ 2 domains: buffer and core) with zero NaNs and preserved source metadata.
- **CRUST1.0 Fill-Value Fix:** Resolved the unmasked `9.96921e+36` fill-value contamination in [`data/processed/seismic/crust1_study_area_summary.csv`](file:///e:/northeast-india-isostasy/data/processed/seismic/crust1_study_area_summary.csv) (original preserved at `crust1_study_area_summary.csv.bak`) and verified against raw `CRUST1.0-*.nc` files.
- **Data Inventory:** Machine-readable inventory written to [`data/processed/data_inventory.csv`](file:///e:/northeast-india-isostasy/data/processed/data_inventory.csv).
- **Automated Tests:** 5/5 tests in [`tests/test_data_preprocessing.py`](file:///e:/northeast-india-isostasy/tests/test_data_preprocessing.py) passed (`pytest -v`).

---

## 2. Grid Inspection & Quantitative Statistics

### 2.1 Buffered Modeling Domain (`19.0°N–30.0°N`, `87.0°E–98.0°E`)

| Dataset | Shape | Valid / Total | Min | Max | Mean | Std Dev | `< 0` Count | `== 0` Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WGM2012 Bouguer** (`mGal`) | `331×331` | `109,561 / 109,561` | `-499.8708` | `241.0624` | `-30.0560` | `168.4757` | `46,103` | `0` |
| **WGM2012 ETOPO1** (`m`) | `331×331` | `109,561 / 109,561` | `-2296.0000` | `8266.0000` | `1105.7471` | `1802.8877` | `15,288` | `144` |
| **WGM2012 Free-Air** (`mGal`) | `331×331` | `109,561 / 109,561` | `-346.8370` | `667.6880` | `-6.2968` | `84.6333` | `70,845` | `1` |
| **WGM2012 Isostatic** (`mGal`) | `331×331` | `109,561 / 109,561` | `-156.2230` | `275.8450` | `-5.5920` | `35.5213` | `64,248` | `3` |
| **Earth2014 TBI2014** (`m`) | `660×660` | `435,600 / 435,600` | `-2225.0000` | `7941.0000` | `1106.3920` | `1794.7593` | `60,341` | `1,281` |

### 2.2 Core Study Area (`22.0°N–27.0°N`, `90.0°E–95.0°E`)

| Dataset | Shape | Valid / Total | Min | Max | Mean | Std Dev | `< 0` Count | `== 0` Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WGM2012 Bouguer** (`mGal`) | `151×151` | `22,801 / 22,801` | `-159.2094` | `165.8308` | `27.5776` | `56.5499` | `7,299` | `0` |
| **WGM2012 ETOPO1** (`m`) | `151×151` | `22,801 / 22,801` | `-38.0000` | `2739.0000` | `409.0586` | `505.1799` | `572` | `42` |
| **WGM2012 Free-Air** (`mGal`) | `151×151` | `22,801 / 22,801` | `-201.9820` | `247.1230` | `-30.9997` | `63.1097` | `17,598` | `0` |
| **WGM2012 Isostatic** (`mGal`) | `151×151` | `22,801 / 22,801` | `-156.2230` | `144.7580` | `-14.1970` | `41.8220` | `14,349` | `0` |
| **Earth2014 TBI2014** (`m`) | `300×300` | `90,000 / 90,000` | `-34.0000` | `2805.0000` | `407.9203` | `502.4736` | `2,035` | `255` |

---

## 3. Coordinate Registration, Resolution & Vertical Datum Verification

- **WGM2012 Grids (all 4):**
  - Ascending `x` (`-180.0` to `180.0`, `10,801` nodes) and ascending `y` (`-90.0` to `90.0`, `5,401` nodes).
  - Node-registered at `2 arc-min` (`0.033333°`). Core subset spans exact endpoints `[22.0, 27.0]` $\times$ `[90.0, 95.0]`; buffer spans `[19.0, 30.0]` $\times$ `[87.0, 98.0]`.
  - Gravity anomalies reference the GRS80 ellipsoid; Bouguer uses spherical terrain correction ($\rho_c = 2670\text{ kg/m}^3$, $\rho_w = 1030\text{ kg/m}^3$); ETOPO1 represents elevation relative to Mean Sea Level (MSL).
- **Earth2014 TBI2014:**
  - Ascending `x` (`-179.991667` to `179.991667`, `21,600` pixels) and ascending `y` (`-89.991667` to `89.991667`, `10,800` pixels).
  - Pixel-registered at `1 arc-min` (`0.016667°`), stored as `int16` (`>i2`).
  - Represents Topography-Bathymetry-Ice orthometric height relative to the EGM2008 geoid / MSL. Because of its 1' resolution, pixel registration, and EGM2008 geoid reference, Earth2014 differs from 2' WGM2012 ETOPO1 (core max `2805 m` vs `2739 m`, core min `-34 m` vs `-38 m`). They are **not** assumed identical; WGM2012 ETOPO1 is co-registered with the WGM2012 gravity grids for consistent 2' forward gravity modeling, while Earth2014 provides 1' high-resolution topographic reference.

---

## 4. Identification of Marine Cells ($h < 0$)

Both topographic grids confirm that **marine/estuarine cells ($h < 0$) exist in both the core and buffered domains**:
- **Core (`22–27°N, 90–95°E`):** `572` cells (`2.51%`) in WGM2012 ETOPO1 (min `-38 m`) and `2,035` cells (`2.26%`) in Earth2014 TBI2014 (min `-34 m`), located in the Meghna estuary / northern Bay of Bengal (`22.0°–22.5°N, 90°–92°E`).
- **Buffer (`19–30°N, 87–98°E`):** `15,288` cells (`13.95%`) in WGM2012 ETOPO1 (min `-2296 m`) and `60,341` cells (`13.85%`) in Earth2014 TBI2014 (min `-2225 m`) across the Bay of Bengal.

**Phase 2 Safeguard:** Subaerial Airy and Pratt equations ($h \ge 0$) **must not** be applied to $h < 0$ cells. Phase 2 must implement separate, explicitly verified marine Airy (anti-root with seawater density $\rho_w = 1030\text{ kg/m}^3$) and marine Pratt equations for $h < 0$.

---

## 5. CRUST1.0 Fill-Value Repair & Verification

- **Root Cause:** In [`CRUST1.0`](file:///e:/northeast-india-isostasy/data/raw/seismic/CRUST1.0-vp.r0.1-n4c.nc), absent layers (such as `upper_sediments` at `(25.5°N, 94.5°E)` and `(23.5°N, 93.5°E)`) carry `thickness = 0.0` and `top = 9.96921e+36` (NetCDF fill value). The previous summary CSV did not mask `9.96921e+36` before extracting surface elevation.
- **Fix Applied:** [`src/data/crust1.py`](file:///e:/northeast-india-isostasy/src/data/crust1.py) loads the raw `CRUST1.0-{vp,vs,rho}.r0.1-n4c.nc` subdatasets via `rasterio`, masks `|val| >= 1e20` at the individual variable level, and extracts solid-Earth surface elevation from the shallowest present non-water, non-ice layer (`upper_crust_top` when sediments are absent).
- **Verified Corrected Values:**
  - `(25.5°N, 94.5°E)`: `surface_elevation_km = 1.35` (`1350.0 m`), `total_crustal_thickness_km = 42.0`, `moho_elevation_km = -40.65` (`1.35 - (-40.65) = 42.0`).
  - `(23.5°N, 93.5°E)`: `surface_elevation_km = 1.16` (`1160.0 m`), `total_crustal_thickness_km = 37.0`, `moho_elevation_km = -35.84` (`1.16 - (-35.84) = 37.0`).
- **Backup:** Previous CSV preserved at [`data/processed/seismic/crust1_study_area_summary.csv.bak`](file:///e:/northeast-india-isostasy/data/processed/seismic/crust1_study_area_summary.csv.bak).
