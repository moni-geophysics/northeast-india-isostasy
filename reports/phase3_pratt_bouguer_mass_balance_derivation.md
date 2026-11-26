# Phase 3 Theoretical Verification: Complete Bouguer-Consistent Pratt & Airy Gravity Formulations

**Project:** Northeast India Airy–Pratt Isostasy Analysis  
**Task:** Read-only first-principles derivation of Bouguer-consistent Pratt and Airy tesseroid layers for land ($h \ge 0$) and marine ($h < 0$) columns relative to WGM2012 Complete Spherical Bouguer conventions.  
**Date:** 2026-11-26  

---

## 1. WGM2012 Bouguer Reference Density & Operator

Let $z = 0$ denote Mean Sea Level / the geoid (positive upward, negative downward), and $h(x, y)$ denote surface elevation ($h \ge 0$ subaerial land; $h < 0$ ocean bathymetry with water depth $d = -h > 0$).

Per Balmino et al. (2012, *J. Geodesy*, DOI: `10.1007/s00190-011-0533-4`), the WGM2012 Complete Spherical Bouguer anomaly ($\Delta g_B$) is obtained from the physical-surface Free-Air anomaly ($\Delta g_{FA}$, relative to GRS80 normal gravity) by applying a Bouguer + spherical terrain reduction operator $\mathcal{B}\{\cdot\}$ using constant reduction density $\rho_B = 2670\text{ kg/m}^3$ and seawater density $\rho_w = 1030\text{ kg/m}^3$:

- **Land ($h \ge 0$):** Subtracts the gravitational attraction of rock of density $\rho_B$ over $z \in [0, h]$:
  $$\Delta g_B = \Delta g_{FA} - g\big(\rho_B \text{ on } [0, h]\big)$$
- **Marine ($h < 0$, $d = -h > 0$):** Replaces seawater ($\rho_w$) with Bouguer rock ($\rho_B$) over $z \in [h, 0]$:
  $$\Delta g_B = \Delta g_{FA} + g\big((\rho_B - \rho_w) \text{ on } [h, 0]\big)$$

Consequently, if a physical Earth model has density $\rho_{\text{phys}}(z)$ relative to a sub-geoid reference column $\rho_{\text{ref}}(z)$ (defined on $z \le 0$, with $0$ above $z = 0$), applying $\mathcal{B}\{\cdot\}$ yields the **Bouguer-equivalent density anomaly** $\Delta\rho_B(z)$:

- **Land ($h \ge 0$):**
  $$\Delta\rho_B(z) = \begin{cases} \rho_{\text{phys}}(z) - \rho_B, & z \in [0, h] \\ \rho_{\text{phys}}(z) - \rho_{\text{ref}}(z), & z \in [-D, 0] \end{cases}$$
- **Marine ($h < 0$):**
  $$\Delta\rho_B(z) = \begin{cases} \big(\rho_w + (\rho_B - \rho_w)\big) - \rho_{\text{ref}}(z) = \rho_B - \rho_{\text{ref}}(z), & z \in [h, 0] \\ \rho_{\text{phys}}(z) - \rho_{\text{ref}}(z), & z \in [-D, h] \end{cases}$$

---

## 2. Pratt–Hayford Mass Balance & Bouguer-Consistent Layers

In Pratt–Hayford isostasy, the reference column ($h = 0$) has uniform density $\rho_0$ on $z \in [-D, 0]$ (reference mass $M_{\text{ref}} = \rho_0 D$).

### 2.1 Land Column ($h \ge 0$)
1. **Physical Mass Balance:**
   $$\rho_{\text{Pratt}}(D + h) = \rho_0 D \implies \rho_{\text{Pratt}} = \rho_0 \frac{D}{D + h}$$
   Physical mass anomaly relative to reference: $\rho_{\text{Pratt}} h + (\rho_{\text{Pratt}} - \rho_0) D = 0$.
2. **Bouguer-Consistent Tesseroid Layers:**
   - **Layer 1 (Sub-geoid compensation, $z \in [-D, 0]$, i.e. $[R - D, R]$):**
     $$\Delta\rho_1 = \rho_{\text{Pratt}} - \rho_0 = -\rho_0 \frac{h}{D + h} < 0$$
   - **Layer 2 (Topographic stripping-mismatch, $z \in [0, h]$, i.e. $[R, R + h]$):**
     $$\Delta\rho_2 = \rho_{\text{Pratt}} - \rho_B$$
3. **Mass Conservation Check:**
   $$\Delta M_{\text{land}, B} = \Delta\rho_1 D + \Delta\rho_2 h = (\rho_{\text{Pratt}} - \rho_0)D + (\rho_{\text{Pratt}} - \rho_B)h = \underbrace{\big[\rho_{\text{Pratt}}(D + h) - \rho_0 D\big]}_{= 0} - \rho_B h = -\rho_B h$$
   This equals the exact mass removed by the WGM2012 Bouguer reduction ($-\rho_B h$), confirming **zero double-counting and zero omitted mass**.

### 2.2 Marine Column ($h < 0$, $d = -h > 0$, $d < D$)
1. **Physical Mass Balance:**
   $$\rho_w d + \rho_{\text{Pratt}}(D - d) = \rho_0 D \implies \rho_{\text{Pratt}} = \frac{\rho_0 D - \rho_w d}{D - d} = \frac{\rho_0 D + \rho_w h}{D + h}$$
   Physical mass anomaly relative to reference: $(\rho_w - \rho_0) d + (\rho_{\text{Pratt}} - \rho_0)(D - d) = 0$.
2. **Bouguer-Consistent Tesseroid Layers:**
   - **Layer 1 (Sub-seafloor compensation, $z \in [-D, h]$, i.e. $[R - D, R + h]$):**
     $$\Delta\rho_1 = \rho_{\text{Pratt}} - \rho_0 = \frac{(\rho_0 - \rho_w) d}{D - d} > 0$$
   - **Layer 2 (Water-replacement mismatch, $z \in [h, 0]$, i.e. $[R + h, R]$):**
     $$\Delta\rho_2 = \rho_B - \rho_0$$
3. **Verification of the Proposed Marine Correction $(\rho_B - \rho_0)$ over $[h, 0]$:**
   Summing the mass of both layers:
   $$\Delta M_{\text{marine}, B} = \Delta\rho_1 (D - d) + \Delta\rho_2 d = (\rho_{\text{Pratt}} - \rho_0)(D - d) + (\rho_B - \rho_0) d$$
   Substituting $(\rho_{\text{Pratt}} - \rho_0)(D - d) = -(\rho_w - \rho_0) d$ from the physical mass balance:
   $$\Delta M_{\text{marine}, B} = -(\rho_w - \rho_0) d + (\rho_B - \rho_0) d = +(\rho_B - \rho_w) d$$
   This equals the **exact mass added** by WGM2012's ocean Bouguer substitution ($+(\rho_B - \rho_w)d$). Therefore, the audit's proposed marine correction $\Delta\rho = \rho_B - \rho_0$ over $[h, 0]$ is **mathematically and physically exact**.
   - *Note:* When $\rho_0 = 3100\text{ kg/m}^3$ and $\rho_B = 2670\text{ kg/m}^3$, $\rho_B - \rho_0 = -430\text{ kg/m}^3 \ne 0$. Omitting this layer leaves an unphysical excess mass of $(\rho_0 - \rho_B)d$. Only in the special case $\rho_0 = \rho_B$ does the $[h, 0]$ layer vanish identically.

---

## 3. Consistent Handling of the Airy Density Mismatch ($\rho_c = 2750$ vs. $\rho_B = 2670\text{ kg/m}^3$)

Applying the exact same WGM2012 Bouguer operator $\mathcal{B}\{\cdot\}$ to the Airy–Heiskanen model ($\rho_{\text{ref}} = \rho_c$ on $[-T_0, 0]$, $\rho_m$ on $[-Z_{\text{comp}}, -T_0]$):

- **Land ($h \ge 0$, $b = \frac{\rho_c}{\rho_m - \rho_c} h > 0$):**
  1. Subsurface root on $[-(T_0 + b), -T_0]$: $\Delta\rho = \rho_c - \rho_m = -600\text{ kg/m}^3$.
  2. Topographic stripping-mismatch on $[0, h]$: $\Delta\rho = \rho_c - \rho_B = +80\text{ kg/m}^3$.
  - Net mass: $(\rho_c - \rho_m)b + (\rho_c - \rho_B)h = -\rho_B h$.
- **Marine ($h < 0$, $d = -h > 0$, $b = -\frac{\rho_c - \rho_w}{\rho_m - \rho_c} d < 0$):**
  1. Subsurface anti-root on $[-T_0, -(T_0 + b)]$: $\Delta\rho = \rho_m - \rho_c = +600\text{ kg/m}^3$.
  2. Water-replacement mismatch on $[h, 0]$: $\Delta\rho = \rho_B - \rho_c = -80\text{ kg/m}^3$.
  - Net mass: $(\rho_m - \rho_c)(-b) + (\rho_B - \rho_c)d = +(\rho_B - \rho_w)d$.

Thus, **both** Airy and Pratt have an identical two-part structure when compared against WGM2012 Complete Spherical Bouguer anomalies: (1) the **subsurface compensating body** ($\Delta\rho_{\text{root}}$ or $\Delta\rho_{\text{Pratt}}$), and (2) the **Bouguer-stripping mismatch layer** between $z = 0$ and $z = h$ ($\rho_{\text{model}} - \rho_B$ on land; $\rho_B - \rho_{\text{ref}}$ on marine).

---

## 4. Summary Table of Final Bouguer-Consistent Tesseroid Geometries

| Model & Domain | Layer | Radial Bounds $[r_{\text{bot}}, r_{\text{top}}]$ | Density Contrast $\Delta\rho$ ($\text{kg/m}^3$) | Net Bouguer Mass |
| :--- | :--- | :--- | :--- | :---: |
| **Airy Land** ($h > 0$) | Root | $[R - (T_0 + b),\; R - T_0]$ | $\rho_c - \rho_m$ (`-600`) | $-\rho_B h$ |
| **Airy Land** ($h > 0$) | Stripping mismatch | $[R,\; R + h]$ | $\rho_c - \rho_B$ (`+80`) | *(included above)* |
| **Airy Marine** ($h < 0$) | Anti-root | $[R - T_0,\; R - (T_0 + b)]$ | $\rho_m - \rho_c$ (`+600`) | $+(\rho_B - \rho_w)d$ |
| **Airy Marine** ($h < 0$) | Water-fill mismatch | $[R + h,\; R]$ | $\rho_B - \rho_c$ (`-80`) | *(included above)* |
| **Pratt Land** ($h > 0$) | Sub-geoid column | $[R - D,\; R]$ | $\rho_{\text{Pratt}} - \rho_0$ | $-\rho_B h$ |
| **Pratt Land** ($h > 0$) | Stripping mismatch | $[R,\; R + h]$ | $\rho_{\text{Pratt}} - \rho_B$ | *(included above)* |
| **Pratt Marine** ($h < 0$) | Sub-seafloor column | $[R - D,\; R + h]$ | $\rho_{\text{Pratt}} - \rho_0$ | $+(\rho_B - \rho_w)d$ |
| **Pratt Marine** ($h < 0$) | Water-fill mismatch | $[R + h,\; R]$ | $\rho_B - \rho_0$ (`-430`) | *(included above)* |

*(Observation points remain on the physical Earth surface $r_{\text{obs}} = R + \max(0, h)$.)*
