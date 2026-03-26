"""
DataLoader – loads all static and synthetic datasets for the planner.
"""

import os
import pandas as pd
import numpy as np
from utils.constants import NAGPUR_ZONES, NAGPUR_CENTER

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class DataLoader:
    """Loads and caches all data needed by the planner."""

    def __init__(self):
        self._density_df: pd.DataFrame | None = None
        self._amenities_df: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_density_data(self) -> pd.DataFrame:
        """Load ward-level population density data."""
        if self._density_df is not None:
            return self._density_df

        path = os.path.join(DATA_DIR, "density_data.csv")
        try:
            self._density_df = pd.read_csv(path)
        except FileNotFoundError:
            self._density_df = self._generate_density_data()
        return self._density_df

    def load_amenities(self) -> pd.DataFrame:
        """Load amenities (schools, hospitals, parks, petrol pumps)."""
        if self._amenities_df is not None:
            return self._amenities_df

        path = os.path.join(DATA_DIR, "amenities.csv")
        try:
            self._amenities_df = pd.read_csv(path)
        except FileNotFoundError:
            self._amenities_df = self._generate_amenities_data()
        return self._amenities_df

    def get_nagpur_zones(self) -> list[str]:
        """Return sorted list of available zone names."""
        return sorted(NAGPUR_ZONES.keys())

    def get_coordinates_for_zone(self, zone: str) -> list[float]:
        """Return [lat, lon] for the given zone, defaulting to city centre."""
        info = NAGPUR_ZONES.get(zone)
        if info:
            return [info["lat"], info["lon"]]
        return NAGPUR_CENTER

    def get_zone_info(self, zone: str) -> dict:
        """Return full zone metadata dict."""
        return NAGPUR_ZONES.get(zone, {})

    def get_density_factor(self, zone: str) -> float:
        """Return people-per-sq-ft density factor for the zone."""
        info = NAGPUR_ZONES.get(zone)
        if info:
            return info["density_factor"]
        return 0.0015  # fallback medium density

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_density_data() -> pd.DataFrame:
        """Fallback: generate density data from constants."""
        rows = []
        for name, info in NAGPUR_ZONES.items():
            rows.append({
                "ward_name": name,
                "population_density": info["density_factor"],
                "area_sq_km": round(np.random.uniform(3, 12), 1),
                "population": int(info["density_factor"] * 1_000_000 * 15),
                "center_latitude": info["lat"],
                "center_longitude": info["lon"],
            })
        return pd.DataFrame(rows)

    @staticmethod
    def _generate_amenities_data() -> pd.DataFrame:
        """Fallback: generate minimal amenities dataframe."""
        rows = []
        for zone, info in NAGPUR_ZONES.items():
            rows.append({"type": "School", "name": f"{zone} School",
                         "latitude": info["lat"] + 0.002, "longitude": info["lon"] + 0.002,
                         "ward": zone, "capacity": 700})
            rows.append({"type": "Hospital", "name": f"{zone} Hospital",
                         "latitude": info["lat"] - 0.002, "longitude": info["lon"] - 0.002,
                         "ward": zone, "capacity": 300})
            rows.append({"type": "Park", "name": f"{zone} Park",
                         "latitude": info["lat"] + 0.003, "longitude": info["lon"] - 0.003,
                         "ward": zone, "capacity": 0})
        return pd.DataFrame(rows)
