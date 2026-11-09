# Northeast India Airy Isostasy Analysis

A research-oriented Python project investigating Airy isostatic compensation, crustal thickness variations, and lithospheric structure across a fixed 5° × 5° study region in South Asia.

---

## 1. Study Region

The study area is defined by a fixed 5° × 5° rectangular coordinate window. Because this boundary is defined by strict geographic coordinates rather than political boundaries, it encompasses sovereign territories beyond India's administrative borders.

| Attribute | Specification | Geological & Geographic Details |
| :--- | :--- | :--- |
| **Latitude Range** | 22.0°N to 27.0°N | 5° latitudinal span |
| **Longitude Range** | 90.0°E to 95.0°E | 5° longitudinal span |
| **Spatial Extent** | 5° × 5° | Fixed geographic research window |
| **Centre Coordinates** | 24.5°N, 92.5°E | Geometric centroid |
| **Horizontal CRS** | EPSG:4326 | 2D WGS 84 geographic coordinates (latitude / longitude) |
| **Reference Elevation ($h_0$)** | 0.0 m | Baseline sea level datum; must be harmonized with the vertical datum of the selected DEM |
| **Regional Coverage** | Transboundary | **India**: Assam, Meghalaya (Shillong Plateau), Tripura, Mizoram, Manipur, Nagaland, and portions of West Bengal/Arunachal.<br>**Adjoining Territories**: Portions of **Bangladesh** (Sylhet, Chittagong, Dhaka divisions), **Myanmar** (western Chin State and Sagaing Region), and southern **Bhutan**. |

All spatial parameters are maintained in [`config/study_area.yaml`](config/study_area.yaml). Note that EPSG:4326 provides strictly 2D horizontal positioning; the vertical elevation datum is specified independently and must be harmonized with the acquired Digital Elevation Model (DEM).

---

## 2. Project Status

> [!IMPORTANT]
> **Status: Project Initialization & Framework Setup**
> - **No scientific calculations or data analyses have been completed yet.**
> - **No datasets have been acquired or downloaded yet.**
> - **The study area is not yet scientifically validated.**
> - In strict adherence to scientific research protocols, physical constants and model parameters (crustal density $\rho_c$, mantle density $\rho_m$, density contrast $\Delta\rho$, and reference crustal thickness $T_0$) are **not assumed or invented**. They are explicitly flagged as `PENDING_LITERATURE_REVIEW` in [`config/model_parameters.yaml`](config/model_parameters.yaml) pending a systematic synthesis of regional geoscientific literature.

---

## 3. Planned Classical Airy Methodology

The project will evaluate regional isostasy through a classical three-stage methodological framework:

```text
[Digital Elevation Model (DEM)]
            │
            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Topographic Root & Crustal Thickness Calculation    │
│    - Additional root thickness: b(x,y)                 │
│    - Total crustal thickness: T_c,Airy(x,y) = T_0 + b  │
│    - Moho depth below surface: D_Moho,surf = T_c,Airy  │
│    - Moho elevation: z_Moho,Airy(x,y) = h - T_c,Airy   │
│    - Moho depth below sea level: D_Moho,SL = T_c,Airy-h│
└────────────────────────────────────────────────────────┘
            │
            ├────────────────────────────────────────┐
            ▼                                        ▼
┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐
│ 2. Bouguer Gravity Comparison          │  │ 3. Independent Seismic Validation      │
│    - Root density contrast: Δρ < 0     │  │    - Collate published seismic Moho    │
│    - Forward calculate root gravity g_r│  │      (Receiver Functions, DSS, etc.)   │
│    - Observed Bouguer anomaly (Δg_B)   │  │    - Reconcile vertical reference      │
│    - Residual: R_Airy = Δg_B - g_r     │  │      (surface vs. sea-level datum)     │
│    - Evaluate non-unique isostasy state│  │    - Compare like with like (T_c or D) │
└────────────────────────────────────────┘  └────────────────────────────────────────┘
```

### 3.1 Topographic Root & Crustal Thickness Calculation
Under classical Airy-Heiskanen local isostatic equilibrium, topographic column loads are assumed to be supported by buoyant crustal roots displacing denser mantle material at the Moho boundary.

For subaerial topography ($h(x, y) \ge 0$), the **additional Airy root thickness** ($b$) projecting below the reference crustal base is given by:

$$b(x, y) = \left[\frac{\rho_c}{\rho_m - \rho_c}\right] h(x, y)$$

The **total Airy crustal thickness** ($T_{c,\text{Airy}}$) is:

$$T_{c,\text{Airy}}(x, y) = T_0 + b(x, y) = T_0 + \left[\frac{\rho_c}{\rho_m - \rho_c}\right] h(x, y)$$

where:
- $h(x, y)$ is surface topographic elevation above the sea-level reference,
- $T_0$ is the reference crustal thickness at zero elevation ($h = 0$),
- $\rho_c$ is average crustal density, and
- $\rho_m$ is upper mantle density ($\rho_m > \rho_c$).

> [!NOTE]
> **Crucial Distinction: Crustal Thickness vs. Moho Depth (Surface vs. Sea-Level References)**
> Geoscientific literature frequently uses "Moho depth" to refer to two fundamentally different physical quantities:
>
> 1. **Total Crustal Thickness ($T_{c,\text{Airy}}$)** $\equiv$ **Moho depth below local topography ($D_{\text{Moho},\text{surface}}$)**:
>    The total vertical distance from the Earth's surface elevation $h(x, y)$ down to the Moho:
>    $$D_{\text{Moho},\text{surface}}(x, y) = T_{c,\text{Airy}}(x, y) = T_0 + b(x, y)$$
>
> 2. **Moho depth below the sea-level reference ($D_{\text{Moho},\text{SL}}$)**:
>    The vertical distance measured positive downward from the nominal sea-level datum ($h = 0$) to the Moho:
>    $$D_{\text{Moho},\text{SL}}(x, y) = T_{c,\text{Airy}}(x, y) - h(x, y) = T_0 + b(x, y) - h(x, y)$$
>
> 3. **Moho elevation relative to the sea-level reference ($z_{\text{Moho},\text{Airy}}$)**:
>    The Cartesian coordinate measured positive upward (negative downward) from sea level ($h = 0$):
>    $$z_{\text{Moho},\text{Airy}}(x, y) = h(x, y) - T_{c,\text{Airy}}(x, y) = -D_{\text{Moho},\text{SL}}(x, y)$$
>
> Conflating crustal thickness (depth below local surface) with Moho depth below sea level introduces an elevation-dependent systematic error equal to $h(x, y)$, which exceeds $1\text{–}3\text{ km}$ across the Shillong Plateau and exceeds $4\text{–}6\text{ km}$ along Himalayan frontal belts.

#### Handling of Depressions and Water Columns
Bathymetric and water-column cells require a separately derived treatment and will be handled after the DEM and gravity data conventions are selected.

---

### 3.2 Bouguer Gravity Comparison
To evaluate the extent to which the observed gravity field can be accounted for by classical local Airy isostasy:

1. **Forward Gravity Modeling**: Calculate the gravitational attraction of the predicted crustal roots ($\Delta g_{\text{root}}$) relative to the reference crustal baseline $T_0$.
   - Because the root consists of crustal material ($\rho_c$) displacing denser mantle ($\rho_m$), the density contrast of the root is negative: $\Delta\rho_{\text{root}} = \rho_c - \rho_m = -(\rho_m - \rho_c) < 0$.
   - Consequently, the predicted gravitational effect of the root at the surface is a **negative quantity** ($\Delta g_{\text{root}} < 0$).

2. **Isostatic Anomaly Residual**: Compute the Airy Bouguer gravity residual ($R_{\text{Airy}}$):

   $$R_{\text{Airy}} = \Delta g_{\text{Bouguer}} - \Delta g_{\text{root}}$$

   where $\Delta g_{\text{Bouguer}}$ is the observed Complete Bouguer Anomaly and $\Delta g_{\text{root}}$ is the predicted gravitational attraction of the compensating root.

3. **Sign Convention & Mathematical Interpretation**:
   - $R_{\text{Airy}} > 0\text{ mGal}$ (**Positive residual**): The observed Bouguer anomaly is more positive (less negative) than predicted by the full Airy root ($\Delta g_{\text{Bouguer}} > \Delta g_{\text{root}}$). This indicates **apparent undercompensation** (a smaller negative root effect than predicted for local Airy equilibrium).
   - $R_{\text{Airy}} < 0\text{ mGal}$ (**Negative residual**): The observed Bouguer anomaly is more negative than predicted by the root ($\Delta g_{\text{Bouguer}} < \Delta g_{\text{root}}$). This indicates **apparent overcompensation** (a larger negative mass deficit than predicted for local Airy equilibrium).
   - $R_{\text{Airy}} \approx 0\text{ mGal}$ (**Near-zero residual**): Indicates **approximate local Airy compensation**, subject to uncertainties in chosen reference parameters.

> [!WARNING]
> **Non-Uniqueness: Gravity Residuals Do Not Uniquely Prove Isostatic State**
> A non-zero residual $R_{\text{Airy}}$ **does not uniquely prove or diagnose** mechanical undercompensation or overcompensation.
> Because potential-field inversion is inherently non-unique, $R_{\text{Airy}}$ reflects the superimposed gravitational effect of all unmodeled density structures and processes across the lithosphere, including:
> - **Intracrustal and upper-crustal density anomalies**: e.g., the thick, low-density Neogene sediments of the Bengal/Surma and Assam basins ($\Delta g < 0$), or high-density mafic/ultramafic basement intrusions and uplifted granulites in the Shillong Plateau ($\Delta g > 0$).
> - **Flexural / regional isostasy**: Regional plate rigidity supporting topographic loads over broad wavelengths rather than locally beneath individual columns.
> - **Dynamic and sub-lithospheric support**: Mantle upwelling, slab pull from the Burma subduction zone, or edge-driven mantle convection.
> - **Parameter mismatch**: Systematic errors in regional background parameters ($\rho_c$, $\rho_m$, $T_0$).
>
> Therefore, gravity residuals provide an *exploratory anomaly index* rather than conclusive proof of isostatic state, and must be cross-validated against independent seismic data and geological constraints.

---

### 3.3 Independent Seismic Moho Validation
To evaluate the Airy isostatic predictions against independent seismological observations:

1. **Compilation of Seismic Constraints**: Extract published seismological Moho determinations from receiver functions (RF), deep seismic sounding (DSS) refraction/reflection profiles, and local earthquake tomography within the 22–27°N, 90–95°E domain.

2. **Reconciliation of Vertical References**:
   Before comparing seismic determinations with Airy model predictions, the exact vertical reference datum and physical definition of the seismic measurement must be verified:
   - If the seismic measurement represents **Moho depth below the local station surface** ($D_{\text{Moho},\text{station}}$), it is directly equivalent to seismic crustal thickness ($T_{c,\text{seismic}} = D_{\text{Moho},\text{station}}$).
   - If the seismic measurement represents **Moho depth below sea level** ($D_{\text{Moho},\text{SL},\text{seismic}}$), its equivalent crustal thickness requires adding station elevation: $T_{c,\text{seismic}} = D_{\text{Moho},\text{SL},\text{seismic}} + h_{\text{station}}$.
   - If the seismic measurement represents **Moho elevation relative to sea level** ($z_{\text{Moho},\text{seismic}}$, negative downward), its equivalent crustal thickness is: $T_{c,\text{seismic}} = h_{\text{station}} - z_{\text{Moho},\text{seismic}}$.

3. **Harmonized Residual Calculation**:
   - **Crustal Thickness Comparison (preferred when both available)**:
     $$\Delta T_c(x_i, y_i) = T_{c,\text{seismic}}(x_i, y_i) - T_{c,\text{Airy}}(x_i, y_i)$$

   - **Moho Depth Below Sea Level Comparison**:
     $$\Delta D_{\text{Moho},\text{SL}}(x_i, y_i) = D_{\text{Moho},\text{SL},\text{seismic}}(x_i, y_i) - D_{\text{Moho},\text{SL},\text{Airy}}(x_i, y_i)$$

   - **Moho Elevation Comparison**:
     $$\Delta z_{\text{Moho}}(x_i, y_i) = z_{\text{Moho},\text{seismic}}(x_i, y_i) - z_{\text{Moho},\text{Airy}}(x_i, y_i)$$

   > [!IMPORTANT]
   > **Cardinal Rule**: **Never compare quantities with different vertical reference levels.** Subtracting a sea-level-referenced Moho depth from a station-referenced crustal thickness introduces an artificial error equal to station elevation $h_{\text{station}}$, falsely biasing residual interpretation in mountainous terranes.

4. **Domain Partitioning**: Quantify spatial discrepancies ($\Delta T_c$, $\Delta D$) across distinct tectonic provinces (e.g., uplifted Shillong Plateau, Bengal Foredeep sediment wedge, Indo-Burma subduction wedge) to identify where simple local Airy models diverge from regional lithospheric support mechanisms (e.g., flexural rigidity, tectonic overthrusting).

---

## 4. Repository Architecture

```text
northeast-india-isostasy/
├── config/
│   ├── study_area.yaml          # Spatial extent, horizontal CRS, centroid, and datum harmonization
│   └── model_parameters.yaml   # Physical densities and reference thickness (pending literature review)
├── data/
│   ├── README.md                # Data management policy, immutability rules, and versioning
│   ├── raw/                     # Original external downloads (read-only; excluded from Git)
│   └── processed/               # Analysis-ready grids and reproducible summary outputs
├── notebooks/                   # Interactive exploratory notebooks
├── src/
│   ├── __init__.py              # Package root
│   ├── data/                    # DEM & gravity ingestion, clipping, and datum harmonization
│   ├── gravity/                 # Gravity anomaly processing and forward root gravity calculation
│   ├── isostasy/                # Airy root modeling, parameter sensitivity, and residual analysis
│   └── visualization/           # Profile plots, spatial maps, and publication cartography
├── results/
│   ├── figures/                 # Profile diagrams, correlation plots, and diagnostic figures
│   ├── maps/                    # Cartographic outputs and spatial anomaly overlays
│   └── tables/                  # Reproducible tables (parameter sensitivity, seismic residuals)
├── reports/                     # Methodology notes, reports, and literature review synthesis
├── tests/                       # Unit tests and mathematical validation suites
├── requirements.txt             # Python project dependencies
├── .gitignore                   # Git exclusion rules with selective tracking of lightweight outputs
└── README.md                    # Project overview and documentation
```

---

## 5. Setup & Environment

### Prerequisites
- Python 3.10+
- Virtual environment tool (`venv` or `conda`)

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
