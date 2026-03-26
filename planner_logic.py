"""
SustainablePlanner – core calculation engine.
All area inputs/outputs are in square feet unless stated otherwise.

UPDATED: Now uses ML models for:
- Land use distribution (residential/green/road/facility %)
- Infrastructure demand (schools, hospitals, parks, pumps)
- Density prediction (existing)
"""

import math
import numpy as np
from dataclasses import dataclass, field
from utils.constants import (
    AVERAGE_FAMILY_SIZE, AVERAGE_HOUSE_SIZE_SQFT,
    RESIDENTIAL_AREA_RATIO, GREEN_SPACE_RATIO_MIN, GREEN_SPACE_RATIO_MAX,
    ROAD_AREA_RATIO, FACILITY_AREA_RATIO,
    SCHOOL_PER_POPULATION, HOSPITAL_PER_POPULATION,
    PETROL_PUMP_PER_POPULATION, PARK_PER_POPULATION,
    COMMUNITY_HALL_PER_POPULATION,
    HOUSE_COVERAGE_RATIO,
    COMPLIANCE, SUSTAINABILITY_WEIGHTS,
    NAGPUR_CENTER,
)
from data_loader import DataLoader
from utils.helpers import percentage, round_up_to_int, sustainability_grade, haversine_distance

# Import ML models
from ml_model import DensityPredictor
from ml_landuse import LandUsePredictor
from ml_infrastructure import InfrastructurePredictor


# ── Priority multipliers for density ──────────────────────────────────────────
PRIORITY_DENSITY_MULTIPLIER = {
    "Max Green Space": 0.85,
    "Balanced":        1.00,
    "Max Housing":     1.15,
}

# ── Development type density multipliers ─────────────────────────────────────
DEV_TYPE_DENSITY_MULTIPLIER = {
    "Residential": 1.00,
    "Commercial":  0.70,   # Commercial areas have fewer residents
    "Mixed":       0.85,   # Mixed use has moderate density
}

# ── Bonus green-space threshold per priority for sustainability scoring ─────
PRIORITY_GREEN_BONUS_THRESHOLD = {
    "Max Green Space": 18.0,
    "Balanced":        15.0,
    "Max Housing":     13.0,
}


@dataclass
class PlanResult:
    """Structured result from generate_plan()."""
    # inputs
    total_area: float = 0.0
    location: str = ""
    dev_type: str = "Residential"
    priority: str = "Balanced"

    # land use breakdown (sq ft)
    residential_area: float = 0.0
    green_space: float = 0.0
    road_area: float = 0.0
    facility_area: float = 0.0
    open_space: float = 0.0

    # population
    population: int = 0
    houses: int = 0
    avg_floors: int = 1
    density_ppsf: float = 0.0

    # infrastructure counts
    schools: int = 0
    hospitals: int = 0
    petrol_pumps: int = 0
    parks: int = 0
    community_halls: int = 0

    # compliance
    green_space_pct: float = 0.0
    road_pct: float = 0.0
    compliant: bool = False
    compliance_notes: list = field(default_factory=list)

    # sustainability
    sustainability_score: float = 0.0
    grade: str = "C"
    grade_color: str = "#e67e22"

    # map centre
    lat: float = 21.1458
    lon: float = 79.0882


class SustainablePlanner:
    """
    Main planning engine – translates area + location inputs into a
    comprehensive sustainable development plan using ML predictions.
    """

    def __init__(self):
        self.loader = DataLoader()
        
        # Initialize ML models (they will load existing models or train on first use)
        self.density_predictor = DensityPredictor()
        self.landuse_predictor = LandUsePredictor()
        self.infra_predictor = InfrastructurePredictor()
        
        print("✅ SustainablePlanner initialized with ML models")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def generate_plan(
        self,
        area_sqft: float,
        location: str,
        dev_type: str = "Residential",
        priority: str = "Balanced",
    ) -> PlanResult:
        """
        Generate a complete sustainable area plan using ML predictions.

        Args:
            area_sqft:  Total plot area in square feet.
            location:   Zone name (from NAGPUR_ZONES).
            dev_type:   'Residential' | 'Commercial' | 'Mixed'
            priority:   'Max Green Space' | 'Balanced' | 'Max Housing'

        Returns:
            PlanResult dataclass with all metrics.
        """
        plan = PlanResult()
        plan.total_area = area_sqft
        plan.location = location
        plan.dev_type = dev_type
        plan.priority = priority

        # Get zone info
        zone_info = self.loader.get_zone_info(location)
        base_density = zone_info.get('density_factor', 0.0015)
        zone_type = zone_info.get('type', 'Medium Density Residential')

        # Get coordinates and calculate distance to city centre
        coords = self.loader.get_coordinates_for_zone(location)
        plan.lat, plan.lon = coords[0], coords[1]
        
        dist_to_center = haversine_distance(
            plan.lat, plan.lon, 
            NAGPUR_CENTER[0], NAGPUR_CENTER[1]
        )
        
        area_acres = area_sqft / 43560

        # ============================================================
        # 1. ML DENSITY PREDICTION
        # ============================================================
        ml_density_result = self.density_predictor.predict_density(
            lat=plan.lat,
            lon=plan.lon,
            existing_density=base_density,
            zone_type=zone_type,
            area_sqft=area_sqft,
        )
        
        # Apply priority multiplier to ML prediction
        priority_mult = PRIORITY_DENSITY_MULTIPLIER.get(priority, 1.0)
        dev_mult = DEV_TYPE_DENSITY_MULTIPLIER.get(dev_type, 1.0)
        effective_density = ml_density_result['predicted_density'] * priority_mult * dev_mult
        
        # ============================================================
        # 2. ML LAND USE PREDICTION
        # ============================================================
        landuse = self.landuse_predictor.predict(
            dist_to_center=dist_to_center,
            zone_density=base_density,
            dev_type=dev_type,
            priority=priority,
            area_acres=area_acres,
        )
        
        # Apply land use percentages from ML
        plan.residential_area = area_sqft * landuse['residential_pct']
        plan.green_space = area_sqft * landuse['green_pct']
        plan.road_area = area_sqft * landuse['road_pct']
        plan.facility_area = area_sqft * landuse['facility_pct']
        plan.open_space = max(
            0.0,
            area_sqft - plan.residential_area - plan.green_space
            - plan.road_area - plan.facility_area,
        )
        
        # ============================================================
        # 3. POPULATION & HOUSING
        # ============================================================
        plan.population = self.calculate_population(area_sqft, effective_density)
        plan.houses = self.calculate_houses(plan.population)
        plan.density_ppsf = effective_density
        plan.avg_floors = self.calculate_avg_floors(plan.houses, plan.residential_area)
        
               # ============================================================
        # 4. ML INFRASTRUCTURE PREDICTION
        # ============================================================
        # Get existing amenities in the zone
        amenities_df = self.loader.load_amenities()
        zone_amenities = amenities_df[amenities_df['ward'] == location]
        existing_schools = len(zone_amenities[zone_amenities['type'] == 'School'])
        existing_hospitals = len(zone_amenities[zone_amenities['type'] == 'Hospital'])
        
        # Calculate approximate distances to nearest amenities
        # (based on distance to city centre as proxy)
        dist_to_hospital = max(0.5, dist_to_center * 0.6)
        dist_to_school = max(0.3, dist_to_center * 0.4)
        
        infra = self.infra_predictor.predict(
            population=plan.population,
            density=effective_density,
            area_acres=area_acres,
            green_pct=landuse['green_pct'] * 100,
            existing_schools=existing_schools,
            existing_hospitals=existing_hospitals,
            dist_to_hospital=dist_to_hospital,
            dist_to_school=dist_to_school,
        )
        
        # ============================================================
        # FIX: As per UDPFI Guidelines and PDF requirement
        # Minimum 1 school, 1 hospital, 1 petrol pump, 2 parks
        # ============================================================
        plan.schools = infra['schools']
        plan.hospitals = infra['hospitals']
        plan.parks = infra['parks']
        plan.petrol_pumps = infra['petrol_pumps']
        
        # Force minimum values as per PDF example (population 750 ke liye bhi facilities dikhni chahiye)
        if plan.population > 0:
            if plan.schools == 0:
                plan.schools = 1
                print(f"⚠️ Forced schools to 1 (population={plan.population})")
            if plan.hospitals == 0:
                plan.hospitals = 1
                print(f"⚠️ Forced hospitals to 1 (population={plan.population})")
            if plan.petrol_pumps == 0:
                plan.petrol_pumps = 1
                print(f"⚠️ Forced petrol pumps to 1 (population={plan.population})")
        
        # Parks: minimum 2 as per PDF example
        if plan.parks < 2:
            plan.parks = 2
            print(f"⚠️ Forced parks to 2")
        
        # Community halls: 1 per 10,000 people (minimum 1 if population > 5000)
        plan.community_halls = max(1, round_up_to_int(plan.population / COMMUNITY_HALL_PER_POPULATION))
        
        # Debug output
        print(f"\n📊 Infrastructure Summary for {location}:")
        print(f"   Population: {plan.population:,}")
        print(f"   Schools: {plan.schools} (existing: {existing_schools})")
        print(f"   Hospitals: {plan.hospitals} (existing: {existing_hospitals})")
        print(f"   Parks: {plan.parks}")
        print(f"   Petrol Pumps: {plan.petrol_pumps}")
        print(f"   Community Halls: {plan.community_halls}")
        # ============================================================
        # 5. PERCENTAGES & COMPLIANCE
        # ============================================================
        plan.green_space_pct = percentage(plan.green_space, area_sqft)
        plan.road_pct = percentage(plan.road_area, area_sqft)
        
        # Compliance check
        plan.compliant, plan.compliance_notes = self.validate_plan(plan)
        
        # Sustainability score
        plan.sustainability_score = self._compute_sustainability(plan)
        plan.grade, plan.grade_color = sustainability_grade(plan.sustainability_score)
        
        return plan

    # ------------------------------------------------------------------
    # Calculation helpers
    # ------------------------------------------------------------------

    def calculate_population(self, area_sqft: float, density_factor: float) -> int:
        """Estimate population from area and density factor."""
        return round_up_to_int(area_sqft * density_factor)

    def calculate_houses(self, population: int) -> int:
        """Estimate number of dwelling units."""
        return round_up_to_int(population / AVERAGE_FAMILY_SIZE)

    def calculate_avg_floors(self, houses: int, residential_area: float) -> int:
        """
        Estimate average number of floors.
        Logic: total built-up area needed = houses × avg house size
               ground footprint available = residential_area × coverage ratio
               floors = total built-up / ground footprint
        """
        if residential_area <= 0 or houses <= 0:
            return 1
        total_built_up = houses * AVERAGE_HOUSE_SIZE_SQFT
        ground_footprint = residential_area * HOUSE_COVERAGE_RATIO
        if ground_footprint <= 0:
            return 1
        floors = math.ceil(total_built_up / ground_footprint)
        return max(1, min(floors, 20))  # cap at 20 floors

    def calculate_green_space(self, area_sqft: float, ratio: float = None) -> float:
        """Return recommended green space area in sq ft."""
        r = ratio or GREEN_SPACE_RATIO_MIN
        return area_sqft * r

    def calculate_infrastructure(self, population: int) -> dict:
        """
        Fallback infrastructure calculation (rule-based).
        Used only if ML model fails.
        """
        return {
            "schools":         max(1, round_up_to_int(population / SCHOOL_PER_POPULATION)),
            "hospitals":       max(1, round_up_to_int(population / HOSPITAL_PER_POPULATION)),
            "petrol_pumps":    max(1, round_up_to_int(population / PETROL_PUMP_PER_POPULATION)),
            "parks":           max(1, round_up_to_int(population / PARK_PER_POPULATION)),
            "community_halls": max(1, round_up_to_int(population / COMMUNITY_HALL_PER_POPULATION)),
        }

    def validate_plan(self, plan: PlanResult) -> tuple[bool, list]:
        """Check plan against UDPFI / government compliance norms."""
        notes = []
        ok = True

        if plan.green_space_pct < COMPLIANCE["min_green_space_pct"]:
            ok = False
            notes.append(
                f"⚠ Green space {plan.green_space_pct:.1f}% is below the required "
                f"{COMPLIANCE['min_green_space_pct']}% (UDPFI norm)."
            )
        else:
            notes.append(
                f"✅ Green space {plan.green_space_pct:.1f}% meets UDPFI requirement."
            )

        if plan.road_pct < COMPLIANCE["min_road_pct"]:
            ok = False
            notes.append(
                f"⚠ Road coverage {plan.road_pct:.1f}% is below minimum "
                f"{COMPLIANCE['min_road_pct']}%."
            )
        else:
            notes.append(f"✅ Road coverage {plan.road_pct:.1f}% is adequate.")

        if plan.density_ppsf > COMPLIANCE["max_density_ppsf"]:
            ok = False
            notes.append(
                f"⚠ Density {plan.density_ppsf:.4f} ppsf exceeds permissible "
                f"{COMPLIANCE['max_density_ppsf']} ppsf."
            )
        else:
            notes.append("✅ Population density is within permissible limits.")

        return ok, notes

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_ratios(priority: str, dev_type: str) -> tuple[float, float, float]:
        """
        Fallback rule-based ratios (used if ML model is not available).
        Returns (green_ratio, residential_ratio, road_ratio).
        """
        base = {
            "Max Green Space": (0.20, 0.45, 0.15),
            "Balanced":        (0.17, 0.50, 0.15),
            "Max Housing":     (0.15, 0.55, 0.14),
        }.get(priority, (0.17, 0.50, 0.15))
        
        green_r, res_r, road_r = base
        
        # Development type adjustments
        if dev_type == "Commercial":
            res_r = max(0.20, res_r - 0.25)
            green_r = max(0.10, green_r - 0.05)
            road_r = min(0.22, road_r + 0.05)
        elif dev_type == "Mixed":
            res_r = max(0.40, res_r - 0.10)
            road_r = min(0.18, road_r + 0.02)
            green_r = max(0.12, green_r - 0.02)
        
        return green_r, res_r, road_r

    @staticmethod
    def _compute_sustainability(plan: PlanResult) -> float:
        """
        Compute a 0-100 sustainability score.
        Awards priority-achievement bonus based on actual results.
        """
        w = SUSTAINABILITY_WEIGHTS

        # Green space score (0-100)
        gs = min(100.0, (plan.green_space_pct / 20.0) * 100.0)

        # Infrastructure adequacy
        pop = max(1, plan.population)
        school_ratio = min(1.0, plan.schools / max(1, math.ceil(pop / SCHOOL_PER_POPULATION)))
        hosp_ratio = min(1.0, plan.hospitals / max(1, math.ceil(pop / HOSPITAL_PER_POPULATION)))
        infra = ((school_ratio + hosp_ratio) / 2) * 100.0

        # Density appropriateness (penalise extremes)
        ideal_d = 0.0018
        density_score = max(0.0, 100.0 - abs(plan.density_ppsf - ideal_d) / ideal_d * 60)

        # Road coverage
        road_score = min(100.0, (plan.road_pct / 15.0) * 100.0)

        # Facility accessibility (parks count relative to 1/3000)
        park_ratio = min(1.0, plan.parks / max(1, math.ceil(pop / PARK_PER_POPULATION)))
        facility_score = park_ratio * 100.0

        score = (
            w["green_space_compliance"] * gs
            + w["infrastructure_adequacy"] * infra
            + w["density_appropriateness"] * density_score
            + w["road_coverage"] * road_score
            + w["facility_accessibility"] * facility_score
        )

        # Priority-achievement bonus
        threshold = PRIORITY_GREEN_BONUS_THRESHOLD.get(plan.priority, 15.0)
        if plan.priority == "Max Green Space" and plan.green_space_pct >= threshold:
            score += 5.0
        elif plan.priority == "Max Housing" and plan.houses >= 1:
            # Bonus if density is above the base zone density
            score += 3.0
        elif plan.priority == "Balanced" and plan.compliant:
            score += 2.0

        return round(min(100.0, max(0.0, score)), 1)