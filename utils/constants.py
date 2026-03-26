"""
Constants for Nagpur Sustainable Area Planner
Based on UDPFI Guidelines, NMC data, and Census 2011
"""

# --- CITY CENTER ---
NAGPUR_CENTER = [21.1458, 79.0882]

# --- FAMILY & HOUSING ---
AVERAGE_FAMILY_SIZE = 4.5
AVERAGE_HOUSE_SIZE_SQFT = 1200       # sq ft per dwelling unit (EWS/LIG mix)
HOUSE_COVERAGE_RATIO = 0.60          # 60% ground coverage for residential
                                     # FIX: was defined here but NOT imported
                                     # in planner_logic.py — added to imports there

# --- LAND USE RATIOS (UDPFI) ---
RESIDENTIAL_AREA_RATIO = 0.50        # 50% of total area
GREEN_SPACE_RATIO_MIN = 0.15         # 15% minimum
GREEN_SPACE_RATIO_MAX = 0.20         # 20% preferred
ROAD_AREA_RATIO = 0.15               # 15% for roads
FACILITY_AREA_RATIO = 0.10           # 10% for schools, hospitals, etc.
OPEN_SPACE_RATIO = 0.05              # 5% open plots/future use

# --- INFRASTRUCTURE NORMS (UDPFI) ---
SCHOOL_PER_POPULATION = 5000         # 1 school per 5000 people
HOSPITAL_PER_POPULATION = 15000      # 1 hospital per 15000 people
PETROL_PUMP_PER_POPULATION = 25000   # 1 petrol pump per 25000 people
PARK_PER_POPULATION = 3000           # 1 park per 3000 people
COMMUNITY_HALL_PER_POPULATION = 10000

# --- DENSITY RANGES (people per sq ft) ---
# Based on NMC zoning regulations
DENSITY_VERY_HIGH = 0.0035           # > 0.0035 ppsf → core commercial zones
DENSITY_HIGH = 0.0025
DENSITY_MEDIUM = 0.0015
DENSITY_LOW = 0.0008
DENSITY_VERY_LOW = 0.0004

# --- NAGPUR ZONES ---
# Each zone: {name, density_factor, lat, lon, type, description}
NAGPUR_ZONES = {
    "Dharampeth": {
        "density_factor": 0.0030,
        "lat": 21.1372,
        "lon": 79.0735,
        "type": "High Density Residential",
        "description": "Central upscale residential area"
    },
    "Sadar": {
        "density_factor": 0.0032,
        "lat": 21.1540,
        "lon": 79.0877,
        "type": "High Density Commercial",
        "description": "Central commercial hub"
    },
    "Civil Lines": {
        "density_factor": 0.0018,
        "lat": 21.1614,
        "lon": 79.0829,
        "type": "Medium Density Administrative",
        "description": "Government offices and residential"
    },
    "Laxmi Nagar": {
        "density_factor": 0.0022,
        "lat": 21.1342,
        "lon": 79.1108,
        "type": "Medium Density Residential",
        "description": "East Nagpur residential area"
    },
    "Manish Nagar": {
        "density_factor": 0.0012,
        "lat": 21.1204,
        "lon": 79.0631,
        "type": "Low Density Residential",
        "description": "South Nagpur quiet residential"
    },
    "Pratap Nagar": {
        "density_factor": 0.0020,
        "lat": 21.1621,
        "lon": 79.1014,
        "type": "Medium Density Residential",
        "description": "North-east Nagpur developing area"
    },
    "Kalamna": {
        "density_factor": 0.0010,
        "lat": 21.1759,
        "lon": 79.1154,
        "type": "Industrial",
        "description": "Industrial zone with low residential density"
    },
    "Jaripatka": {
        "density_factor": 0.0028,
        "lat": 21.1488,
        "lon": 79.1016,
        "type": "Mixed Use",
        "description": "Mixed commercial and residential"
    },
    "Gandhibagh": {
        "density_factor": 0.0034,
        "lat": 21.1489,
        "lon": 79.0751,
        "type": "High Density Old City",
        "description": "Old city core, very high density"
    },
    "Mankapur": {
        "density_factor": 0.0008,
        "lat": 21.1170,
        "lon": 79.0530,
        "type": "Developing Area",
        "description": "Peripheral developing zone"
    },
    "Sitabuldi": {
        "density_factor": 0.0033,
        "lat": 21.1480,
        "lon": 79.0830,
        "type": "High Density Commercial",
        "description": "Central commercial and retail hub"
    },
    "Itwari": {
        "density_factor": 0.0031,
        "lat": 21.1510,
        "lon": 79.0780,
        "type": "High Density Mixed",
        "description": "Old market area"
    },
}

# --- SUSTAINABILITY SCORING WEIGHTS ---
SUSTAINABILITY_WEIGHTS = {
    "green_space_compliance": 0.25,
    "infrastructure_adequacy": 0.25,
    "density_appropriateness": 0.20,
    "road_coverage": 0.15,
    "facility_accessibility": 0.15,
}

# --- COLOR SCHEME FOR MAP ---
COLORS = {
    "residential": "#FF6B6B",
    "green_space": "#51CF66",
    "roads": "#FFD43B",
    "schools": "#339AF0",
    "hospitals": "#F03E3E",
    "petrol_pumps": "#FF922B",
    "parks": "#20C997",
    "commercial": "#CC5DE8",
}

# --- GOVERNMENT COMPLIANCE THRESHOLDS ---
COMPLIANCE = {
    "min_green_space_pct": 15.0,
    "min_road_pct": 12.0,
    "max_density_ppsf": 0.004,
    "min_school_coverage": 0.90,   # 90% of norm
    "min_hospital_coverage": 0.90,
}
