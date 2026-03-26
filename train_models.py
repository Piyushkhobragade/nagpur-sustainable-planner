"""
Run this once to train all ML models
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_model import DensityPredictor
from ml_landuse import LandUsePredictor
from ml_infrastructure import InfrastructurePredictor

print("=" * 60)
print("🚀 Training all ML models for Nagpur Sustainable Planner")
print("=" * 60)

# Train Density Predictor (if not already trained)
print("\n📊 1. Training Density Predictor...")
density = DensityPredictor()
if density.model is None:
    metrics = density.train_model()
    print(f"   ✅ R² Score: {metrics['r2']:.3f}")
    print(f"   ✅ MAE: {metrics['mae']:.5f}")
else:
    print("   ✅ Density model already exists!")

# Train Land Use Predictor
print("\n🏠 2. Training Land Use Predictor...")
landuse = LandUsePredictor()
landuse.train_model()

# Train Infrastructure Predictor
print("\n🏥 3. Training Infrastructure Predictor...")
infra = InfrastructurePredictor()
infra.train_model()

print("\n" + "=" * 60)
print("✅ All models trained successfully!")
print("📁 Models saved in 'models/' folder:")
print("   - density_predictor.pkl (already existed)")
print("   - landuse_predictor.pkl (new)")
print("   - infra_predictor.pkl (new)")
print("=" * 60)
print("\n🎯 Now you can run the app:")
print("   streamlit run app.py")
print("=" * 60)