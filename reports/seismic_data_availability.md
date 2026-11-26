# Seismic Data Availability & Suitability Investigation
**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Study Region:** 22.0°N–27.0°N, 90.0°E–95.0°E (Centre: 24.5°N, 92.5°E; Horizontal CRS: EPSG:4326)  
**Report Date:** 2026-11-10  
**Status:** Pre-download Data Source Investigation (Read-Only)

---

## 1. Executive Summary & Purpose

This report investigates available global and regional seismological datasets to support the **Northeast India Airy–Pratt Isostasy Analysis**. The primary objectives are:
1. To obtain observational **crustal thickness ($T_c$)** and **Moho depth ($D_{\text{Moho}}$)** against which theoretical Airy and Pratt isostatic root predictions can be quantitatively validated.
2. To compile **seismic velocities ($V_p, V_s$)** and **velocity ratios ($V_p/V_s$)** across crustal layers to constrain Pratt compensation models (lateral density variations) and evaluate crustal composition.
3. To determine whether **density ($\rho$)** is directly provided, model-derived, or requires estimation via empirical velocity-to-density scaling laws.
4. To establish vertical datum conventions, spatial coverage limitations, and data accessibility across global gridded models and regional receiver-function studies.

---

## 2. Global Model: CRUST1.0

### 2.1 Overview & Data Provenance
* **Model Name:** CRUST1.0 (A 1-degree Global Model of Earth's Crust)
* **Authors:** Gabi Laske, Guy Masters, Zhitu Ma, and Michael Pasyanos (2013)
* **Citation:** Laske, G., Masters, G., Ma, Z., and Pasyanos, M. (2013), *Update on CRUST1.0 - A 1-degree Global Model of Earth's Crust*, Geophys. Res. Abstracts, 15, Abstract EGU2013-2658.
* **Official Primary Repository:** [UC San Diego IGPP CRUST1.0 Portal](https://igppweb.ucsd.edu/~gabi/crust1.html)
* **Standardized Repository:** [EarthScope Earth Model Collaboration (EMC)](https://data.earthscope.org/app/products/portal/#/models/global/CRUST1.0)

### 2.2 Model Architecture & Layering
CRUST1.0 discretizes the crust into an 8-layer vertical column for every $1^\circ \times 1^\circ$ cell, plus the uppermost mantle directly below the Moho:
1. Water (layer 1)
2. Ice (layer 2)
3. Upper sediments (layer 3)
4. Middle sediments (layer 4)
5. Lower sediments (layer 5)
6. Upper crystalline crust (layer 6)
7. Middle crystalline crust (layer 7)
8. Lower crystalline crust (layer 8)
9. Sub-Moho mantle ($P_n, S_n$)

For every layer, the model provides layer boundary depths ($z_{\text{top}}, z_{\text{bottom}}$), compressional wave velocity ($V_p$), shear wave velocity ($V_s$), and bulk density ($\rho$).

### 2.3 Investigation of EarthScope NetCDF Files
EarthScope EMC provides standardized NetCDF-4 Classic (`-n4c.nc`) files for CRUST1.0:

| File Identifier | Parameter | Units | Direct Official Download Link |
| :--- | :--- | :--- | :--- |
| **`CRUST1.0-vp.r0.1-n4c.nc`** | Compressional Velocity ($V_p$) | $\text{km/s}$ | [`https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-vp.r0.1-n4c.nc`](https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-vp.r0.1-n4c.nc) |
| **`CRUST1.0-vs.r0.1-n4c.nc`** | Shear Velocity ($V_s$) | $\text{km/s}$ | [`https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-vs.r0.1-n4c.nc`](https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-vs.r0.1-n4c.nc) |
| **`CRUST1.0-rho.r0.1-n4c.nc`** | Bulk Density ($\rho$) | $\text{g/cm}^3$ | [`https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-rho.r0.1-n4c.nc`](https://data.earthscope.org/products/emc/CRUST1.0/model/CRUST1.0-rho.r0.1-n4c.nc) |

*Alternative Direct ASCII Files (from UCSD IGPP):*
* Total Crustal Thickness (excluding water): [`https://igppweb.ucsd.edu/~gabi/crust1/crsthk.xyz.zip`](https://igppweb.ucsd.edu/~gabi/crust1/crsthk.xyz.zip)
* Depth to Moho below Sea Level: [`https://igppweb.ucsd.edu/~gabi/crust1/depthtomoho.xyz.zip`](https://igppweb.ucsd.edu/~gabi/crust1/depthtomoho.xyz.zip)
* Total Sediment Thickness: [`https://igppweb.ucsd.edu/~gabi/crust1/sedthk.xyz.zip`](https://igppweb.ucsd.edu/~gabi/crust1/sedthk.xyz.zip)
* Full Model Tarball: [`https://igppweb.ucsd.edu/~gabi/crust1/crust1.0.tar.gz`](https://igppweb.ucsd.edu/~gabi/crust1/crust1.0.tar.gz)

### 2.4 Spatial Coverage & Resolution Evaluation for the Study Area
* **Spatial Resolution:** $1.0^\circ \times 1.0^\circ$ ($\approx 111\text{ km} \times 101\text{ km}$ at 24.5°N).
* **Grid Coverage in Study Window (22°N–27°N, 90°E–95°E):**
  * Cell centers fall at half-degree offsets:
    * Latitudes: $22.5^\circ\text{N}, 23.5^\circ\text{N}, 24.5^\circ\text{N}, 25.5^\circ\text{N}, 26.5^\circ\text{N}$ (5 rows)
    * Longitudes: $90.5^\circ\text{E}, 91.5^\circ\text{E}, 92.5^\circ\text{E}, 93.5^\circ\text{E}, 94.5^\circ\text{E}$ (5 columns)
  * Total sample points inside the core 5° × 5° box: **Exactly 25 grid cells**.
* **Vertical Reference & Depth Convention:**
  * Topographic surface datum: Derived from ETOPO1, averaged into 1° cells.
  * `depthtomoho`: Positive-downward depth **relative to Mean Sea Level (MSL)**.
  * `crsthk`: Total vertical distance **from local surface down to Moho** (crustal thickness, excluding water column).
  * Layer boundaries are referenced negative-downward relative to sea level.

### 2.5 Critical Limitations of CRUST1.0 for This Study
1. **Severe Spatial Smoothing:** A single 1° cell covers $\approx 11,200\text{ km}^2$. The Shillong Plateau is only $\approx 80\text{ km}$ wide north-to-south, and the Brahmaputra Valley is $\approx 50\text{–}80\text{ km}$ wide. A 1° grid cell smears the high-elevation cratonic plateau, the deep alluvial valley, and the Himalayan frontal fault into single averaged values.
2. **Model-Derived Densities:** Densities in CRUST1.0 are **not directly measured**. They are assigned based on statistical crustal types tied to tectonic province age (Artemieva & Mooney) and laboratory empirical velocity-to-density curves (e.g., Christensen & Mooney, 1995; Brocher, 2005).

---

## 3. Regional Seismic Studies & Datasets

Four key peer-reviewed regional seismological studies covering Northeast India were investigated:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ REGIONAL SEISMIC STUDIES IN NORTHEAST INDIA (Station-Level Receiver Functions)        │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Study                    │ Lead Authors / Year      │ Primary Focus                    │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 1. GJI (2021)            │ Agrawal et al. (2021)    │ Joint RF & Surface Waves (Vs)    │
│ 2. JGR Solid Earth (2018)│ Mitra et al. (2018)      │ RF & Gravity (Tc, Moho, Vp/Vs)   │
│ 3. PEPI (2016)           │ Borah et al. (2016)      │ H-k Stacking & NA Inversion (Vs) │
│ 4. Geol. Journal (2022)  │ Shukla et al. (2022)     │ H-k Stacking (Tc, Poisson ratio) │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

### 3.1 Study 1: Agrawal et al. (2021) — Joint Receiver Functions & Dispersion

* **Full Title:** *Mapping lithospheric seismic structure beneath the Shillong plateau (India) and adjoining regions by jointly fitting receiver functions and surface wave dispersion*
* **Authors:** Mohit Agrawal, Mukesh Kumar Das, Sachin Kumar, and Jay Pulliam
* **Journal:** *Geophysical Journal International*, 226(3), 1645–1675.
* **DOI:** [10.1093/gji/ggab146](https://doi.org/10.1093/gji/ggab146)
* **Official Article Link:** [`https://academic.oup.com/gji/article/226/3/1645/6274677`](https://academic.oup.com/gji/article/226/3/1645/6274677)

#### Technical Findings:
1. **Parameters Provided:**
   * Station-level crustal thickness ($H$).
   * 1D depth-dependent shear wave velocity profiles ($V_s(z)$ from surface to $100\text{ km}$ depth).
   * Sediment layer thickness and shear velocity ($V_{s,\text{sed}}$).
   * Bulk crustal $V_p/V_s$ ratios.
   * Moho transition sharpness/gradient.
2. **Spatial Coverage & Resolution:**
   * 18 broadband seismic stations deployed across the Shillong Plateau, Brahmaputra Valley, and Mikir Hills.
   * Irregular station spacing ranging from $25\text{ to }70\text{ km}$.
   * Stations lie almost entirely within Indian territory ($24.5^\circ\text{–}27.0^\circ\text{N}$, $90.5^\circ\text{–}94.5^\circ\text{E}$).
3. **Vertical Resolution & Reference:**
   * Receiver function + dispersion joint inversion resolves vertical layer velocity gradients down to $\sim 1\text{–}2\text{ km}$ in the upper crust and $\sim 2\text{–}4\text{ km}$ at Moho depths.
   * **Reference Datum:** Depths ($H$) are measured **positive downward from the station elevation** (local surface), **not** sea level.
4. **Data Availability:**
   * **Continuous Gridded Model:** Not available as a continuous grid.
   * **Tabular Station Data:** Station coordinates, instruments, and estimated crustal thickness values are published in **Table 1** and the **Online Supplementary Material** (`ggab146_supplementary_data`).

---

### 3.2 Study 2: Mitra et al. (2018) — Eastern Himalayan Plate Boundary

* **Full Title:** *Crustal Structure and Evolution of the Eastern Himalayan Plate Boundary System, Northeast India*
* **Authors:** Supriyo Mitra, Keith Priestley, Kajaljyoti Borah, and Vinod K. Gaur
* **Journal:** *Journal of Geophysical Research: Solid Earth*, 123(1), 621–640.
* **DOI:** [10.1002/2017JB014714](https://doi.org/10.1002/2017JB014714)
* **Official Article Link:** [`https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JB014714`](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JB014714)

#### Technical Findings:
1. **Parameters Provided:**
   * Crustal thickness ($H$) beneath individual broadband stations.
   * Bulk crustal $V_p/V_s$ ratio.
   * 2D forward-modeled density and Moho profiles integrated with Bouguer gravity.
   * Inferred crustal composition (felsic vs. intermediate/mafic).
2. **Key Findings for Our Region:**
   * Shillong Plateau & Mikir Hills: Thin, felsic crust ($T_c \approx 30\text{–}35\text{ km}$; $V_p/V_s \approx 1.70\text{–}1.75$).
   * Brahmaputra Valley: Moderate crustal thickness ($T_c \approx 36\text{–}40\text{ km}$; $V_p/V_s \approx 1.75\text{–}1.80$).
   * Northern Bengal Basin: Transitional/rifted crust beneath thick sediments ($T_c \approx 32\text{–}36\text{ km}$).
   * Himalayan Foothills / Frontal Belt: Deepening crust ($T_c > 45\text{–}50\text{ km}$).
3. **Vertical Reference:**
   * Receiver function delay times are measured relative to the station surface; crustal thickness $H$ represents **depth below station surface**.
4. **Data Availability:**
   * Station coordinates, Moho depths, and error bars are provided in **Table 1** of the manuscript. Supplementary material S1 contains individual $H$-$\kappa$ stacking curves. No downloadable NetCDF raster is provided.

---

### 3.3 Study 3: Borah et al. (2016) — PEPI Receiver Function Modeling

* **Full Title:** *Crustal structure beneath northeast India inferred from receiver function modeling*
* **Authors:** Kajaljyoti Borah, Dipok K. Bora, Ayush Goyal, and Raju Kumar
* **Journal:** *Physics of the Earth and Planetary Interiors*, 258, 15–27.
* **DOI:** [10.1016/j.pepi.2016.06.009](https://doi.org/10.1016/j.pepi.2016.06.009)
* **Official Article Link:** [`https://www.sciencedirect.com/science/article/abs/pii/S0031920116300292`](https://www.sciencedirect.com/science/article/abs/pii/S0031920116300292)

#### Technical Findings:
1. **Parameters Provided:**
   * Crustal thickness ($H$).
   * Bulk $V_p/V_s$ and Poisson's ratio ($\nu$).
   * Low-velocity surface sediment layer thickness ($h_{\text{sed}}$) and sediment shear velocity ($V_{s,\text{sed}}$).
   * 1D crustal shear wave velocity structure ($V_s(z)$) derived via the Neighbourhood Algorithm (NA).
2. **Spatial Coverage:**
   * 10 broadband stations distributed across the Shillong Plateau, Assam Valley, and Lesser Himalaya.
3. **Data Availability:**
   * Station results are tabulated directly in **Table 1 and Table 2** of the paper.

---

### 3.4 Study 4: Shukla et al. (2022) — Geological Journal Spatial Analysis

* **Full Title:** *Spatial variations of crustal thickness and Poisson's ratio in the northeastern region of India based on receiver function analysis*
* **Authors:** Neeharika Shukla, Devajit Hazarika, Abhishek Kundu, and Sagarika Mukhopadhyay
* **Journal:** *Geological Journal*, 57(9), 3624–3639.
* **DOI:** [10.1002/gj.4469](https://doi.org/10.1002/gj.4469)
* **Official Article Link:** [`https://onlinelibrary.wiley.com/doi/full/10.1002/gj.4469`](https://onlinelibrary.wiley.com/doi/full/10.1002/gj.4469)

#### Technical Findings:
1. **Parameters Provided:**
   * Crustal thickness ($H$) with confidence intervals ($\pm \sigma$).
   * $V_p/V_s$ ratio and Poisson's ratio ($\nu$).
   * Regional contour maps of crustal thickness and Poisson's ratio across Northeast India.
2. **Spatial Coverage:**
   * 19 broadband seismic stations operated by the Wadia Institute of Himalayan Geology (WIHG), National Center for Seismology (NCS), and regional networks.
   * Stations span from the Bengal Basin margin ($22.5^\circ\text{N}$) to the Arunachal Higher Himalaya ($27.5^\circ\text{N}$), and from $90.5^\circ\text{E}$ to $95.5^\circ\text{E}$.
3. **Key Observations:**
   * Thinnest crust observed beneath the Shillong Plateau ($32.0\text{–}36.0\text{ km}$) and northern Bengal Basin margin ($34.0\text{–}37.0\text{ km}$).
   * Intermediate crust beneath the Brahmaputra Valley ($36.5\text{–}41.0\text{ km}$).
   * Thickest crust beneath the Indo-Burma Ranges ($42.0\text{–}52.0\text{ km}$) and Himalayan collision front ($45.0\text{–}54.0\text{ km}$).
4. **Data Availability:**
   * The station parameters are reported in **Table 1** of the publication. The spatial contour maps in the paper are interpolated illustrations, **not downloadable numerical GIS grids**.

---

## 4. Scientific Evaluation & Synthesis

### 4.1 Global Gridded Model vs. Regional Station Networks

```text
CRUST1.0 (Global 1° Grid)                   Regional RF Studies (Station Points)
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│ • Continuous 1° grid coverage   │         │ • High-resolution local accuracy│
│ • Full 5° × 5° spatial window   │   vs.   │ • Directly observed converted Ps│
│ • But: Severe spatial smoothing │         │ • But: Irregular station sparse │
│   (only 25 cells in study area) │         │ • Clustered on Indian territory │
│ • Model-derived densities       │         │ • Zero coverage in Bangladesh   │
└─────────────────────────────────┘         └─────────────────────────────────┘
```

1. **Resolution Mismatch**:
   * CRUST1.0's 1° resolution ($\sim 111\text{ km}$) is far too coarse to resolve the horst-and-graben geometry of the Shillong Plateau, Dauki Fault scarp, and narrow Brahmaputra Valley.
   * Regional receiver functions provide localized vertical resolution ($< 1\text{ km}$) beneath the station piercing points, making them the only reliable ground-truth for actual Moho depth.
2. **Spatial Incompleteness of Regional Studies**:
   * The regional seismic networks are strictly confined to India.
   * The southwest quadrant of our study region ($22^\circ\text{–}25^\circ\text{N}, 90^\circ\text{–}92^\circ\text{E}$) comprises sovereign territory of **Bangladesh** (Bengal Basin / Surma Basin), where no stations from these 4 studies are located.
   * The eastern edge ($94.5^\circ\text{–}95.0^\circ\text{E}$) touches western **Myanmar** (Chin State), which also lacks dense academic station coverage in these datasets.

---

### 4.2 Velocity-to-Density Empirical Scaling Laws

**Crucial Scientific Distinction:**  
The $V_p/V_s$ ratio (and associated Poisson's ratio $\nu$) is a dimensionless kinematic parameter diagnostic of lithology and fluid state:

$$\nu = \frac{1}{2} \left[ \frac{(V_p/V_s)^2 - 2}{(V_p/V_s)^2 - 1} \right]$$

**$V_p/V_s$ is NOT density.**

To estimate crustal density ($\rho$) from seismic velocity ($V_p$), geophysicists must rely on empirical laboratory scaling laws. The three primary relationships relevant to continental crust are:

#### 1. Brocher's Empirical Law (Brocher, 2005)
Compiled by the USGS from extensive laboratory ultrasonic measurements:

$$\rho = 1.6612 V_p - 0.4721 V_p^2 + 0.0671 V_p^3 - 0.0043 V_p^4 + 0.000106 V_p^5 \quad (\text{g/cm}^3)$$

* *Limitations:* Valid for typical crystalline rocks ($V_p = 1.5\text{–}8.5\text{ km/s}$). However, it has an intrinsic scatter of $\pm 0.10\text{–}0.15\text{ g/cm}^3$ ($\pm 100\text{–}150\text{ kg/m}^3$) and fails in calcium-rich rocks, serpentinites, and high-porosity unconsolidated sediments.

#### 2. Christensen & Mooney's Linear Regression (Christensen & Mooney, 1995)
Empirical relation based on continental crustal rocks at $20\text{ km}$ equivalent pressure ($600\text{ MPa}$):

$$\rho = 0.541 + 0.3601 V_p \quad (\text{g/cm}^3, \text{ with } V_p \text{ in km/s})$$

* *Limitations:* Derived for average crystalline basement; overestimates density in fractured upper crust and underestimates density in mafic granulites.

#### 3. Birch's Law (Birch, 1961)
Linear relationship for rocks of constant mean atomic weight ($\bar{m} \approx 21$):

$$\rho = a(\bar{m}) + b \cdot V_p$$

* *Limitations:* Highly sensitive to mineral composition and iron content ($\bar{m}$ varies from 20 for felsic granites to $>22$ for mafic/ultramafic rocks).

---

### 4.3 Vertical Datum & Reference Harmonization

* **Receiver Function Convention:**
  Receiver functions measure the relative travel-time delay of the $P$-to-$s$ converted phase at the Moho boundary beneath the seismometer:
  $$t_{Ps} - t_P = \int_{-H}^0 \left( \sqrt{V_s(z)^{-2} - p^2} - \sqrt{V_p(z)^{-2} - p^2} \right) dz$$
  Therefore, the reported value $H$ is the **total vertical crustal thickness measured from the local station elevation ($h_{\text{station}}$)**.
* **Harmonization to Sea Level:**
  To validate sea-level-referenced Moho depths ($D_{\text{Moho},\text{SL}}$) or Moho elevations ($z_{\text{Moho}}$) predicted by our Airy models:
  $$D_{\text{Moho},\text{SL}}(x_i, y_i) = H(x_i, y_i) - h_{\text{station}}(x_i, y_i)$$
  $$z_{\text{Moho}}(x_i, y_i) = h_{\text{station}}(x_i, y_i) - H(x_i, y_i) = -D_{\text{Moho},\text{SL}}(x_i, y_i)$$

> [!IMPORTANT]
> Because stations on the Shillong Plateau sit at elevations of $1000\text{ to }1960\text{ m}$, neglecting station elevation introduces an immediate systematic bias of $1\text{ to }2\text{ km}$ in Moho depth residuals!

---

## 5. Comprehensive Dataset Comparison Table

| Dataset / Study | Type | Spatial Coverage | Spatial Resolution | Parameters Provided | Directly Downloadable? | Primary Format | Key Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CRUST1.0** (Laske et al., 2013) | Global Gridded Model | Global ($100\%$ of study window) | $1.0^\circ \times 1.0^\circ$ ($25$ cells in 5°×5°) | $V_p, V_s, \rho, T_c, D_{\text{Moho}}$, 8-layer boundaries | **Yes** (UCSD & EarthScope EMC) | NetCDF-4 (`.nc`), ASCII XYZ | Resolution too coarse for local tectonic horsts; model-assigned densities. |
| **Agrawal et al. (2021)** | Regional Joint Inversion | Shillong Plateau & Assam Valley | 18 broadband stations ($25\text{–}70\text{ km}$ spacing) | $H, V_p/V_s, V_s(z)$ profiles, sediment $h_{\text{sed}}$ | **Yes (Tabular)** | Published Table 1 & Supplementary text | Station points only; no stations in Bangladesh/Myanmar. |
| **Mitra et al. (2018)** | Regional Receiver Function & Gravity | Shillong, Mikir Hills, Assam Valley | ~20 broadband stations | $H, V_p/V_s$, 2D gravity-modeled crustal density | **Yes (Tabular)** | Published Table 1 & Supp. S1 | Irregular station distribution; proprietary journal paywall. |
| **Borah et al. (2016)** | Regional RF Modeling (PEPI) | Shillong, Assam, Lesser Himalaya | 10 broadband stations | $H, V_p/V_s, V_s(z)$ (Neighbourhood Algorithm) | **Yes (Tabular)** | Published Tables 1 & 2 | Small station count (10); sparse coverage. |
| **Shukla et al. (2022)** | Regional Receiver Function (GJ) | NE India (Bengal margin to Himalaya) | 19 broadband stations | $H, V_p/V_s$, Poisson ratio ($\nu$), error margins | **Yes (Tabular)** | Published Table 1 | Maps are graphical illustrations only; station tables require extraction. |

---

## 6. Synthesis & Final Recommendations

Because no single dataset provides continuous, high-resolution coverage with directly measured velocities and densities across the entire 5° × 5° transboundary region, a multi-tiered integration strategy is recommended:

### 1. Best Source for Primary Ground-Truth Crustal Thickness ($T_c$)
* **Recommendation:** **Harmonized Compilation of Station Receiver-Function Tables** (synthesizing Shukla et al., 2022; Mitra et al., 2018; Agrawal et al., 2021; Borah et al., 2016).
* **Rationale:** Direct $P$-to-$s$ converted phase arrivals provide true localized crustal thickness with uncertainties of $\pm 1.5\text{–}2.5\text{ km}$. Digitizing and compiling these ~30 distinct broadband station locations into a clean project table (`data/processed/seismic_stations_moho.csv`) yields high-precision validation points across the Shillong Plateau, Mikir Hills, Assam Valley, and Indo-Burma frontal belt.

### 2. Best Source for Seismic Velocities ($V_p$ and $V_s$)
* **Recommendation:**
  * **For 1D/Layered $V_s$ Profiles:** **Agrawal et al. (2021)** and **Borah et al. (2016)**, which used non-linear joint inversion with Rayleigh surface wave dispersion to resolve depth-dependent shear velocity $V_s(z)$.
  * **For Bulk Crustal $V_p/V_s$:** **Mitra et al. (2018)** and **Shukla et al. (2022)** (via robust $H$-$\kappa$ stacking).
  * **For Gridded Baseline:** **EarthScope EMC CRUST1.0 NetCDF files** (`CRUST1.0-vp.r0.1-n4c.nc` and `CRUST1.0-vs.r0.1-n4c.nc`) as a regional background framework, recognizing its 1° spatial smoothing.

### 3. Best Source for Crustal Density ($\rho$)
* **Recommendation:** **Pratt Density Modeling constrained by Brocher (2005) / Christensen & Mooney (1995) Velocity Conversions & Mitra et al. (2018) Gravity-Seismic Profiles**.
* **Rationale:** Direct physical density measurements do not exist continuously across the lithosphere. CRUST1.0 provides pre-computed densities, but they are generic model assignments. Calculating densities from regional $V_p$ using Brocher's polynomial scaling provides a physically grounded, data-driven density structure for Pratt isostatic analysis.

### 4. Best Independent Validation Dataset
* **Recommendation:** **Station Moho compilation (Shukla et al., 2022 + Mitra et al., 2018) referenced to sea level** ($D_{\text{Moho},\text{SL}} = H - h_{\text{station}}$).
* **Rationale:** Evaluating predicted Airy roots against these point measurements prevents false validation caused by gridded interpolation artifacts and provides unambiguous ground-truth comparisons across contrasting tectonic blocks.

---

## 7. Next Steps & Data Ingestion Roadmap

1. **Station Table Extraction (No Raw Raster Downloads Needed)**:
   * Collate station metadata (Code, Lat, Lon, Station Elevation, $H$, $\pm\sigma$, $V_p/V_s$) from the published tables of Mitra et al. (2018), Shukla et al. (2022), Agrawal et al. (2021), and Borah et al. (2016) into an auditable CSV table in `data/processed/`.
2. **CRUST1.0 Ingestion**:
   * If approved, download `CRUST1.0-vp.r0.1-n4c.nc`, `CRUST1.0-vs.r0.1-n4c.nc`, and `CRUST1.0-rho.r0.1-n4c.nc` from EarthScope EMC to establish regional 1° background grids.
3. **Sediment & Water Correction Protocol**:
   * Utilize CRUST1.0 sediment thickness (`sedthk.xyz`) or regional estimates to isolate the sediment gravity deficit in the Bengal Basin during isostatic residual analysis.
