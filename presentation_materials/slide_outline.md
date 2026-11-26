# Suggested Presentation Slide Outline (16 Slides, 15–20 Minutes)

1. **Title Slide:** *Northeast India Isostasy: Airy–Heiskanen and Pratt–Hayford Models* — Study area, motivation, and scope.
2. **Tectonic & Geographic Setting:** `22–27°N, 90–95°E` window (Shillong Plateau, Brahmaputra Valley, Bengal Basin, Indo-Burma Ranges) and why a `3°` buffer (`19–30°N, 87–98°E`) is required.
3. **Research Questions & Project Workflow:** Comparing crustal-thickness vs. lateral-density local compensation using 3D spherical tesseroid forward gravity.
4. **Datasets & Preprocessing (Phase 1):** WGM2012 (`2'`), Earth2014 (`1'`), CRUST1.0 (`1°`), and audited regional RF inventory; detection of marine cells (`572` core / `15,288` buffer) and CRUST1.0 fill-value fix.
5. **Literature-Grounded Parameters:** `config/model_parameters.yaml` values ($T_0 = 35\text{ km}$, $\rho_c = 2750$, $\rho_m = 3350$, $\rho_w = 1030$, $D = 100\text{ km}$, $\rho_0 = 3100\text{ kg/m}^3$) and regional vs. adopted distinction.
6. **Isostatic Theory — Land & Marine Airy:** Equal-mass derivation, marine anti-root with $\rho_w$, and strict separation of $b$, $D_{\text{Moho,SL}}$, and $T_c$.
7. **Isostatic Theory — Land & Marine Pratt:** Equal-mass derivation with $\rho_w$ in marine columns, and mass-balance verification.
8. **WGM2012 Bouguer Reference Conventions:** What the degree-2160 spherical Bouguer operator removes on land ($\rho_B = 2670\text{ kg/m}^3$) and replaces in ocean ($[h, 0]$), plus `~5'` EGM2008 resolution limit.
9. **Bouguer-Consistent 3D Tesseroid Formulation:** Two-layer Airy and Pratt geometries (`[R, R+h]` / `[R+h, R]` stripping-mismatch layers) and why they preserve exact $-\rho_B h$ and $+(\rho_B - \rho_w)d$ mass balance.
10. **Numerical Validation & Convergence:** `23/23` tests passing — infinite slab (`0.6801%`), Nagy prism (`< 0.5%`), buffer edge-effect test, and `0.212%` shallow-layer mesh convergence (`+1.0 m` surface regularization).
11. **Observed Gravity Field:** `figures/phase3_bouguer_observed.png` — spatial pattern (`-159.21` to `+165.83 mGal`, mean `+27.58 mGal`).
12. **Airy vs. Pratt Predicted Gravity:** Side-by-side `figures/phase3_airy_predicted_gravity.png` (`mean -58.84 mGal`) and `figures/phase3_pratt_predicted_gravity.png` (`mean -57.86 mGal`).
13. **Airy vs. Pratt Bouguer Residuals:** Side-by-side `figures/phase3_airy_residual.png` (`mean +86.42 mGal`) and `figures/phase3_pratt_residual.png` (`mean +85.44 mGal`).
14. **Regional Cross-Sections & Correlation Analysis:** `figures/phase3_cross_sections.png` (`91.87°E` N–S and `25.50°N` E–W transects) and `figures/phase3_gravity_comparison.png` ($r = 0.6842$ vs. $0.6862$; std reduced `56.55 -> 41.66/41.98 mGal`).
15. **Scientific Limitations & Unresolved Offset:** Local $T_e = 0$ assumption, single-layer uniform crust, non-uniqueness, and why the `+86 mGal` offset remains unresolved without Phase 4 seismic testing.
16. **Conclusions & Future Work (Phase 4):** Summary of verified Phase 3 deliverables and next steps (station-level RF Moho validation, $V_p$–$\rho$ analysis, and flexural/sediment modeling).
