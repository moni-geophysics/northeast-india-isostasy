# Verified Project Facts Sheet (For Academic Presentation)

**Study Title:** Northeast India Isostasy: Airy–Heiskanen and Pratt–Hayford Models  
**Project Status:** Frozen at completed Phase 3 (Phase 4 seismic validation not undertaken)

---

## 1. Study Area & Grids
- **Core Study Window:** `22.0°N–27.0°N`, `90.0°E–95.0°E` (`EPSG:4326`, centre `24.5°N, 92.5°E`)
- **Buffered Forward-Modeling Domain:** `19.0°N–30.0°N`, `87.0°E–98.0°E` (`3°` margin to eliminate edge effects)
- **WGM2012 Core Grid:** `151 × 151` (`22,801` nodes), `2'` spacing; effective gravity resolution `~5'` (`EGM2008` degree `2160`)
- **WGM2012 Buffer Grid:** `331 × 331` (`109,561` nodes; `109,417` non-zero elevation cells, `144` zero-elevation cells skipped)
- **Marine Cells ($h < 0$):** `572` in core (`min -38 m`), `15,288` in buffer (`min -2296 m`) in WGM2012 ETOPO1
- **Core Elevation (ETOPO1):** min `-38.00 m`, max `2739.00 m`, mean `409.06 m`, std `505.18 m`, median `160.00 m`

## 2. Literature-Grounded Parameters (`config/model_parameters.yaml`)
- **Airy–Heiskanen:** $T_0 = 35.0\text{ km}$, $\rho_c = 2750\text{ kg/m}^3$ (CRUST1.0 25-cell thickness-weighted mean: `2750.9 kg/m³`), $\rho_m = 3350\text{ kg/m}^3$ ($\Delta\rho = 600\text{ kg/m}^3$), $\rho_w = 1030\text{ kg/m}^3$
- **Pratt–Hayford:** $D = 100.0\text{ km}$, $\rho_0 = 3100\text{ kg/m}^3$, $\rho_w = 1030\text{ kg/m}^3$
- **WGM2012 Bouguer Reduction Density:** $\rho_B = 2670.0\text{ kg/m}^3$

## 3. Governing Equations (MSL Datum $z = 0$, positive upward)
- **Airy Land ($h \ge 0$):** $b = \frac{\rho_c}{\rho_m - \rho_c} h$; $D_{\text{Moho,SL}} = T_0 + b$; $T_c = h + T_0 + b$
- **Airy Marine ($h < 0, d = -h$):** $b = \frac{\rho_c - \rho_w}{\rho_m - \rho_c} h = -\frac{\rho_c - \rho_w}{\rho_m - \rho_c} d$
- **Pratt Land ($h \ge 0$):** $\rho_{\text{Pratt}} = \rho_0 \frac{D}{D + h}$
- **Pratt Marine ($h < 0$):** $\rho_{\text{Pratt}} = \frac{\rho_0 D + \rho_w h}{D + h}$
- **Bouguer-Consistent 3D Tesseroids (`harmonica.tesseroid_gravity`, $R = 6,371,000\text{ m}$, $r_{\text{obs}} = R + \max(0, h) + 1.0\text{ m}$):**
  - Airy: subsurface root/anti-root ($\pm 600\text{ kg/m}^3$) + stripping mismatch between $z = 0$ and $z = h$ ($\pm 80\text{ kg/m}^3$)
  - Pratt: subsurface column ($\rho_{\text{Pratt}} - \rho_0$) + stripping/water-replacement mismatch ($\rho_{\text{Pratt}} - \rho_B$ on land; $\rho_B - \rho_0 = -430\text{ kg/m}^3$ on marine)

## 4. Corrected Phase 3 Results (`22–27°N, 90–95°E`, $N = 22,801$)
- **Observed WGM2012 Bouguer:** min `-159.21`, max `+165.83`, mean `+27.58`, std `56.55`, RMS `62.92 mGal`
- **Airy Predicted (v2):** min `-186.01`, max `-4.46`, mean `-58.84`, std `32.81`, RMS `67.37 mGal`, $r = 0.6842$
- **Pratt Predicted (v2):** min `-184.99`, max `-4.33`, mean `-57.86`, std `30.43`, RMS `65.37 mGal`, $r = 0.6862$
- **Airy Residual (`Obs − Airy`):** min `-49.46`, max `+238.40`, mean `+86.42`, std `41.66`, RMS `95.93 mGal`
- **Pratt Residual (`Obs − Pratt`):** min `-52.76`, max `+239.30`, mean `+85.44`, std `41.98`, RMS `95.19 mGal`

## 5. Verification & Limitations
- **Test Suite:** `23/23` passed (`pytest -v`), including `12°×12°` slab (`0.6801%`), Nagy prism (`< 0.5%`), Bouguer mass-balance (`rel=1e-12`), and `8×8×4` shallow-layer convergence (`0.212%`).
- **Key Limitations:** Phase 4 seismic Moho validation was not executed; models assume $T_e = 0$ local isostasy and uniform single-layer crust; `+86.42 / +85.44 mGal` mean residual is an unresolved regional offset; WGM2012 gravity is limited to `~5'` (`EGM2008` degree `2160`).
