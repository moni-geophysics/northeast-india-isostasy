"""
Isostatic compensation modeling and Moho depth calculation subpackage.
"""

from pathlib import Path
import yaml

from src.isostasy.airy import (
    airy_root_land,
    airy_root_marine,
    compute_airy_isostasy,
)
from src.isostasy.pratt import (
    compute_pratt_isostasy,
    pratt_density_land,
    pratt_density_marine,
)


def load_model_parameters(config_path: str | Path = "config/model_parameters.yaml") -> dict:
    """Load literature-grounded Airy and Pratt parameters from YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


__all__ = [
    "airy_root_land",
    "airy_root_marine",
    "compute_airy_isostasy",
    "pratt_density_land",
    "pratt_density_marine",
    "compute_pratt_isostasy",
    "load_model_parameters",
]
