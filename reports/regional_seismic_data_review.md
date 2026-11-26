# Regional Seismic Observations for Northeast India: Audited Receiver-Function Baseline and CRUST1.0 Comparison

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Study Region:** Latitude 22°N–27°N, Longitude 90°E–95°E (Centre: 24.5°N, 92.5°E)  
**Date:** 2026-11-10  
**Horizontal CRS:** EPSG:4326 (WGS84)  
**Vertical Datum:** Mean Sea Level (MSL, $0.0\text{ km}$)  

---

## 1. Executive Summary and Scientific Purpose

This report provides a comprehensive scientific audit, harmonization, and validation review of published regional receiver-function (RF) seismic datasets across Northeast India. The primary purpose is to establish an empirical station-level Moho depth and crustal velocity baseline to evaluate theoretical Airy and Pratt isostatic compensation models, and to test the fidelity of the global $1^\circ \times 1^\circ$ CRUST1.0 model across this tectonically complex region.

Three benchmark peer-reviewed seismological investigations form the foundation of this regional baseline:
1. **Study A:** Agrawal, Das, Kumar, & Pulliam (2021), *Geophysical Journal International* (GJI), DOI: [10.1093/gji/ggab146](https://doi.org/10.1093/gji/ggab146).
2. **Study B:** Mitra, Priestley, Borah, & Gaur (2018), *Journal of Geophysical Research: Solid Earth* (JGR), DOI: [10.1002/2017JB014714](https://doi.org/10.1002/2017JB014714).
3. **Study C:** Borah, Bora, Goyal, & Kumar (2016), *Physics of the Earth and Planetary Interiors* (PEPI), DOI: [10.1016/j.pepi.2016.07.005](https://doi.org/10.1016/j.pepi.2016.07.005).

A total of **25 seismic observation records** have been audited and compiled into [`data/processed/seismic/regional_receiver_function_stations.csv`](file:///e:/northeast-india-isostasy/data/processed/seismic/regional_receiver_function_stations.csv). Within our core study window ($22^\circ\text{–}27^\circ\text{N}$, $90^\circ\text{–}95^\circ\text{E}$), there are **23 observation records** representing **21 unique physical seismological stations** (with the permanent station `SHL` observed across all three studies). Two additional stations (`DHUB` at $89.98^\circ\text{E}$ and `RUP` at $27.20^\circ\text{N}$) provide regional tectonic context immediately outside the boundary.

---

## 2. Comprehensive Scientific Correction Log

Following an exhaustive audit of the primary publications against earlier preliminary summaries, significant numerical, methodological, and attribution errors were identified and resolved. Table 2.1 details every discrepancy, its original published source, and the exact correction applied.

### Table 2.1: Scientific Audit and Correction Log

| Station / Parameter | Previous Erroneous Entry | Audited Published Value | Primary Source Reference | Nature and Rationale of Correction |
| :--- | :--- | :--- | :--- | :--- |
| **JOWA** (Agrawal et al. 2021) | Moho: $35.0\text{ km}$ (VFSA) | $H_{\text{joint}} = 28.9 \pm 1.4\text{ km}$<br>$H_{\kappa} = 29.1\text{ km}$, $\kappa = 1.74$ | Table 3 (Joint Model)<br>Table 2 ($H-\kappa$) | Corrected major error ($6.1\text{ km}$ shallower). Separated joint-inversion Moho from preliminary $H-\kappa$ stack. Preferred: $28.9 \pm 1.4\text{ km}$. |
| **KHLI** (Agrawal et al. 2021) | Moho: $35.5\text{ km}$ (VFSA) | $H_{\text{joint}} = 32.0 \pm 1.6\text{ km}$<br>$H_{\kappa} = 31.8\text{ km}$, $\kappa = 1.71$ | Table 3 (Joint Model)<br>Table 2 ($H-\kappa$) | Corrected error ($3.5\text{ km}$ shallower). Joint model preferred from Table 3. |
| **MAWK** (Agrawal et al. 2021) | Moho: $35.6\text{ km}$ (VFSA) | $H_{\text{joint}} = 32.5 \pm 1.6\text{ km}$<br>$H_{\kappa} = 32.3\text{ km}$, $\kappa = 1.69$ | Table 3 (Joint Model)<br>Table 2 ($H-\kappa$) | Corrected error ($3.1\text{ km}$ shallower). Separated joint model from $H-\kappa$ stack ($\kappa=1.69$ is regional minimum). |
| **SHL** (Agrawal et al. 2021) | Moho: $35.0\text{ km}$ | $H_{\text{joint}} = 33.0 \pm 1.5\text{ km}$<br>$H_{\kappa} = 33.0\text{ km}$, $\kappa = 1.73$ | Table 2 & Table 3 text | Replaced discussion estimate with published table value ($33.0\text{ km}$). |
| **KOHI** (Agrawal et al. 2021) | Moho: $41.5\text{ km}$ (Joint) | $H_{\kappa} = 45.0 \pm 2.0\text{ km}$, $\kappa = 1.82$<br>$H_{\text{joint}} = \text{NaN}$ | Table 2 ($H-\kappa$) | Corrected Moho depth to published Table 2 value ($45.0\text{ km}$). Joint 1D profile only in figures, no numerical table; marked joint depth as NaN. |
| **DHUB** (Agrawal et al. 2021) | Study Area: Core ($90.00^\circ\text{E}$) | $H_{\kappa} = 37.0 \pm 2.0\text{ km}$, $\kappa = 1.78$<br>Lon: $89.98^\circ\text{E}$ | Table 1 & Table 2 | Longitude $89.98^\circ\text{E}$ is $0.02^\circ$ west of core boundary ($90^\circ\text{E}$). Flagged as regional context (`in_core_study_area = False`). |
| **Mitra et al. (2018) Inventory** | 4 stations reported | 24 deployed stations;<br>8 quantitative stations | Table 1 (Deployment)<br>Table S1 & Priestley '19 | Audited full deployment. Standard $H-\kappa$ failed in Bengal Basin due to sediment resonance. Extracted 8 stations with rigorous Moho constraints (`BPN`, `BORJ`, `BAI`, `BNGN`, `SHL`, `AGT`, `AZL`, `BELO`). |
| **Borah et al. (2016) Dataset** | Mixed parameters | 10 network stations + 1 regional (`RUP`) | Table 1 ($H-V_p/V_s$)<br>Table 2 (NA Inversion) | Verified all coordinates, elevations, layer thicknesses, and velocities. Primary values taken from Table 2 Neighbourhood Algorithm inversion. |
| **Residual Averaging** | Mean $\Delta T_c = -1.13\text{ km}$ over 22 raw rows | Deduplicated unique stations:<br>Mean $\Delta T_c = -1.51\text{ km}$ ($N=21$) | Harmonized spatial statistics | Discarded unverified raw averaging that double-counted repeated stations (`SHL` $\times 3$). Statistics now computed strictly across unique primary benchmark stations. |
| **Crustal Density** | $V_p/V_s$ labeled as density proxy | Density: "Not Provided" | Receiver function theory | Removed misleading statements. Receiver functions do NOT measure mass density; marked explicitly as unavailable in empirical tables. |

---

## 3. In-Depth Review of the Three Target Publications

### 3.1 Study A: Agrawal et al. (2021) — Shillong Plateau & Surrounding Regions
* **Citation:** Agrawal, M., Das, M. K., Kumar, S., & Pulliam, J. (2021). Mapping lithospheric seismic structure beneath the Shillong plateau (India) and adjoining regions by jointly fitting receiver functions and surface wave dispersion. *Geophysical Journal International*, 226(3), 1645–1675. DOI: [10.1093/gji/ggab146](https://doi.org/10.1093/gji/ggab146).
* **Network & Deployment:** Nine broadband stations: three temporary stations installed by IIT (ISM) Dhanbad (`JOWA`, `KHLI`, `MAWK`) operating from December 2018 to June 2020 equipped with Trillium Compact 120s sensors; and permanent NCS stations (`SHL`, `DHUB`, `KOHI`, `GUWA`, `TEZP`, `SILC`).
* **Methodology:** Teleseismic $P$-wave receiver functions (PRF), $S$-wave receiver functions (SRF), and fundamental-mode Rayleigh wave group velocity dispersion curves (5–60 s) were inverted jointly using Very Fast Simulated Annealing (VFSA) to map 1D $V_s$ profiles and parameter posterior probability distributions. Preliminary crustal thickness and bulk $V_p/V_s$ ($\kappa$) were derived via Zhu & Kanamori (2000) $H-\kappa$ stacking.
* **Audited Findings:**
  * Eastern Shillong Plateau stations exhibit remarkably thin continental crust: `JOWA` has $H_{\text{joint}} = 28.9 \pm 1.4\text{ km}$ ($H_{\kappa} = 29.1\text{ km}$, $\kappa = 1.74$); `KHLI` has $H_{\text{joint}} = 32.0 \pm 1.6\text{ km}$ ($H_{\kappa} = 31.8\text{ km}$, $\kappa = 1.71$); and `MAWK` has $H_{\text{joint}} = 32.5 \pm 1.6\text{ km}$ ($H_{\kappa} = 32.3\text{ km}$, $\kappa = 1.69$).
  * The permanent Shillong station (`SHL`) yields $H = 33.0 \pm 1.5\text{ km}$ ($\kappa = 1.73$).
  * In the Indo-Burma Ranges, `KOHI` shows a thick crustal root: $H_{\kappa} = 45.0 \pm 2.0\text{ km}$ with a high bulk $V_p/V_s = 1.82$, indicative of intermediate-to-mafic composition or tectonic underthrusting.
  * `DHUB` on the western Assam border yields $H_{\kappa} = 37.0 \pm 2.0\text{ km}$ ($\kappa = 1.78$).

### 3.2 Study B: Mitra et al. (2018) — Eastern Himalayan Plate Boundary System
* **Citation:** Mitra, S., Priestley, K. F., Borah, K., & Gaur, V. K. (2018). Crustal Structure and Evolution of the Eastern Himalayan Plate Boundary System, Northeast India. *Journal of Geophysical Research: Solid Earth*, 123(1), 621–640. DOI: [10.1002/2017JB014714](https://doi.org/10.1002/2017JB014714).
* **Network & Deployment:** 24 broadband seismographs deployed across the Brahmaputra Valley, Shillong Plateau, Mikir Hills, and Bengal Basin by IISER Kolkata and Cambridge University.
* **Methodological Distinction (24 Deployed vs. 8 Usable Stations):**
  * In the Bengal Basin and Surma Valley, thick Neogene unconsolidated sediments ($6\text{–}15\text{ km}$) cause severe low-velocity resonance and multiple reverberations that obscure direct Moho conversions. Consequently, conventional $H-\kappa$ grid search failed at most basin stations.
  * Quantitative constraints were achieved through a combination of: (i) rigorous receiver function inversion with formal uncertainties for hard-rock/thin-sediment stations (`BPN`, `BORJ`, `BAI`, `BNGN`, `SHL`, as synthesized in Table S1 and Priestley, Ho, & Mitra 2019 Table 4); and (ii) 1D waveform synthetic modeling constrained by 2D forward gravity transects across the Dauki Fault and Bengal Basin (`AGT`, `AZL`, `BELO`).
* **Audited Findings:**
  * Thin, felsic crust beneath the central Shillong Plateau (`BPN`: $30.0 \pm 2.7\text{ km}$; `SHL`: $30.0 \pm 2.0\text{ km}$) and Mikir Hills (`BORJ`: $30.0 \pm 2.0\text{ km}$).
  * Northward flexural thickening beneath the Brahmaputra Valley: `BAI` sits at $39.0 \pm 0.5\text{ km}$ ($V_s = 3.46\text{ km/s}$), while `BNGN` (north bank) reaches $48.0 \pm 2.9\text{ km}$ ($V_s = 3.58\text{ km/s}$), recording deep flexural down-warping.
  * In the Bengal Basin, transitional basement ($20\text{–}22\text{ km}$ thick) is buried beneath $14\text{–}15\text{ km}$ of sediments, placing total Moho depth below surface at $35.5\text{–}36.0\text{ km}$ (`AGT`, `BELO`).

### 3.3 Study C: Borah et al. (2016) — CSIR-4PI Regional Network
* **Citation:** Borah, K., Bora, D. K., Goyal, A., & Kumar, R. (2016). Crustal structure beneath northeast India inferred from receiver function modeling. *Physics of the Earth and Planetary Interiors*, 258, 15–27. DOI: [10.1016/j.pepi.2016.07.005](https://doi.org/10.1016/j.pepi.2016.07.005).
* **Network & Deployment:** 10 broadband stations deployed across the Shillong Plateau and Assam Valley, plus one regional context station (`RUP`) in the Lesser Himalaya.
* **Methodology:** Teleseismic $P$-wave receiver functions were analyzed using both $H-V_p/V_s$ stacking (Table 1) and non-linear waveform inversion via the Neighbourhood Algorithm (NA, Table 2) to resolve layer thicknesses, shear velocities, and bulk $V_p/V_s$.
* **Audited Findings:**
  * Shillong Plateau: `TUR` ($37.0 \pm 1.5\text{ km}$), `MND` ($34.0 \pm 1.5\text{ km}$), `NGL` ($38.0 \pm 1.5\text{ km}$), and `SHL` ($35.0 \pm 1.5\text{ km}$). Bulk $V_p/V_s$ ranges from $1.73$ to $1.75$, with average crustal $V_s \approx 3.4\text{–}3.7\text{ km/s}$.
  * Assam / Brahmaputra Valley: `JPA` ($38.0 \pm 1.5\text{ km}$), `TZR` (Tezpur, $39.0 \pm 1.5\text{ km}$), `SNG` ($38.0 \pm 1.5\text{ km}$), `LNK` ($36.5 \pm 1.5\text{ km}$), `BOKO` ($36.0 \pm 1.5\text{ km}$), and `AGIA` ($37.0 \pm 1.5\text{ km}$). Bulk $V_p/V_s$ is elevated ($1.76\text{–}1.81$), indicating intermediate-to-mafic lower crust.
  * Lesser Himalaya (`RUP`): $H = 44.0 \pm 2.0\text{ km}$ with $4.0\text{ km}$ of low-velocity sedimentary/metasedimentary cover and high $V_p/V_s = 1.85$.

---

## 4. Audited Regional Seismic Station Inventory

The updated dataset is archived in [`data/processed/seismic/regional_receiver_function_stations.csv`](file:///e:/northeast-india-isostasy/data/processed/seismic/regional_receiver_function_stations.csv). Table 4.1 presents the complete station inventory, distinguishing $H-\kappa$ stacking estimates from joint-inversion estimates and specifying benchmark flags.

### Table 4.1: Audited Regional Receiver-Function Dataset (25 Records)

| Obs ID | Physical Code | Station Name | Study | Lat (°N) | Lon (°E) | Elev (m) | Domain | Method | $H_{\kappa}$ (km) | $\kappa$ | $H_{\text{joint}}$ (km) | $\pm \sigma$ | Pref. $H$ (km) | $\pm \sigma$ | In Core? | Repeated? | Primary? |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **AGR21_JOWA** | JOWA | Jowai | Agrawal '21 | 25.450 | 92.210 | 1390 | Shillong Plateau (E) | Joint Inv (VFSA) & $H-\kappa$ | 29.1 | 1.74 | 28.9 | 1.4 | 28.9 | 1.4 | **Yes** | No | **Yes** |
| **AGR21_KHLI** | KHLI | Khliehriat | Agrawal '21 | 25.350 | 92.300 | 1160 | Shillong Plateau (E) | Joint Inv (VFSA) & $H-\kappa$ | 31.8 | 1.71 | 32.0 | 1.6 | 32.0 | 1.6 | **Yes** | No | **Yes** |
| **AGR21_MAWK** | MAWK | Mawryngkneng | Agrawal '21 | 25.550 | 92.060 | 1530 | Shillong Plateau (C-E) | Joint Inv (VFSA) & $H-\kappa$ | 32.3 | 1.69 | 32.5 | 1.6 | 32.5 | 1.6 | **Yes** | No | **Yes** |
| **AGR21_SHL** | SHL | Shillong | Agrawal '21 | 25.560 | 91.880 | 1598 | Shillong Plateau (C) | $H-\kappa$ & Joint Inv | 33.0 | 1.73 | 33.0 | 1.5 | 33.0 | 1.5 | **Yes** | **Yes** | **Yes** |
| **AGR21_KOHI** | KOHI | Kohima | Agrawal '21 | 25.630 | 94.160 | 1406 | Indo-Burma Ranges | $H-\kappa$ stacking (PRF) | 45.0 | 1.82 | NaN | NaN | 45.0 | 2.0 | **Yes** | No | **Yes** |
| **AGR21_DHUB** | DHUB | Dhubri | Agrawal '21 | 26.010 | 89.980 | 40 | W. Brahmaputra | $H-\kappa$ stacking (PRF) | 37.0 | 1.78 | NaN | NaN | 37.0 | 2.0 | **No** (Reg.) | No | **Yes** |
| **MIT18_BPN** | BPN | Barapani | Mitra '18 | 25.669 | 91.908 | 1095 | Shillong Plateau (C) | RF Inversion & $H-\kappa$ | 30.0 | NaN | 30.0 | 2.7 | 30.0 | 2.7 | **Yes** | No | **Yes** |
| **MIT18_BORJ** | BORJ | Borjuri | Mitra '18 | 26.411 | 92.932 | 66 | Mikir Hills Margin | RF Inversion & $H-\kappa$ | 30.0 | NaN | 30.0 | 2.0 | 30.0 | 2.0 | **Yes** | No | **Yes** |
| **MIT18_BAI** | BAI | Baihata | Mitra '18 | 26.318 | 91.739 | 65 | Brahmaputra Valley | RF Inversion & $H-\kappa$ | 39.0 | NaN | 39.0 | 0.5 | 39.0 | 0.5 | **Yes** | No | **Yes** |
| **MIT18_BNGN** | BNGN | Bongaigaon | Mitra '18 | 26.451 | 90.558 | 67 | N. Brahmaputra | RF Inversion & $H-\kappa$ | 48.0 | NaN | 48.0 | 2.9 | 48.0 | 2.9 | **Yes** | No | **Yes** |
| **MIT18_SHL** | SHL | Shillong (Mitra) | Mitra '18 | 25.570 | 91.870 | 1590 | Shillong Plateau | 1D Waveform / Gravity | NaN | NaN | 30.0 | 2.0 | 30.0 | 2.0 | **Yes** | **Yes** | No |
| **MIT18_AGT** | AGT | Agartala | Mitra '18 | 23.889 | 91.246 | 18 | Bengal Basin | 1D Waveform & Gravity | NaN | NaN | 36.0 | 2.0 | 36.0 | 2.0 | **Yes** | No | **Yes** |
| **MIT18_AZL** | AZL | Aizawl | Mitra '18 | 23.738 | 92.690 | 969 | Indo-Burma Ranges | 1D Waveform Modeling | NaN | NaN | 39.0 | 2.0 | 39.0 | 2.0 | **Yes** | No | **Yes** |
| **MIT18_BELO** | BELO | Belonia | Mitra '18 | 23.250 | 91.450 | 25 | Bengal Basin (S) | 1D Waveform & Gravity | NaN | NaN | 35.5 | 2.0 | 35.5 | 2.0 | **Yes** | No | **Yes** |
| **BOR16_TUR** | TUR | Tura | Borah '16 | 25.546 | 90.243 | 305 | Shillong Plateau (W) | $H-V_p/V_s$ & NA Inversion | 37.0 | 1.73 | 37.0 | 1.5 | 37.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_MND** | MND | Mendipathar | Borah '16 | 25.924 | 90.676 | 40 | Shillong Plateau (N) | $H-V_p/V_s$ & NA Inversion | 34.0 | 1.74 | 34.0 | 1.5 | 34.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_NGL** | NGL | Nangalbibra | Borah '16 | 25.472 | 90.702 | 330 | Shillong Plateau (C) | $H-V_p/V_s$ & NA Inversion | 38.0 | 1.75 | 38.0 | 1.5 | 38.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_SHL** | SHL | Shillong (Borah) | Borah '16 | 25.566 | 91.859 | 1590 | Shillong Plateau (E) | $H-V_p/V_s$ & NA Inversion | 35.0 | 1.74 | 35.0 | 1.5 | 35.0 | 1.5 | **Yes** | **Yes** | No |
| **BOR16_JPA** | JPA | Jogighopa | Borah '16 | 26.239 | 90.575 | 42 | Assam Valley (W) | $H-V_p/V_s$ & NA Inversion | 38.0 | 1.80 | 38.0 | 1.5 | 38.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_TZR** | TEZP | Tezpur (TZR) | Borah '16 | 26.617 | 92.783 | 140 | Assam Valley (N) | $H-V_p/V_s$ & NA Inversion | 39.0 | 1.81 | 39.0 | 1.5 | 39.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_SNG** | SNG | Singri | Borah '16 | 26.608 | 92.474 | 60 | Assam Valley (C) | $H-V_p/V_s$ & NA Inversion | 38.0 | 1.80 | 38.0 | 1.5 | 38.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_LNK** | LNK | Lanka | Borah '16 | 25.905 | 92.985 | 90 | Mikir Foreland | $H-V_p/V_s$ & NA Inversion | 36.5 | 1.77 | 36.5 | 1.5 | 36.5 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_BOKO** | BOKO | Boko | Borah '16 | 25.969 | 91.244 | 50 | Brahmaputra (S) | $H-V_p/V_s$ & NA Inversion | 36.0 | 1.76 | 36.0 | 1.5 | 36.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_AGIA** | AGIA | Agia | Borah '16 | 26.066 | 90.464 | 75 | Brahmaputra (S) | $H-V_p/V_s$ & NA Inversion | 37.0 | 1.78 | 37.0 | 1.5 | 37.0 | 1.5 | **Yes** | No | **Yes** |
| **BOR16_RUP** | RUP | Rupa | Borah '16 | 27.200 | 92.400 | 1500 | Lesser Himalaya | $H-V_p/V_s$ & NA Inversion | 44.0 | 1.85 | 44.0 | 2.0 | 44.0 | 2.0 | **No** (Reg.) | No | **Yes** |

*Note on Density:* In strict accordance with seismological principles, density is marked as "Not Provided" for all receiver-function stations because receiver functions invert for velocity contrasts and acoustic/shear impedances ($V_s$, $V_p/V_s$), not volumetric mass density.

---

## 5. Spatial Distribution and Boundary Verification

### 5.1 Core Study Window vs. Regional Context
* **Core Study Window ($22^\circ\text{–}27^\circ\text{N}$, $90^\circ\text{–}95^\circ\text{E}$):** Contains **23 observation records** representing **21 unique physical stations**.
* **Regional Context Stations ($N = 2$):**
  1. `DHUB` ($26.010^\circ\text{N}, 89.980^\circ\text{E}$): Located $0.02^\circ$ west of $90.00^\circ\text{E}$. Samples the western Brahmaputra foreland and its transition to the Indian Shield.
  2. `RUP` ($27.200^\circ\text{N}, 92.400^\circ\text{E}$): Located $0.20^\circ$ north of $27.00^\circ\text{N}$. Samples the flexural down-warping of the Indian crust beneath the Lesser Himalaya.

### 5.2 Station Independence and Repeated Observations
* **Repeated Stations (`SHL` $\times 3$):** The permanent NCS station at Shillong (`SHL`) was independently analyzed by Agrawal et al. ($33.0\pm 1.5\text{ km}$), Mitra et al. ($30.0\pm 2.0\text{ km}$), and Borah et al. ($35.0\pm 1.5\text{ km}$). To prevent spatial distortion, `AGR21_SHL` is designated as the primary benchmark record (`primary_benchmark_station = True`) due to its joint receiver-function and surface-wave inversion, while `MIT18_SHL` and `BOR16_SHL` are preserved for inter-study consistency checks but excluded from deduplicated spatial statistics.
* **Clarification on `TEZP` and `BOKO`:**
  - `TEZP`: Analyzed in Borah et al. (2016) as `TZR` ($39.0 \pm 1.5\text{ km}$). While deployed in regional network inventories in Mitra et al. (2018), it is quantitatively provided in this baseline by Borah et al.
  - `BOKO`: Deployed in Mitra et al. (2018) Table 1, but standard $H-\kappa$ stacking was impeded by sediment resonance; it was successfully modeled by Borah et al. (2016) via Neighbourhood Algorithm inversion ($36.0 \pm 1.5\text{ km}$).

### 5.3 Diagnostic Cartographic Map

Figure 5.1 illustrates the spatial distribution of all 25 audited seismic stations overlaid on the CRUST1.0 Moho Depth below Sea Level grid and the bounding box of the study region.

![Audited Northeast India Regional Receiver-Function Seismic Stations](file:///e:/northeast-india-isostasy/results/maps/regional_seismic_station_locations.png)
*Figure 5.1: Audited seismic receiver-function station locations across Northeast India, categorized by study source and overlaid on the CRUST1.0 Moho depth grid (shading in km below MSL) and the study region boundary ($22^\circ\text{–}27^\circ\text{N}$, $90^\circ\text{–}95^\circ\text{E}$). Regional context stations outside the boundary (`DHUB`, `RUP`) are highlighted with distinct dashed symbols.*

---

## 6. Harmonized Comparison of Regional Observations with CRUST1.0

### 6.1 Mathematical Harmonization of Vertical Datums

To eliminate artificial offsets caused by topography, vertical references must be harmonized mathematically before comparison:
1. **Receiver Function Crustal Thickness ($T_{c,\text{obs}}$):**  
   Receiver function phase conversions originate at the Moho and travel to the seismometer located at the Earth's topographic surface ($h_{\text{station}}$ in km). Hence, the preferred receiver function estimate $H_{\text{obs}}$ represents total crustal thickness:
   $$T_{c,\text{obs}} = H_{\text{obs}}$$
2. **Observed Moho Depth Below Sea Level ($D_{\text{Moho,SL,obs}}$):**  
   Referenced to Mean Sea Level ($z = 0.0\text{ km}$):
   $$D_{\text{Moho,SL,obs}} = H_{\text{obs}} - h_{\text{station}} = H_{\text{obs}} - \frac{\text{Elevation (m)}}{1000}$$
3. **CRUST1.0 Model Definitions:**  
   - $T_{c,\text{CRUST1.0}}$: Sum of all crustal layer thicknesses (sediments + crystalline crust).
   - $D_{\text{Moho,SL,CRUST1.0}} = -\text{mantle\_top}$.
4. **Residual Definitions:**  
   $$\Delta T_c = T_{c,\text{obs}} - T_{c,\text{CRUST1.0}}$$
   $$\Delta D_{\text{Moho,SL}} = D_{\text{Moho,SL,obs}} - D_{\text{Moho,SL,CRUST1.0}}$$
   A negative residual indicates that the empirical receiver-function Moho is shallower / thinner than CRUST1.0.

### 6.2 Core Study Area Comparison Table (23 Records)

Table 6.1 compares every observation record in the core study window against its co-located CRUST1.0 $1^\circ \times 1^\circ$ cell.

### Table 6.1: Core Study Area Seismic Observations vs. CRUST1.0

| Physical Code | Obs ID | Lat (°N) | Lon (°E) | Elev (m) | $H_{\text{obs}}$ (km) | $D_{\text{Moho,SL}}^{\text{obs}}$ (km) | CRUST1.0 $T_c$ (km) | CRUST1.0 $D_{\text{Moho}}^{\text{SL}}$ (km) | $\Delta T_c$ (km) | $\Delta D_{\text{Moho}}^{\text{SL}}$ (km) | Benchmark? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **JOWA** | AGR21_JOWA | 25.450 | 92.210 | 1390 | 28.9 | 27.51 | 36.27 | 35.60 | **$-7.37$** | **$-8.09$** | **Primary** |
| **KHLI** | AGR21_KHLI | 25.350 | 92.300 | 1160 | 32.0 | 30.84 | 36.27 | 35.60 | **$-4.27$** | **$-4.76$** | **Primary** |
| **MAWK** | AGR21_MAWK | 25.550 | 92.060 | 1530 | 32.5 | 30.97 | 36.27 | 35.60 | **$-3.77$** | **$-4.63$** | **Primary** |
| **SHL** | AGR21_SHL | 25.560 | 91.880 | 1598 | 33.0 | 31.40 | 36.18 | 35.45 | **$-3.18$** | **$-4.05$** | **Primary** |
| **KOHI** | AGR21_KOHI | 25.630 | 94.160 | 1406 | 45.0 | 43.59 | 42.00 | 40.65 | **$+3.00$** | **$+2.94$** | **Primary** |
| **BPN** | MIT18_BPN | 25.669 | 91.908 | 1095 | 30.0 | 28.91 | 36.18 | 35.45 | **$-6.18$** | **$-6.55$** | **Primary** |
| **BORJ** | MIT18_BORJ | 26.411 | 92.932 | 66 | 30.0 | 29.93 | 42.01 | 41.87 | **$-12.01$** | **$-11.94$** | **Primary** |
| **BAI** | MIT18_BAI | 26.318 | 91.739 | 65 | 39.0 | 38.94 | 42.00 | 41.77 | **$-3.00$** | **$-2.84$** | **Primary** |
| **BNGN** | MIT18_BNGN | 26.451 | 90.558 | 67 | 48.0 | 47.93 | 35.82 | 35.58 | **$+12.18$** | **$+12.35$** | **Primary** |
| **SHL** | MIT18_SHL | 25.570 | 91.870 | 1590 | 30.0 | 28.41 | 36.18 | 35.45 | $-6.18$ | $-7.04$ | Repeated |
| **AGT** | MIT18_AGT | 23.889 | 91.246 | 18 | 36.0 | 35.98 | 39.00 | 38.94 | **$-3.00$** | **$-2.96$** | **Primary** |
| **AZL** | MIT18_AZL | 23.738 | 92.690 | 969 | 39.0 | 38.03 | 39.00 | 38.58 | **$0.00$** | **$-0.55$** | **Primary** |
| **BELO** | MIT18_BELO | 23.250 | 91.450 | 25 | 35.5 | 35.48 | 39.00 | 38.94 | **$-3.50$** | **$-3.47$** | **Primary** |
| **TUR** | BOR16_TUR | 25.546 | 90.243 | 305 | 37.0 | 36.70 | 35.36 | 35.13 | **$+1.64$** | **$+1.57$** | **Primary** |
| **MND** | BOR16_MND | 25.924 | 90.676 | 40 | 34.0 | 33.96 | 35.36 | 35.13 | **$-1.36$** | **$-1.17$** | **Primary** |
| **NGL** | BOR16_NGL | 25.472 | 90.702 | 330 | 38.0 | 37.67 | 35.36 | 35.13 | **$+2.64$** | **$+2.54$** | **Primary** |
| **SHL** | BOR16_SHL | 25.566 | 91.859 | 1590 | 35.0 | 33.41 | 36.18 | 35.45 | $-1.18$ | $-2.04$ | Repeated |
| **JPA** | BOR16_JPA | 26.239 | 90.575 | 42 | 38.0 | 37.96 | 35.82 | 35.58 | **$+2.18$** | **$+2.38$** | **Primary** |
| **TEZP** | BOR16_TZR | 26.617 | 92.783 | 140 | 39.0 | 38.86 | 42.01 | 41.87 | **$-3.01$** | **$-3.01$** | **Primary** |
| **SNG** | BOR16_SNG | 26.608 | 92.474 | 60 | 38.0 | 37.94 | 42.01 | 41.87 | **$-4.01$** | **$-3.93$** | **Primary** |
| **LNK** | BOR16_LNK | 25.905 | 92.985 | 90 | 36.5 | 36.41 | 36.27 | 35.60 | **$+0.23$** | **$+0.81$** | **Primary** |
| **BOKO** | BOR16_BOKO | 25.969 | 91.244 | 50 | 36.0 | 35.95 | 36.18 | 35.45 | **$-0.18$** | **$+0.50$** | **Primary** |
| **AGIA** | BOR16_AGIA | 26.066 | 90.464 | 75 | 37.0 | 36.92 | 35.82 | 35.58 | **$+1.18$** | **$+1.35$** | **Primary** |

---

### 6.3 Deduplicated Statistical Summary and Tectonic Interpretation

To prevent statistical skewing from repeated observations at `SHL`, summary metrics are computed **strictly across the 21 unique primary benchmark stations** within the core study window:

* **Overall Core Study Window Statistics ($N = 21$ unique stations):**
  * **Mean Crustal Thickness Residual ($\Delta T_c$):** **$-1.51\text{ km}$** (Std: $4.80\text{ km}$; Range: $-12.01\text{ km}$ to $+12.18\text{ km}$).
  * **Mean Moho Sea-Level Residual ($\Delta D_{\text{Moho,SL}}$):** **$-1.59\text{ km}$** (Std: $4.96\text{ km}$; Range: $-11.94\text{ km}$ to $+12.35\text{ km}$).
* **Tectonic Province Breakdown:**
  1. **Shillong Plateau ($N = 8$: `JOWA`, `KHLI`, `MAWK`, `SHL`, `BPN`, `TUR`, `MND`, `NGL`):**
     * Mean observed crustal thickness: **$33.17\text{ km}$** (Range: $28.9\text{–}38.0\text{ km}$).
     * Mean observed Moho depth below sea level: **$32.24\text{ km}$**.
     * Mean $\Delta T_c$: **$-2.73\text{ km}$**; Mean $\Delta D_{\text{Moho,SL}}$: **$-3.14\text{ km}$**.
     * *Key Finding:* Across the central and eastern horst (`JOWA`, `KHLI`, `MAWK`, `BPN`, `SHL`), the empirical Moho is dramatically shallower than CRUST1.0 (residuals of $-3.2\text{ km}$ to $-8.1\text{ km}$). CRUST1.0 fails to capture the uplifted, thin crust of the Shillong horst because its $1^\circ$ cells blend the horst with the surrounding deep foreland basins.
  2. **Brahmaputra / Assam Valley ($N = 9$: `BAI`, `BNGN`, `BORJ`, `JPA`, `TEZP`, `SNG`, `LNK`, `BOKO`, `AGIA`):**
     * Mean observed crustal thickness: **$37.94\text{ km}$** (Range: $30.0\text{–}48.0\text{ km}$).
     * Mean $\Delta T_c$: **$-0.72\text{ km}$**; Mean $\Delta D_{\text{Moho,SL}}$: **$-0.48\text{ km}$**.
     * *Key Finding:* While the regional mean residual is near zero, local residuals are extreme ($-12.0\text{ km}$ at `BORJ` vs. $+12.2\text{ km}$ at `BNGN`). At `BNGN` on the north bank, the Moho plunges flexurally to $48.0\text{ km}$ beneath Himalayan foreland loading, which CRUST1.0 completely misses (assigning only $35.8\text{ km}$). Conversely, at `BORJ` on the Mikir Hills edge, crystalline basement is shallow ($30.0\text{ km}$), whereas CRUST1.0 assigns $42.0\text{ km}$.
  3. **Basins & Accretionary Margins ($N = 4$: `KOHI`, `AGT`, `AZL`, `BELO`):**
     * Mean $\Delta T_c$: **$-0.88\text{ km}$**.
     * In the Bengal Basin (`AGT`, `BELO`), Moho depth below sea level sits at $\sim 35.5\text{–}36.0\text{ km}$, but $14\text{–}15\text{ km}$ of that column is low-density Cenozoic sediment. At `KOHI` in the Indo-Burma Ranges, crustal thickness reaches $45.0\text{ km}$ ($\Delta T_c = +3.0\text{ km}$).

---

## 7. Density Limitations and Geodynamic Implications for Airy–Pratt Modelling

### 7.1 Scientific Clarification: Velocity vs. Density
A critical finding of this scientific audit is that **none of the published receiver-function studies directly measure or invert for crustal mass density**:
1. **Receiver Function Physics:** Teleseismic $P$-to-$S$ conversions are governed by velocity contrasts and shear-wave impedance boundaries ($\Delta V_s / V_s$ and $V_p/V_s$). They have zero direct sensitivity to absolute volumetric mass density ($\rho$).
2. **Bulk $V_p/V_s$ as a Compositional Proxy:** Bulk crustal $V_p/V_s$ ($\kappa$) reflects mineralogy and Poisson's ratio (e.g., quartz-rich felsic crust yields $V_p/V_s \approx 1.68\text{–}1.73$; plagioclase/amphibole-rich mafic crust yields $V_p/V_s \approx 1.78\text{–}1.84$). However, converting $V_p/V_s$ to density requires empirical scaling laws (e.g., Birch's Law or Brocher 2005 polynomials) which carry substantial non-uniqueness.
3. **Gravity Profile Densities in Mitra et al. (2018):** Densities reported in Mitra et al. ($2.67\text{–}2.72\text{ g/cm}^3$ for upper crust; $2.85\text{–}2.90\text{ g/cm}^3$ for lower crust) are **assumed forward-modeling parameters**, not independent empirical observations.

### 7.2 Geodynamic Implications for Classical Isostasy
The audited seismic baseline provides a decisive benchmark for evaluating classical isostatic compensation:
* **The Shillong Plateau Paradox (Airy Failure):** Classical Airy isostasy predicts that a topographic plateau elevated $1.5\text{ km}$ above sea level should possess a crustal root extending $5\text{–}8\text{ km}$ deeper than the surrounding lowlands ($T_c \approx 40\text{–}43\text{ km}$ for $T_0 = 35\text{ km}$). In stark contrast, our audited seismic baseline demonstrates that the crust beneath the Shillong horst is only **$28.9\text{–}33.0\text{ km}$ thick**—significantly *thinner* than the adjacent Brahmaputra foreland ($38\text{–}48\text{ km}$). This proves conclusively that the Shillong Plateau is **not** supported by local Airy isostatic roots, but is supported dynamically or flexurally by pop-up tectonics between bounding crustal faults (Dauki and Brahmaputra faults).
* **Foreland Flexural Loading:** The Brahmaputra Valley Moho deepens sharply from south to north ($36\text{ km}$ at `BOKO` to $48\text{ km}$ at `BNGN`), characteristic of flexural bending under the advancing Himalayan orogenic wedge.
* **Superiority over CRUST1.0:** The global CRUST1.0 model blurs these narrow structural transitions due to its $1^\circ$ resolution. The audited receiver-function dataset provides the true empirical ground truth necessary to validate forward and inverse isostatic gravity calculations.

---

## 8. Verification and Sign-Off Checklist

- [x] **Agrawal et al. (2021) fully audited:** Erroneous values for `JOWA`, `KHLI`, `MAWK`, `SHL`, and `KOHI` corrected directly from published Table 2 ($H-\kappa$) and Table 3 (Joint model).
- [x] **Distinct parameter columns:** $H-\kappa$ stacking and joint-inversion Moho estimates maintained in separate, explicit columns.
- [x] **Mitra et al. (2018) inventory clarified:** 24-station deployment distinguished from the 8 stations with usable quantitative Moho constraints.
- [x] **Borah et al. (2016) parameters verified:** 10 network stations + regional station `RUP` verified against PEPI Table 1 & Table 2.
- [x] **Station independence enforced:** Repeated observations (`SHL` $\times 3$) flagged; primary benchmarks selected; spatial statistics deduplicated.
- [x] **Core window separation:** Core study area ($22^\circ\text{–}27^\circ\text{N}$, $90^\circ\text{–}95^\circ\text{E}$, $N=21$ unique stations) separated from regional context stations (`DHUB`, `RUP`).
- [x] **Density limitations documented:** Explicitly clarified that receiver functions do not measure density; densities labeled as "Not Provided".
- [x] **Deliverables updated and verified:**
  - Audited CSV saved: [`data/processed/seismic/regional_receiver_function_stations.csv`](file:///e:/northeast-india-isostasy/data/processed/seismic/regional_receiver_function_stations.csv).
  - Diagnostic map regenerated: [`results/maps/regional_seismic_station_locations.png`](file:///e:/northeast-india-isostasy/results/maps/regional_seismic_station_locations.png).
  - Review report rewritten: [`reports/regional_seismic_data_review.md`](file:///e:/northeast-india-isostasy/reports/regional_seismic_data_review.md).
- [x] **Scientific restrictions maintained:** No Airy or Pratt forward calculations executed ahead of instructions.
