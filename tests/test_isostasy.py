"""
Comprehensive unit tests for Airy-Heiskanen and Pratt-Hayford local isostasy models.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from src.isostasy import (
    airy_root_land,
    airy_root_marine,
    compute_airy_isostasy,
    compute_pratt_isostasy,
    load_model_parameters,
    pratt_density_land,
    pratt_density_marine,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_zero_topography_reference_case():
    airy = compute_airy_isostasy(0.0, t0_km=35.0, rho_c=2750.0, rho_m=3350.0, rho_w=1030.0)
    assert airy["root_thickness_km"] == pytest.approx(0.0)
    assert airy["moho_depth_sl_km"] == pytest.approx(35.0)
    assert airy["moho_elevation_km"] == pytest.approx(-35.0)
    assert airy["total_crustal_thickness_km"] == pytest.approx(35.0)
    assert airy["is_marine"] is False

    pratt = compute_pratt_isostasy(0.0, d_km=100.0, rho_0=3100.0, rho_w=1030.0)
    assert pratt["pratt_density_kgm3"] == pytest.approx(3100.0)
    assert pratt["density_anomaly_kgm3"] == pytest.approx(0.0)
    assert pratt["is_marine"] is False


def test_positive_elevation_analytical_benchmark():
    # h = +1200 m = +1.2 km
    # Airy: b = (2750 / 600) * 1.2 = 5.5 km; D_Moho,SL = 40.5 km; T_c = 41.7 km
    airy = compute_airy_isostasy(1200.0, t0_km=35.0, rho_c=2750.0, rho_m=3350.0, rho_w=1030.0)
    assert airy["root_thickness_km"] == pytest.approx(5.5)
    assert airy["moho_depth_sl_km"] == pytest.approx(40.5)
    assert airy["moho_elevation_km"] == pytest.approx(-40.5)
    assert airy["total_crustal_thickness_km"] == pytest.approx(41.7)
    assert airy["is_marine"] is False

    # Pratt: rho = 3100 * 100 / 101.2 = 3063.2411067...
    pratt = compute_pratt_isostasy(1200.0, d_km=100.0, rho_0=3100.0, rho_w=1030.0)
    expected_rho = 3100.0 * (100.0 / 101.2)
    assert pratt["pratt_density_kgm3"] == pytest.approx(expected_rho)
    assert pratt["density_anomaly_kgm3"] == pytest.approx(expected_rho - 3100.0)


def test_negative_bathymetry_analytical_benchmark():
    # h = -2000 m = -2.0 km (water depth d_w = 2.0 km)
    # Airy: b = ((2750 - 1030) / 600) * (-2.0) = -5.733333... km
    # D_Moho,SL = 35.0 - 5.733333... = 29.266666... km
    # Solid crustal thickness T_c = -2.0 + 29.266666... = 27.266666... km
    airy = compute_airy_isostasy(-2000.0, t0_km=35.0, rho_c=2750.0, rho_m=3350.0, rho_w=1030.0)
    expected_b = ((2750.0 - 1030.0) / 600.0) * (-2.0)
    assert airy["root_thickness_km"] == pytest.approx(expected_b)
    assert airy["moho_depth_sl_km"] == pytest.approx(35.0 + expected_b)
    assert airy["moho_elevation_km"] == pytest.approx(-(35.0 + expected_b))
    assert airy["total_crustal_thickness_km"] == pytest.approx(35.0 + expected_b - 2.0)
    assert airy["is_marine"] is True

    # Pratt: rho = (3100*100 - 1030*2) / (100 - 2) = 307940 / 98 = 3142.244898...
    pratt = compute_pratt_isostasy(-2000.0, d_km=100.0, rho_0=3100.0, rho_w=1030.0)
    expected_rho = (3100.0 * 100.0 - 1030.0 * 2.0) / 98.0
    assert pratt["pratt_density_kgm3"] == pytest.approx(expected_rho)
    assert pratt["is_marine"] is True


def test_land_ocean_transition_and_domain_guards():
    with pytest.raises(ValueError):
        airy_root_land(-10.0)
    with pytest.raises(ValueError):
        airy_root_marine(10.0)
    with pytest.raises(ValueError):
        pratt_density_land(-10.0)
    with pytest.raises(ValueError):
        pratt_density_marine(10.0)
    with pytest.raises(ValueError):
        pratt_density_marine(-100000.0, d_km=100.0)

    elevs = np.array([-1000.0, -0.001, 0.0, 0.001, 1000.0])
    airy = compute_airy_isostasy(elevs)
    assert list(airy["is_marine"]) == [True, True, False, False, False]
    # Continuity near h = 0
    assert airy["moho_depth_sl_km"][2] == pytest.approx(35.0)
    assert abs(airy["moho_depth_sl_km"][1] - 35.0) < 1e-5
    assert abs(airy["moho_depth_sl_km"][3] - 35.0) < 1e-5


def test_equal_mass_balance_at_compensation_depth():
    t0_km, rho_c, rho_m, rho_w = 35.0, 2750.0, 3350.0, 1030.0
    z_comp_km = 70.0  # Deeper than deepest root
    m_ref_airy = rho_c * t0_km + rho_m * (z_comp_km - t0_km)

    for h_m in [-3000.0, -500.0, 0.0, 500.0, 2500.0, 5000.0]:
        res = compute_airy_isostasy(h_m, t0_km=t0_km, rho_c=rho_c, rho_m=rho_m, rho_w=rho_w)
        water_col = max(0.0, -h_m / 1000.0)
        mantle_col = z_comp_km - res["moho_depth_sl_km"]
        mass = rho_w * water_col + rho_c * res["total_crustal_thickness_km"] + rho_m * mantle_col
        assert mass == pytest.approx(m_ref_airy, rel=1e-12)

    d_km, rho_0 = 100.0, 3100.0
    m_ref_pratt = rho_0 * d_km
    for h_m in [-3000.0, -500.0, 0.0, 500.0, 2500.0, 5000.0]:
        res = compute_pratt_isostasy(h_m, d_km=d_km, rho_0=rho_0, rho_w=rho_w)
        h_km = h_m / 1000.0
        water_col = max(0.0, -h_km)
        rock_col = d_km + h_km
        mass = rho_w * water_col + res["pratt_density_kgm3"] * rock_col
        assert mass == pytest.approx(m_ref_pratt, rel=1e-12)


def test_vertical_datum_conversions():
    elevs = np.array([-1500.0, 0.0, 1500.0, 4000.0])
    airy = compute_airy_isostasy(elevs)
    h_km = elevs / 1000.0
    np.testing.assert_allclose(airy["moho_depth_sl_km"], -airy["moho_elevation_km"])
    np.testing.assert_allclose(airy["total_crustal_thickness_km"] - h_km, airy["moho_depth_sl_km"])


def test_physical_consistency_and_monotonicity():
    elevs = np.array([-2000.0, -500.0, 0.0, 500.0, 2000.0])
    airy = compute_airy_isostasy(elevs)
    pratt = compute_pratt_isostasy(elevs)
    # Increasing elevation -> monotonically deeper Moho & monotonically lower Pratt density
    assert np.all(np.diff(airy["moho_depth_sl_km"]) > 0.0)
    assert np.all(np.diff(pratt["pratt_density_kgm3"]) < 0.0)


def test_missing_values_preserved():
    elevs = np.array([-500.0, np.nan, 0.0, 1000.0, np.nan])
    airy = compute_airy_isostasy(elevs)
    pratt = compute_pratt_isostasy(elevs)

    for key in ["root_thickness_km", "moho_depth_sl_km", "moho_elevation_km", "total_crustal_thickness_km"]:
        assert np.isnan(airy[key][1])
        assert np.isnan(airy[key][4])
        assert np.isfinite(airy[key][0])
        assert np.isfinite(airy[key][2])

    for key in ["pratt_density_kgm3", "density_anomaly_kgm3"]:
        assert np.isnan(pratt[key][1])
        assert np.isnan(pratt[key][4])
        assert np.isfinite(pratt[key][0])
        assert np.isfinite(pratt[key][2])


def test_xarray_coordinate_preservation_on_core_etopo1():
    etopo_path = PROJECT_ROOT / "data/processed/gravity/WGM2012_ETOPO1_core_22_27N_90_95E.nc"
    with xr.open_dataset(etopo_path) as ds:
        da = ds["z"]
        airy_ds = compute_airy_isostasy(da)
        pratt_ds = compute_pratt_isostasy(da)

        assert isinstance(airy_ds, xr.Dataset)
        assert isinstance(pratt_ds, xr.Dataset)
        assert list(airy_ds.dims) == list(da.dims)
        np.testing.assert_allclose(airy_ds["x"].values, da["x"].values)
        np.testing.assert_allclose(airy_ds["y"].values, da["y"].values)
        assert int(airy_ds["is_marine"].sum()) == 572
        assert int(pratt_ds["is_marine"].sum()) == 572


def test_parameter_sensitivity_and_yaml_config():
    params = load_model_parameters(PROJECT_ROOT / "config/model_parameters.yaml")
    assert params["airy"]["reference_thickness_T0"]["value"] == 35.0
    assert params["densities"]["crust"]["value"] == 2750.0
    assert params["densities"]["mantle"]["value"] == 3350.0
    assert params["densities"]["seawater"]["value"] == 1030.0
    assert params["pratt"]["compensation_depth_D"]["value"] == 100.0
    assert params["pratt"]["reference_density_rho0"]["value"] == 3100.0

    # Smaller density contrast -> larger Airy root for same elevation
    a_low_dr = compute_airy_isostasy(1500.0, rho_c=2800.0, rho_m=3300.0)   # dr = 500
    a_high_dr = compute_airy_isostasy(1500.0, rho_c=2700.0, rho_m=3400.0)  # dr = 700
    assert a_low_dr["root_thickness_km"] > a_high_dr["root_thickness_km"]

    # Deeper Pratt compensation depth -> smaller density anomaly for same elevation
    p_shallow = compute_pratt_isostasy(1500.0, d_km=60.0)
    p_deep = compute_pratt_isostasy(1500.0, d_km=120.0)
    assert abs(p_shallow["density_anomaly_kgm3"]) > abs(p_deep["density_anomaly_kgm3"])
