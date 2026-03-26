"""
Helper utility functions for Nagpur Sustainable Area Planner
"""

import math
from typing import Union


def sqft_to_acres(sqft: float) -> float:
    """Convert square feet to acres."""
    return sqft / 43560.0


def sqft_to_hectares(sqft: float) -> float:
    """Convert square feet to hectares."""
    return sqft / 107639.1


def acres_to_sqft(acres: float) -> float:
    """Convert acres to square feet."""
    return acres * 43560.0


def sqft_to_sqm(sqft: float) -> float:
    """Convert square feet to square meters."""
    return sqft * 0.0929


def format_number(n: Union[int, float], decimals: int = 0) -> str:
    """Format a number with commas and optional decimal places."""
    if decimals == 0:
        return f"{int(n):,}"
    return f"{n:,.{decimals}f}"


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two points on Earth.
    Returns distance in kilometers.
    """
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calculate_population_density(population: int, area_sqft: float) -> float:
    """Return people per square foot."""
    if area_sqft <= 0:
        return 0.0
    return population / area_sqft


def validate_area_input(area_sqft: float) -> tuple[bool, str]:
    """
    Validate plot area input.
    Returns (is_valid, message).
    """
    if area_sqft <= 0:
        return False, "Area must be a positive number."
    if area_sqft < 5000:
        return False, "Minimum plannable area is 5,000 sq ft."
    if area_sqft > 500_000_000:
        return False, "Area exceeds maximum supported (500 million sq ft)."
    return True, "Valid"


def round_up_to_int(value: float) -> int:
    """Round up a float to the nearest integer (ceiling)."""
    return math.ceil(value)


def percentage(part: float, whole: float) -> float:
    """Return percentage of part in whole, or 0 if whole is 0."""
    if whole == 0:
        return 0.0
    return (part / whole) * 100.0


def sustainability_grade(score: float) -> tuple[str, str]:
    """
    Convert a 0-100 sustainability score to a letter grade and colour.
    Returns (grade, hex_colour).
    """
    if score >= 85:
        return "A+", "#2ecc71"
    elif score >= 75:
        return "A", "#27ae60"
    elif score >= 65:
        return "B", "#f1c40f"
    elif score >= 50:
        return "C", "#e67e22"
    else:
        return "D", "#e74c3c"


def area_label(sqft: float) -> str:
    """Return a human-readable area label (sq ft / acres / hectares)."""
    if sqft >= 1_000_000:
        return f"{sqft/43560:.1f} acres ({sqft/107639:.2f} ha)"
    return f"{format_number(sqft)} sq ft ({sqft/43560:.2f} acres)"
