# CRUST1.0 Seismic Model: Data Acquisition and Metadata Validation Report

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Study Region:** Latitude 22°N–27°N, Longitude 90°E–95°E (Centre: 24.5°N, 92.5°E)  
**Date of Validation:** 2026-11-10  
**Horizontal Coordinate Reference System:** EPSG:4326 (WGS84)  
**Vertical Reference Datum:** Mean Sea Level (MSL, $0.0\text{ km}$)  

---

## 1. Executive Summary

This report documents the acquisition, structural validation, and spatial subsetting of the CRUST1.0 global seismic model (Laske et al., 2013) for the Northeast India study area. All three official component files (`vp`, `vs`, and `rho`) were successfully downloaded from EarthScope Earth Model Collaboration (EMC) archives and verified with SHA-256 checksums. 

A $5 \times 5$ cell subset ($22^\circ\text{–}27^\circ\text{N}, 90^\circ\text{–}95^\circ\text{E}$; cell centres $22.5^\circ\text{–}26.5^\circ\text{N}, 90.5^\circ\text{–}94.5^\circ\text{E}$) was extracted without vertical averaging, fully preserving the original 8-layer crustal and sediment stratification plus uppermost mantle lid.

---

## 2. Source Provenance and File Integrity

Official distribution files were retrieved from EarthScope Earth Model Collaboration (EMC) under the `EMC-CRUST1.0` product catalog.

* **Original Archive Host:** EarthScope Consortium (formerly IRIS Data Management Center)
* **Archive Base URL:** `https://data.earthscope.org/archive/seismology/products/emc/netcdf/`
* **Local Storage Directory:** `data/raw/seismic/`

### Downloaded Raw Files and Checksums

| Filename | Physical Quantity | Size (bytes) | SHA-256 Checksum | Validation Status |
| :--- | :--- | :--- | :--- | :--- |
| `CRUST1.0-vp.r0.1-n4c.nc` | Compressional velocity ($V_p$) | 1,256,446 | `e31d69405d51465555dd913c5b6bc9aec4f78249e01dcd653a3674af635dcdf6` | Intact / Verified |
| `CRUST1.0-vs.r0.1-n4c.nc` | Shear velocity ($V_s$) | 1,250,053 | `5ff0eb808e9d602b35766ff888e90cc4911d5421addfa941f10e22f2a184551e` | Intact / Verified |
| `CRUST1.0-rho.r0.1-n4c.nc` | Density ($\rho$) | 1,241,636 | `b9f3d5ce98a0e21ffb733fbead2fbbe8ba00340fc746977edd3b198dbed44411` | Intact / Verified |

---

## 3. Global Grid Coordinates and Geometry

Each global file contains 26 distinct subdatasets organized on an identical global grid:

* **Grid Dimensions:** 180 rows $\times$ 360 columns (total 64,800 cells globally).
* **Grid Spacing / Resolution:** $1.0^\circ \times 1.0^\circ$ (~$111\text{ km} \times 101\text{ km}$ at $24.5^\circ\text{N}$).
* **Grid Registration:** Pixel / cell-centred.
* **Coordinate Variables:**
  * `latitude`: Range $[+89.5^\circ, -89.5^\circ]$, descending with step size $-1.0^\circ$. Cell boundaries run from $+90.0^\circ$ to $-90.0^\circ$.
  * `longitude`: Range $[-179.5^\circ, +179.5^\circ]$, ascending with step size $+1.0^\circ$. Cell boundaries run from $-180.0^\circ$ to $+180.0^\circ$.
* **Missing Value (NoData) Representation:** `9.96921e+36` (standard NetCDF floating-point fill value).
* **Geodetic Datum:** WGS84 (EPSG:4326 horizontal coordinates).

---

## 4. Vertical Layer Architecture and Variable Definitions

CRUST1.0 decomposes the lithosphere into 8 distinct crustal/water/ice layers over an uppermost mantle half-space. 

### Layer Hierarchy (Surface to Mantle)

1. `water`: Ocean water column (thickness $0.0\text{ km}$ across the study area).
2. `ice`: Glacial ice cap (thickness $0.0\text{ km}$ across the study area).
3. `upper_sediments`: Unconsolidated upper sedimentary cover.
4. `middle_sediments`: Semi-consolidated middle sedimentary rocks.
5. `lower_sediments`: Consolidated / lithified deep sediments.
6. `upper_crust`: Upper crystalline crust (felsic/granitic composition).
7. `middle_crust`: Middle crystalline crust (intermediate composition).
8. `lower_crust`: Lower crystalline crust (mafic/granulitic composition).
9. `mantle`: Sub-Moho uppermost mantle lid (Pn/Sn velocity and uppermost mantle density).

### Subdataset Variable Schema

For each layer, three structural and physical parameters are provided:

| Variable Template | Description | Units | Coordinate / Reference |
| :--- | :--- | :--- | :--- |
| `<layer>_top` | Elevation of layer upper boundary | `km` | Relative to Mean Sea Level (positive up, negative down) |
| `<layer>_thickness` | Vertical thickness of layer | `km` | Positive scalar thickness ($\ge 0.0\text{ km}$) |
| `<layer>_vp` | Compressional wave velocity ($V_p$) | `km.s-1` | In situ velocity parameter |
| `<layer>_vs` | Shear wave velocity ($V_s$) | `km.s-1` | In situ velocity parameter |
| `<layer>_rho` | Mass density ($\rho$) | `g.cm-3` | Model-assigned bulk density (multiply by 1000 for $\text{kg/m}^3$) |

> **Crucial Scientific Distinction regarding Density:**  
> The density values in `CRUST1.0-rho.r0.1-n4c.nc` are **not** direct physical gravimetric or borehole core measurements. They are model-assigned bulk densities derived from empirical seismic velocity-to-density scaling relationships (e.g., Birch's law, Christensen and Mooney 1995, Brocher 2005) conditioned on regional crustal tectonic classifications. They must not be treated as independent observational truth in isostatic mass-balance testing.

---

## 5. Study Area Coverage and Verification

The target analysis area is bounded by $22^\circ\text{N}\text{–}27^\circ\text{N}$ and $90^\circ\text{E}\text{–}95^\circ\text{E}$.

### Extracted Grid Indices and Coordinates

| Dimension | Coordinate Range | Grid Indices | Cell Centres Sampled |
| :--- | :--- | :--- | :--- |
| **Latitude** | $22.0^\circ\text{N} \le \phi \le 27.0^\circ\text{N}$ | Rows `[63, 64, 65, 66, 67]` | $26.5^\circ\text{N}, 25.5^\circ\text{N}, 24.5^\circ\text{N}, 23.5^\circ\text{N}, 22.5^\circ\text{N}$ |
| **Longitude** | $90.0^\circ\text{E} \le \lambda \le 95.0^\circ\text{E}$ | Cols `[270, 271, 272, 273, 274]` | $90.5^\circ\text{E}, 91.5^\circ\text{E}, 92.5^\circ\text{E}, 93.5^\circ\text{E}, 94.5^\circ\text{E}$ |

Total cells: **25 cells** ($5 \times 5$ matrix).

### Data Completeness Check
- Missing values: **0** across all variables.
- Water thickness: **$0.00\text{ km}$** across all 25 cells (100% terrestrial/subaerial).
- Ice thickness: **$0.00\text{ km}$** across all 25 cells.
- Surface elevation range: $+0.015\text{ km}$ ($15\text{ m}$) in southern Bengal Basin to $+1.205\text{ km}$ ($1205\text{ m}$) in eastern Indo-Burma ranges.

### Key Physical Parameters across Study Area (25 Cells)

| Parameter | Minimum | Mean | Maximum | Unit |
| :--- | :--- | :--- | :--- | :--- |
| **Total Sediment Thickness** | $0.00$ | $4.42$ | $14.50$ | $\text{km}$ |
| **Crystalline Crust Thickness** | $22.50$ | $33.16$ | $36.00$ | $\text{km}$ |
| **Total Crustal Thickness ($T_c$)** | $35.00$ | $37.58$ | $42.00$ | $\text{km}$ |
| **Moho Elevation ($z_\text{Moho}$)** | $-41.87$ | $-37.40$ | $-34.84$ | $\text{km}$ (MSL) |
| **Moho Depth Below Sea Level ($D_\text{Moho}$)** | $34.84$ | $37.40$ | $41.87$ | $\text{km}$ |
| **Upper Crust Density** | $2.70$ | $2.72$ | $2.75$ | $\text{g/cm}^3$ |
| **Middle Crust Density** | $2.80$ | $2.82$ | $2.86$ | $\text{g/cm}^3$ |
| **Lower Crust Density** | $2.95$ | $3.01$ | $3.05$ | $\text{g/cm}^3$ |
| **Uppermost Mantle Density ($\rho_m$)** | $3.34$ ($3340$) | $3.38$ ($3382$) | $3.41$ ($3410$) | $\text{g/cm}^3$ ($\text{kg/m}^3$) |
| **Uppermost Mantle $V_p$** | $8.05$ | $8.15$ | $8.22$ | $\text{km/s}$ |

---

## 6. Processed Data Deliverables

The processed seismic deliverables are stored in `data/processed/seismic/`:

1. **`CRUST1.0_study_area_subset.nc`**
   - Self-contained NetCDF dataset containing all 44 variables for the $5 \times 5$ grid.
   - Contains exact layer tops, layer thicknesses, $V_p$, $V_s$, and density arrays.
   - No vertical averaging or layer collapse was applied.

2. **`crust1_study_area_layers.csv`**
   - Tabular record of 225 rows ($25\text{ cells} \times 9\text{ layers}$).
   - Columns: `latitude`, `longitude`, `layer`, `top_km`, `thickness_km`, `vp_kms`, `vs_kms`, `rho_gcm3`, `rho_kgm3`.
   - Allows straightforward SQL/Pandas querying of individual crustal layers.

3. **`crust1_study_area_summary.csv`**
   - Tabular summary of 25 rows (one per grid cell).
   - Columns include: `latitude`, `longitude`, `surface_elevation_km`, `total_sediment_thickness_km`, `crystalline_crust_thickness_km`, `total_crustal_thickness_km`, `moho_elevation_km`, `moho_depth_below_sl_km`, layer velocities, and uppermost mantle parameters.

4. **Diagnostic Cartographic Map**
   - Path: `results/maps/crust1_study_area_moho_thickness.png`
   - High-resolution side-by-side visualization showing CRUST1.0 Moho Depth below Sea Level and Total Crustal Thickness ($T_c$) across the study region with individual cell values annotated.

---

## 7. Scientific Limitations and Cautions for Isostasy Modelling

1. **Spatial Smoothing:**
   A spatial grid spacing of $1^\circ \times 1^\circ$ (~$100\text{ km}$) cannot resolve abrupt crustal transitions known to occur in Northeast India, such as the steep southern bounding fault of the Shillong Plateau (Dauki Fault) or the narrow Brahmaputra alluvium graben (~$50\text{–}80\text{ km}$ wide).
2. **Sediment–Basement Tradeoff:**
   Extreme sediment accumulations in the southern cells ($14.5\text{ km}$ in the Bengal foredeep) severely depress the basement. When comparing Airy isostatic root calculations with CRUST1.0 Moho, the large negative density contrast of sediments must be accounted for (sediment stripping / decompaction correction), otherwise Airy predictions based solely on surface topography will systematically underestimate the depth of compensation in deep sedimentary basins.
3. **Reference Model Only:**
   CRUST1.0 provides an essential regional baseline and starting model. However, local seismic receiver function studies (e.g., Mitra et al., 2005, 2018; Kumar et al., 2004; Borah et al., 2016) should be integrated during seismic validation stages to capture short-wavelength Moho undulations.

---

## 8. Verification Sign-Off

- [x] Raw source files downloaded intact and SHA-256 verified.
- [x] Grid coordinates, layer schema, units, and missing value conventions fully documented.
- [x] Full study area coverage verified without missing cells or unphysical values.
- [x] Subsets exported preserving complete vertical layer stratigraphy.
- [x] Diagnostic cartographic visualization generated and verified.
- [x] No modeling, regression, or parameter tuning executed ahead of user instruction.
