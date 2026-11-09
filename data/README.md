# Data Management Protocol: Northeast India Airy Isostasy Analysis

This directory stores datasets used and produced during the Airy isostatic compensation investigation for Northeast India (22°N–27°N, 90°E–95°E).

---

## Directory Organization

```text
data/
├── raw/         # Immutable raw datasets exactly as obtained from primary sources
└── processed/   # Analysis-ready, standardized, clipped, and reprojected data products
```

---

## Data Integrity & Governance Principles

1. **Strict Immutability of Raw Data**:
   - Files stored in `data/raw/` must **never** be manually modified, overwritten, edited, or re-saved.
   - Raw data files serve as immutable ground truth.
   - If an error is found in a raw dataset, re-download the original or document the anomaly in an issue/report rather than altering the raw file in-place.

2. **Automated, Deterministic Preprocessing**:
   - All transformations from raw to processed states (clipping to the 5° × 5° bounding box, coordinate transformations to EPSG:4326, nodata masking, resampling) must be fully automated via Python scripts in `src/data/`.
   - Any file in `data/processed/` must be completely reproducible from `data/raw/` and configuration files.

3. **Data Provenance & Cataloging**:
   - For every external dataset placed in `data/raw/`, maintain an accompanying metadata entry recording:
     - **Dataset Identifier & Version** (e.g., SRTM v3, EGM2008, WGM2012)
     - **Source Organization / Host URL / DOI**
     - **Acquisition Date (UTC)**
     - **Original Coordinate Reference System (CRS) and Spatial Resolution**
     - **Associated Literature Citation**

4. **Version Control & Data Tiering**:
   - **Raw Datasets (`data/raw/`)**: Large external files (DEM rasters, global potential-field grids) are excluded from Git commits.
   - **Processed Datasets (`data/processed/`)**: Large binary grids (`.tif`, `.nc`, `.grd`, `.h5`) are excluded from Git, whereas lightweight, reproducible outputs (e.g., summary tables, profile CSVs, seismic station coordinates, bounding-box GeoJSON, data manifests) are tracked for scientific auditability.
   - Data retrieval scripts and checksums (e.g., SHA-256 via `pooch`) should be used to guarantee identical raw data acquisition across environments.
