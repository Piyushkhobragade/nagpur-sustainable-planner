"""
DensityPredictor – ML model that predicts optimal population density
for a zone based on location and proximity features.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

from utils.constants import NAGPUR_ZONES, NAGPUR_CENTER
from utils.helpers import haversine_distance

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "density_predictor.pkl")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)


class DensityPredictor:
    """
    Random-Forest-based density predictor.
    Features: distance_to_center, avg_school_dist, avg_hospital_dist,
              land_price_index, existing_density, zone_type_encoded,
              area_sqft_log.
    Target:   Optimal population density (people per sq ft).
    """

    FEATURE_NAMES = [
        "dist_to_center_km",
        "avg_school_dist_km",
        "avg_hospital_dist_km",
        "land_price_index",
        "existing_density",
        "zone_type_encoded",
        "area_sqft_log",
    ]

    ZONE_TYPE_MAP = {
        "High Density Residential":    5,
        "High Density Commercial":     5,
        "High Density Old City":       5,
        "High Density Mixed":          5,
        "Medium Density Administrative": 3,
        "Medium Density Residential":  3,
        "Mixed Use":                   3,
        "Low Density Residential":     2,
        "Industrial":                  1,
        "Developing Area":             1,
    }

    def __init__(self):
        self.model: Pipeline | None = None
        self._try_load()

    # ------------------------------------------------------------------

    def generate_synthetic_data(self, n_samples: int = 2000) -> pd.DataFrame:
        """
        Generate realistic training data where target density is computed
        from a FORMULA based on features — not just copied from input.
        """
        rng = np.random.default_rng(42)
        rows = []

        zone_list = list(NAGPUR_ZONES.values())

        density_ceiling = {
            5: 0.0038,
            3: 0.0022,
            2: 0.0013,
            1: 0.0008,
        }

        for _ in range(n_samples):
            z = zone_list[rng.integers(len(zone_list))]
            dist_c = haversine_distance(z["lat"], z["lon"], *NAGPUR_CENTER)

            school_d  = max(0.1, dist_c * 0.35 + rng.uniform(-0.5, 0.5))
            hosp_d    = max(0.2, dist_c * 0.55 + rng.uniform(-0.6, 0.6))
            lpi       = float(np.clip(1.0 - dist_c / 14.0 + rng.normal(0, 0.08), 0.05, 1.0))
            zone_enc  = self.ZONE_TYPE_MAP.get(z["type"], 3)
            area_sqft = float(rng.uniform(10_000, 5_000_000))
            area_log  = np.log1p(area_sqft)

            base          = density_ceiling.get(zone_enc, 0.0015)
            center_factor = max(0.4, 1.0 - (dist_c / 12.0) * 0.5)
            school_factor = max(0.7, 1.0 - school_d * 0.06)
            hosp_factor   = max(0.7, 1.0 - hosp_d * 0.04)
            price_factor  = 0.8 + lpi * 0.4
            area_factor   = max(0.75, 1.0 - (area_log / 25.0) * 0.15)

            target = base * center_factor * school_factor * hosp_factor * price_factor * area_factor
            target = float(np.clip(target + rng.normal(0, target * 0.05), 0.0002, 0.0045))

            rows.append({
                "dist_to_center_km":    dist_c,
                "avg_school_dist_km":   school_d,
                "avg_hospital_dist_km": hosp_d,
                "land_price_index":     lpi,
                "existing_density":     z["density_factor"],
                "zone_type_encoded":    zone_enc,
                "area_sqft_log":        area_log,
                "target_density":       target,
            })

        return pd.DataFrame(rows)

    def train_model(self) -> dict:
        """Train and save the model. Returns evaluation metrics."""
        df = self.generate_synthetic_data()
        X = df[self.FEATURE_NAMES]
        y = df["target_density"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestRegressor(
                n_estimators=150, max_depth=8,
                min_samples_leaf=4, random_state=42, n_jobs=-1
            )),
        ])
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        metrics = {
            "mae": mean_absolute_error(y_test, y_pred),
            "r2":  r2_score(y_test, y_pred),
            "test_samples": len(y_test),
        }

        self.model = pipe
        self.save_model()
        return metrics

    def predict_density(
        self,
        lat: float,
        lon: float,
        existing_density: float,
        zone_type: str,
        area_sqft: float,
        # FIX: Added override params so What-If sliders in app.py actually
        # feed into the prediction instead of being silently ignored.
        dist_km_override: float | None = None,
        lpi_override: float | None = None,
    ) -> dict:
        """
        Predict optimal density for given location features.

        Args:
            lat, lon:           Zone coordinates.
            existing_density:   Zone's base density factor.
            zone_type:          Zone type string (maps to encoded int).
            area_sqft:          Plot area.
            dist_km_override:   If provided, overrides the computed distance
                                to city centre (used by What-If analysis).
            lpi_override:       If provided, overrides the computed land price
                                index (used by What-If analysis).

        Returns:
            dict with prediction and interpretation.
        """
        if self.model is None:
            self.train_model()

        # Compute base values from coordinates
        dist_c   = haversine_distance(lat, lon, *NAGPUR_CENTER)
        school_d = max(0.1, dist_c * 0.4)
        hosp_d   = max(0.1, dist_c * 0.6)
        lpi      = max(0.1, 1.0 - dist_c / 15.0)

        # FIX: Apply overrides when provided (What-If sliders)
        if dist_km_override is not None:
            dist_c   = dist_km_override
            school_d = max(0.1, dist_c * 0.4)
            hosp_d   = max(0.1, dist_c * 0.6)
            # Recompute lpi from overridden distance unless lpi also overridden
            lpi = max(0.1, 1.0 - dist_c / 15.0)
        if lpi_override is not None:
            lpi = lpi_override

        zone_enc = self.ZONE_TYPE_MAP.get(zone_type, 3)
        area_log = np.log1p(area_sqft)

        features = pd.DataFrame([[
            dist_c, school_d, hosp_d, lpi,
            existing_density, zone_enc, area_log
        ]], columns=self.FEATURE_NAMES)

        predicted = float(self.model.predict(features)[0])
        diff_pct  = ((predicted - existing_density) / max(existing_density, 1e-9)) * 100

        return {
            "predicted_density":      round(predicted, 6),
            "existing_density":       round(existing_density, 6),
            "difference_pct":         round(diff_pct, 1),
            "recommendation":         self._interpret(predicted, existing_density),
            "distance_to_center_km":  round(dist_c, 2),
        }

    def get_feature_importance(self) -> pd.Series:
        """Return feature importances as a named Series."""
        if self.model is None:
            return pd.Series(dtype=float)
        rf = self.model.named_steps["rf"]
        return pd.Series(rf.feature_importances_, index=self.FEATURE_NAMES).sort_values(ascending=False)

    def save_model(self):
        """Persist model to disk."""
        if self.model:
            joblib.dump(self.model, MODEL_PATH)

    def _try_load(self):
        """Attempt to load pre-trained model silently."""
        try:
            self.model = joblib.load(MODEL_PATH)
        except Exception:
            self.model = None

    @staticmethod
    def _interpret(predicted: float, existing: float) -> str:
        diff = predicted - existing
        if diff > 0.0005:
            return "📈 ML suggests higher density is sustainable here."
        elif diff < -0.0005:
            return "📉 ML recommends reducing density for sustainability."
        return "✅ Current density aligns with ML recommendation."
