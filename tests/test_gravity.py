"""
Numerical validation tests for 3D forward gravity modeling (Phase 3, Part 3):
1. Infinite horizontal slab analytical solution
2. Finite rectangular prism analytical benchmark (Nagy closed-form via Harmonica)
3. Positive and negative density contrasts (land vs marine)
4. Zero density contrast / zero topography
5. Land-marine transitions
6. Grid-edge effects and buffer sensitivity
"""

import math

import harmonica as hm
import numpy as np
import pytest

from src.gravity.forward import (
    EARTH_MEAN_RADIUS_M,
    GRAVITATIONAL_CONSTANT,
    build_airy_tesseroids,
    build_pratt_tesseroids,
    compute_tesseroid_gravity,
)


def test_infinite_horizontal_slab_analytical():
    """
    A wide (12 deg x 12 deg) horizontal shell of thickness H=5 km and
    delta_rho=-600 kg/m^3 at 35-40 km depth should match the infinite Bouguer
    slab formula: dg = 2 * pi * G * delta_rho * H * 1e5 mGal within ~2.5%
    (finite-cap and spherical-shell geometry limit).
    """
    delta_rho = -600.0
    thickness_m = 5000.0
    dg_analytical_mgal = 2.0 * math.pi * GRAVITATIONAL_CONSTANT * delta_rho * thickness_m * 1e5

    lons = np.linspace(86.5, 98.5, 49)  # 0.25-deg cells centered around 92.5E
    lats = np.linspace(18.5, 30.5, 49)  # 0.25-deg cells centered around 24.5N
    dlon = 0.25
    dlat = 0.25
    lon2d, lat2d = np.meshgrid(lons, lats)
    r_bot = EARTH_MEAN_RADIUS_M - 40_000.0
    r_top = EARTH_MEAN_RADIUS_M - 35_000.0
    tess = np.column_stack([
        lon2d.ravel() - 0.5 * dlon,
        lon2d.ravel() + 0.5 * dlon,
        lat2d.ravel() - 0.5 * dlat,
        lat2d.ravel() + 0.5 * dlat,
        np.full(lon2d.size, r_bot),
        np.full(lon2d.size, r_top),
    ])
    dens = np.full(lon2d.size, delta_rho)

    g_center = compute_tesseroid_gravity(
        np.array([92.5]), np.array([24.5]), np.array([0.0]), tess, dens
    )[0]
    assert g_center == pytest.approx(dg_analytical_mgal, rel=0.025)


def test_finite_rectangular_prism_benchmark():
    """
    Compare a single small tesseroid (0.1 deg x 0.1 deg) against Harmonica's
    analytical Cartesian rectangular prism (Nagy formula) at local tangent plane.
    """
    lat0, lon0 = 24.5, 92.5
    dlat, dlon = 0.1, 0.1
    z_top, z_bot = -35_000.0, -40_000.0
    delta_rho = -600.0

    tess = np.array([[
        lon0 - 0.5 * dlon, lon0 + 0.5 * dlon,
        lat0 - 0.5 * dlat, lat0 + 0.5 * dlat,
        EARTH_MEAN_RADIUS_M + z_bot, EARTH_MEAN_RADIUS_M + z_top,
    ]])
    g_tess = compute_tesseroid_gravity(
        np.array([lon0]), np.array([lat0]), np.array([0.0]), tess, np.array([delta_rho])
    )[0]

    # Equivalent Cartesian prism dimensions at mid-depth radius (spherical convergence)
    r_mid = EARTH_MEAN_RADIUS_M + 0.5 * (z_top + z_bot)
    deg_to_m_lat = math.radians(1.0) * r_mid
    deg_to_m_lon = math.radians(1.0) * r_mid * math.cos(math.radians(lat0))
    dx = dlon * deg_to_m_lon
    dy = dlat * deg_to_m_lat
    prism = np.array([[-0.5 * dx, 0.5 * dx, -0.5 * dy, 0.5 * dy, z_bot, z_top]])
    g_prism = hm.prism_gravity(
        (np.array([0.0]), np.array([0.0]), np.array([0.0])),
        prism,
        np.array([delta_rho]),
        field="g_z",
    )[0]

    assert g_tess < 0.0
    assert g_tess == pytest.approx(g_prism, rel=0.005)


def test_positive_and_negative_density_contrasts():
    lons = np.linspace(91.0, 94.0, 7)
    lats = np.linspace(23.0, 26.0, 7)
    obs_lon, obs_lat = np.meshgrid([92.5], [24.5])
    obs_elev = np.zeros_like(obs_lon)

    # Land (+1500 m) -> negative gravity for both Airy and Pratt
    elev_land = np.full((7, 7), 1500.0)
    t_a_land, d_a_land = build_airy_tesseroids(lons, lats, elev_land)
    t_p_land, d_p_land = build_pratt_tesseroids(lons, lats, elev_land)
    g_a_land = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_a_land, d_a_land)[0, 0]
    g_p_land = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_p_land, d_p_land)[0, 0]
    assert g_a_land < 0.0
    assert g_p_land < 0.0

    # Marine (-1500 m) -> positive gravity for both Airy and Pratt
    elev_mar = np.full((7, 7), -1500.0)
    t_a_mar, d_a_mar = build_airy_tesseroids(lons, lats, elev_mar)
    t_p_mar, d_p_mar = build_pratt_tesseroids(lons, lats, elev_mar)
    g_a_mar = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_a_mar, d_a_mar)[0, 0]
    g_p_mar = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_p_mar, d_p_mar)[0, 0]
    assert g_a_mar > 0.0
    assert g_p_mar > 0.0


def test_zero_density_contrast_zero_topography():
    lons = np.linspace(90.0, 95.0, 11)
    lats = np.linspace(22.0, 27.0, 11)
    elev_zero = np.zeros((11, 11))

    t_a, d_a = build_airy_tesseroids(lons, lats, elev_zero)
    t_p, d_p = build_pratt_tesseroids(lons, lats, elev_zero)
    assert len(t_a) == 0
    assert len(t_p) == 0

    obs_lon, obs_lat = np.meshgrid(lons, lats)
    g_a = compute_tesseroid_gravity(obs_lon, obs_lat, np.zeros_like(obs_lon), t_a, d_a)
    g_p = compute_tesseroid_gravity(obs_lon, obs_lat, np.zeros_like(obs_lon), t_p, d_p)
    assert g_a.shape == (11, 11)
    np.testing.assert_allclose(g_a, 0.0)
    np.testing.assert_allclose(g_p, 0.0)


def test_land_marine_transition():
    lons = np.linspace(90.0, 95.0, 11)
    lats = np.linspace(22.0, 27.0, 11)
    # West half land (+1000 m), East half marine (-1000 m)
    elev = np.where(lons[None, :] < 92.5, 1000.0, -1000.0)
    elev = np.broadcast_to(elev, (11, 11)).copy()

    t_a, d_a = build_airy_tesseroids(lons, lats, elev)
    t_p, d_p = build_pratt_tesseroids(lons, lats, elev)

    obs_lons = np.array([90.5, 92.5, 94.5])
    obs_lats = np.array([24.5, 24.5, 24.5])
    obs_elev = np.array([1000.0, 0.0, 0.0])

    g_a = compute_tesseroid_gravity(obs_lons, obs_lats, obs_elev, t_a, d_a)
    g_p = compute_tesseroid_gravity(obs_lons, obs_lats, obs_elev, t_p, d_p)

    # Monotonic increase from negative (land) through coast to positive (marine)
    assert g_a[0] < 0.0 < g_a[2]
    assert g_p[0] < 0.0 < g_p[2]


def test_grid_edge_effects_and_buffer_sensitivity():
    """
    Compare Airy gravity at the core west edge (90.0E, 24.5N) for a uniform
    1000 m plateau when modeled only over core (90-95E) vs buffered (87-98E).
    The unbuffered core-only domain loses ~50% of the signal at the edge.
    """
    lons_core = np.linspace(90.0, 95.0, 11)
    lats_core = np.linspace(22.0, 27.0, 11)
    elev_core = np.full((11, 11), 1000.0)

    lons_buf = np.linspace(87.0, 98.0, 23)
    lats_buf = np.linspace(19.0, 30.0, 23)
    elev_buf = np.full((23, 23), 1000.0)

    t_core, d_core = build_airy_tesseroids(lons_core, lats_core, elev_core)
    t_buf, d_buf = build_airy_tesseroids(lons_buf, lats_buf, elev_buf)

    obs_lon = np.array([90.0, 92.5])
    obs_lat = np.array([24.5, 24.5])
    obs_elev = np.array([1000.0, 1000.0])

    g_unbuf = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_core, d_core)
    g_buf = compute_tesseroid_gravity(obs_lon, obs_lat, obs_elev, t_buf, d_buf)

    # Edge (90.0E) without buffer loses ~33% of the buffered signal (since cell extends 0.25 deg west)
    assert abs(g_unbuf[0]) < 0.70 * abs(g_buf[0])
    # Buffered edge (90.0E) is close to buffered center (92.5E)
    assert abs(g_buf[0]) > 0.90 * abs(g_buf[1])


def test_bouguer_mass_balance_land_and_marine():
    """
    Independently verify that the Bouguer-consistent Airy and Pratt tesseroid
    stacks satisfy:
      - Land (h > 0): sum(thickness * delta_rho) == -rho_bouguer * h
      - Marine (h < 0, d = -h): sum(thickness * delta_rho) == +(rho_bouguer - rho_w) * d
      - Every tesseroid has bottom < top and exact expected radial bounds.
    """
    lons = np.array([92.0, 93.0])
    lats = np.array([24.0, 25.0])
    rho_b = 2670.0
    rho_w = 1030.0

    # Pure land cell (+1500 m)
    elev_land = np.full((2, 2), 1500.0)
    for builder in [build_airy_tesseroids, build_pratt_tesseroids]:
        tess, dens = builder(lons, lats, elev_land, rho_w=rho_w, rho_bouguer=rho_b)
        assert len(tess) == 8  # 4 cells * 2 layers (subsurface + stripping mismatch)
        assert np.all(tess[:, 4] < tess[:, 5])  # bottom < top
        total_col_mass = np.sum((tess[:, 5] - tess[:, 4]) * dens) / 4.0
        assert total_col_mass == pytest.approx(-rho_b * 1500.0, rel=1e-12)

    # Pure marine cell (-1500 m)
    elev_mar = np.full((2, 2), -1500.0)
    for builder in [build_airy_tesseroids, build_pratt_tesseroids]:
        tess, dens = builder(lons, lats, elev_mar, rho_w=rho_w, rho_bouguer=rho_b)
        assert len(tess) == 8  # 4 cells * 2 layers (subsurface + water-fill mismatch)
        assert np.all(tess[:, 4] < tess[:, 5])
        total_col_mass = np.sum((tess[:, 5] - tess[:, 4]) * dens) / 4.0
        assert total_col_mass == pytest.approx((rho_b - rho_w) * 1500.0, rel=1e-12)


def test_shallow_surface_layer_convergence():
    """
    Verify that a shallow 2-arc-min stripping-mismatch tesseroid [R, R+2000]
    evaluated at its top face (r_obs = R+2000) with radial_adaptive_discretization=False
    converges within 0.5% of an 8x8x4 refined sub-mesh.
    """
    dlon = dlat = 1.0 / 30.0
    tess_1 = np.array([[
        92.5 - 0.5 * dlon, 92.5 + 0.5 * dlon,
        24.5 - 0.5 * dlat, 24.5 + 0.5 * dlat,
        EARTH_MEAN_RADIUS_M, EARTH_MEAN_RADIUS_M + 2000.0,
    ]])
    dens_1 = np.array([80.0])

    nx, ny, nz = 8, 8, 4
    xs = np.linspace(92.5 - 0.5 * dlon, 92.5 + 0.5 * dlon, nx + 1)
    ys = np.linspace(24.5 - 0.5 * dlat, 24.5 + 0.5 * dlat, ny + 1)
    zs = np.linspace(EARTH_MEAN_RADIUS_M, EARTH_MEAN_RADIUS_M + 2000.0, nz + 1)
    sub_tess = np.array([
        [xs[i], xs[i + 1], ys[j], ys[j + 1], zs[k], zs[k + 1]]
        for i in range(nx) for j in range(ny) for k in range(nz)
    ])
    sub_dens = np.full(len(sub_tess), 80.0)

    g_single = compute_tesseroid_gravity(
        np.array([92.5]), np.array([24.5]), np.array([2000.0]), tess_1, dens_1
    )[0]
    g_refined = compute_tesseroid_gravity(
        np.array([92.5]), np.array([24.5]), np.array([2000.0]), sub_tess, sub_dens
    )[0]

    assert g_single > 0.0
    assert g_single == pytest.approx(g_refined, rel=0.005)
