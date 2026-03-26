"""
InfrastructurePredictor - ML model for predicting infrastructure needs
More sophisticated than simple population/ratio formulas
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODEL_PATH_INFRA = os.path.join(os.path.dirname(__file__), "models", "infra_predictor.pkl")


class InfrastructurePredictor:
    """
    Predicts optimal number of:
    - Schools (considering existing schools in zone)
    - Hospitals (considering distance to existing)
    - Parks (based on density and green space)
    - Petrol pumps (based on road network and traffic)
    """

    def __init__(self):
        self.models = {}
        self._try_load()

    def generate_training_data(self, n_samples=3000):
        """Generate realistic infrastructure demand data"""
        np.random.seed(42)
        data = []

        for _ in range(n_samples):
            # Wider range for better training
            population = np.random.randint(1000, 150000)
            density = np.random.uniform(0.0005, 0.0045)
            area_acres = np.random.uniform(5, 2000)
            green_pct = np.random.uniform(0.08, 0.28)
            existing_schools = np.random.randint(0, 8)
            existing_hospitals = np.random.randint(0, 5)
            dist_to_hospital = np.random.uniform(0.3, 8)
            dist_to_school = np.random.uniform(0.2, 5)

            # ============================================================
            # Schools calculation - ALWAYS at least 1 if population > 0
            # ============================================================
            # Base schools needed: 1 per 5000 people
            base_schools = max(1, int(np.ceil(population / 5000)))
            # Adjust for existing schools
            schools_needed = max(1, base_schools - existing_schools)
            # If distance to school is far, add more schools
            if dist_to_school > 2:
                schools_needed += 1

            # ============================================================
            # Hospitals calculation - ALWAYS at least 1 if population > 0
            # ============================================================
            base_hospitals = max(1, int(np.ceil(population / 15000)))
            hospitals_needed = max(1, base_hospitals - existing_hospitals)
            if dist_to_hospital > 3:
                hospitals_needed += 1

            # ============================================================
            # Parks calculation - 1 per 3000 people, minimum 2
            # ============================================================
            parks_needed = max(2, int(np.ceil(population / 3000)))
            if green_pct > 0.20:
                parks_needed = max(2, parks_needed - 1)

            # ============================================================
            # Petrol pumps calculation - 1 per 25000 people, minimum 1
            # ============================================================
            pumps_needed = max(1, int(np.ceil(population / 25000)))

            data.append({
                'population': population,
                'density_ppsf': density,
                'area_acres': area_acres,
                'green_pct': green_pct,
                'existing_schools': existing_schools,
                'existing_hospitals': existing_hospitals,
                'dist_to_nearest_hospital': dist_to_hospital,
                'dist_to_nearest_school': dist_to_school,
                'schools_needed': min(8, schools_needed),  # Cap at 8
                'hospitals_needed': min(5, hospitals_needed),  # Cap at 5
                'parks_needed': min(10, parks_needed),  # Cap at 10
                'pumps_needed': min(6, pumps_needed),  # Cap at 6
            })

        return pd.DataFrame(data)

    def train_model(self):
        """Train all infrastructure prediction models"""
        print("Training Infrastructure Predictor...")
        df = self.generate_training_data()

        features = ['population', 'density_ppsf', 'area_acres', 'green_pct',
                    'existing_schools', 'existing_hospitals',
                    'dist_to_nearest_hospital', 'dist_to_nearest_school']

        X = df[features]

        targets = ['schools_needed', 'hospitals_needed', 'parks_needed', 'pumps_needed']

        for target in targets:
            model = Pipeline([
                ('scaler', StandardScaler()),
                ('rf', RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42))
            ])
            model.fit(X, df[target])
            self.models[target] = model

        self._save_model()
        print(f"✅ Infrastructure Predictor trained on {len(df)} samples!")

        # Print sample predictions for verification
        sample = df.head(3)
        print("\n📊 Sample predictions:")
        for _, row in sample.iterrows():
            print(f"   Population: {row['population']:,} → Schools: {int(row['schools_needed'])}, "
                  f"Hospitals: {int(row['hospitals_needed'])}, Parks: {int(row['parks_needed'])}")

    def predict(self, population, density, area_acres, green_pct,
                existing_schools, existing_hospitals,
                dist_to_hospital, dist_to_school):
        """
        Predict infrastructure needs with minimum guarantees as per UDPFI

        As per PDF requirement:
        - Schools: 1 per 5000 people (minimum 1)
        - Hospitals: 1 per 15000 people (minimum 1)
        - Parks: 1 per 3000 people (minimum 2)
        - Petrol Pumps: 1 per 25000 people (minimum 1)
        """
        if not self.models:
            self.train_model()

        features = pd.DataFrame([[
            population, density, area_acres, green_pct,
            existing_schools, existing_hospitals,
            dist_to_hospital, dist_to_school
        ]])

        # Get predictions
        schools_pred = self.models['schools_needed'].predict(features)[0]
        hospitals_pred = self.models['hospitals_needed'].predict(features)[0]
        parks_pred = self.models['parks_needed'].predict(features)[0]
        pumps_pred = self.models['pumps_needed'].predict(features)[0]

        # ============================================================
        # FIX: As per UDPFI Guidelines and PDF requirement
        # Minimum 1 school, 1 hospital, 1 petrol pump, 2 parks
        # ============================================================

        # Schools: Minimum 1 always (as per PDF example)
        if population > 0:
            schools = max(1, int(round(schools_pred)))
        else:
            schools = 0

        # Hospitals: Minimum 1 always (as per PDF example with 750 population)
        if population > 0:
            hospitals = max(1, int(round(hospitals_pred)))
        else:
            hospitals = 0

        # Parks: Minimum 2 always (as per PDF example)
        parks = max(2, int(round(parks_pred)))

        # Petrol Pumps: Minimum 1 always (as per PDF example)
        if population > 0:
            petrol_pumps = max(1, int(round(pumps_pred)))
        else:
            petrol_pumps = 0

        return {
            'schools': schools,
            'hospitals': hospitals,
            'parks': parks,
            'petrol_pumps': petrol_pumps,
        }

    def _save_model(self):
        os.makedirs(os.path.dirname(MODEL_PATH_INFRA), exist_ok=True)
        joblib.dump(self.models, MODEL_PATH_INFRA)

    def _try_load(self):
        try:
            self.models = joblib.load(MODEL_PATH_INFRA)
            print("✅ Loaded existing Infrastructure Predictor model")
        except:
            self.models = {}
            print("⚠️ No existing Infrastructure model found. Will train on first use.")