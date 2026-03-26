"""
LandUsePredictor - ML model for predicting optimal land use percentages
Based on location characteristics, development type, and priority
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODEL_PATH_LANDUSE = os.path.join(os.path.dirname(__file__), "models", "landuse_predictor.pkl")

class LandUsePredictor:
    """
    Predicts optimal percentages for:
    - Residential %
    - Green Space %
    - Road %
    - Facility %
    """
    
    FEATURES = [
        'dist_to_center_km',
        'zone_density_factor',
        'dev_type_encoded',
        'priority_encoded',
        'area_acres_log',
        'population_density_ward',
    ]
    
    def __init__(self):
        self.model = None
        self._try_load()
    
    def generate_training_data(self, n_samples=3000):
        """
        Generate realistic training data based on UDPFI guidelines
        and Nagpur city patterns
        """
        np.random.seed(42)
        data = []
        
        # Zone types with their characteristics
        zones = [
            {'name': 'High Density', 'density': 0.0032, 'base_res': 0.35, 'base_green': 0.12},
            {'name': 'Medium Density', 'density': 0.0020, 'base_res': 0.50, 'base_green': 0.17},
            {'name': 'Low Density', 'density': 0.0010, 'base_res': 0.60, 'base_green': 0.20},
            {'name': 'Commercial', 'density': 0.0030, 'base_res': 0.20, 'base_green': 0.10},
            {'name': 'Industrial', 'density': 0.0008, 'base_res': 0.15, 'base_green': 0.08},
        ]
        
        dev_types = {'Residential': 2, 'Mixed': 1, 'Commercial': 0}
        priorities = {'Max Green Space': 2, 'Balanced': 1, 'Max Housing': 0}
        
        for _ in range(n_samples):
            # Random inputs
            zone = np.random.choice(len(zones))
            dist_to_center = np.random.uniform(0.5, 15.0)
            dev_type = np.random.choice(list(dev_types.keys()))
            priority = np.random.choice(list(priorities.keys()))
            area_acres = np.random.uniform(1, 500)
            area_log = np.log1p(area_acres)
            
            zone_data = zones[zone]
            
            # Calculate target percentages based on rules + noise
            # This creates realistic training data
            
            # Base from zone type
            if zone_data['name'] == 'High Density':
                res_base = 0.35
                green_base = 0.12
            elif zone_data['name'] == 'Medium Density':
                res_base = 0.50
                green_base = 0.17
            elif zone_data['name'] == 'Low Density':
                res_base = 0.60
                green_base = 0.20
            else:
                res_base = 0.25
                green_base = 0.10
            
            # Adjust for development type
            if dev_type == 'Residential':
                res_adj = +0.10
                green_adj = +0.03
            elif dev_type == 'Commercial':
                res_adj = -0.20
                green_adj = -0.04
            else:  # Mixed
                res_adj = -0.05
                green_adj = -0.01
            
            # Adjust for priority
            if priority == 'Max Green Space':
                green_adj += 0.05
                res_adj -= 0.05
            elif priority == 'Max Housing':
                res_adj += 0.08
                green_adj -= 0.03
            
            # Distance factor - farther from center = more green space
            dist_factor = min(0.10, dist_to_center / 100)
            green_adj += dist_factor
            
            # Final percentages
            residential_pct = np.clip(res_base + res_adj + np.random.normal(0, 0.02), 0.15, 0.70)
            green_pct = np.clip(green_base + green_adj + np.random.normal(0, 0.01), 0.08, 0.25)
            road_pct = np.clip(0.15 + np.random.normal(0, 0.01), 0.12, 0.18)
            facility_pct = np.clip(0.10 + np.random.normal(0, 0.005), 0.08, 0.12)
            
            # Normalize to sum to 1 (excluding open space)
            total = residential_pct + green_pct + road_pct + facility_pct
            residential_pct /= total
            green_pct /= total
            road_pct /= total
            facility_pct /= total
            
            data.append({
                'dist_to_center_km': dist_to_center,
                'zone_density_factor': zone_data['density'],
                'dev_type_encoded': dev_types[dev_type],
                'priority_encoded': priorities[priority],
                'area_acres_log': area_log,
                'population_density_ward': zone_data['density'] * 1000,
                'residential_pct': residential_pct,
                'green_pct': green_pct,
                'road_pct': road_pct,
                'facility_pct': facility_pct,
            })
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the land use prediction model"""
        df = self.generate_training_data()
        
        X = df[self.FEATURES]
        y_res = df['residential_pct']
        y_green = df['green_pct']
        y_road = df['road_pct']
        y_facility = df['facility_pct']
        
        # Train separate models for each output
        self.model_res = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42))
        ])
        
        self.model_green = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42))
        ])
        
        self.model_road = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42))
        ])
        
        self.model_facility = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42))
        ])
        
        self.model_res.fit(X, y_res)
        self.model_green.fit(X, y_green)
        self.model_road.fit(X, y_road)
        self.model_facility.fit(X, y_facility)
        
        self._save_model()
        
        return {
            'res_r2': self.model_res.score(X, y_res),
            'green_r2': self.model_green.score(X, y_green),
        }
    
    def predict(self, dist_to_center, zone_density, dev_type, priority, area_acres):
        """
        Predict land use percentages
        """
        if self.model_res is None:
            self.train_model()
        
        dev_encoding = {'Residential': 2, 'Mixed': 1, 'Commercial': 0}.get(dev_type, 1)
        priority_encoding = {'Max Green Space': 2, 'Balanced': 1, 'Max Housing': 0}.get(priority, 1)
        
        features = pd.DataFrame([[
            dist_to_center,
            zone_density,
            dev_encoding,
            priority_encoding,
            np.log1p(area_acres),
            zone_density * 1000,
        ]], columns=self.FEATURES)
        
        return {
            'residential_pct': float(self.model_res.predict(features)[0]),
            'green_pct': float(self.model_green.predict(features)[0]),
            'road_pct': float(self.model_road.predict(features)[0]),
            'facility_pct': float(self.model_facility.predict(features)[0]),
        }
    
    def _save_model(self):
        os.makedirs(os.path.dirname(MODEL_PATH_LANDUSE), exist_ok=True)
        joblib.dump({
            'res': self.model_res,
            'green': self.model_green,
            'road': self.model_road,
            'facility': self.model_facility,
        }, MODEL_PATH_LANDUSE)
    
    def _try_load(self):
        try:
            models = joblib.load(MODEL_PATH_LANDUSE)
            self.model_res = models['res']
            self.model_green = models['green']
            self.model_road = models['road']
            self.model_facility = models['facility']
        except:
            self.model_res = None