# astro_constants.py
# Contains all constant data used in the astrological calculations

import swisseph as swe

class AstroConstants:
    # Set ephemeris path
    EPHE_PATH = "./ephe"
    
    # Planets and points
    PLANETS = {
        "☉": swe.SUN, "☽": swe.MOON, "☿": swe.MERCURY, "♀": swe.VENUS,
        "♂": swe.MARS, "♃": swe.JUPITER, "♄": swe.SATURN, "♅": swe.URANUS,
        "♆": swe.NEPTUNE, "♇": swe.PLUTO, "⚷": 15, "⚸": 12, "☊": swe.TRUE_NODE
    }
    
    # Aspects
    ASPECTS = {
        0: {"tol": 8, "cor": "red", "estilo": "solid", "simbolo": "☌"},
        30: {"tol": 3, "cor": "blue", "estilo": "dotted", "simbolo": "≿"},
        45: {"tol": 3, "cor": "red", "estilo": "dotted", "simbolo": "∕"},
        60: {"tol": 5, "cor": "blue", "estilo": "solid", "simbolo": "*"},
        90: {"tol": 5, "cor": "red", "estilo": "solid", "simbolo": "□"},
        120: {"tol": 5, "cor": "blue", "estilo": "solid", "simbolo": "△"},
        150: {"tol": 3, "cor": "red", "estilo": "dotted", "simbolo": "⨯"},
        180: {"tol": 8, "cor": "red", "estilo": "solid", "simbolo": "⊗"},
    }
    
    # Zodiac signs
    SIGNS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
    
    # Timezones by country/region
    TIMEZONE_MAP = {
        "Brasil": "America/Sao_Paulo",
        "EUA": "America/New_York",
        "Europa": "Europe/London", 
        "Asia": "Asia/Tokyo",
        "Oceania": "Australia/Sydney"
    }
    
    # House systems
    HOUSE_SYSTEMS = {
        "Placidus": 'P',
        "Koch": 'K',
        "Campanus": 'C',
        "Equal": 'E',
        "Whole Sign": 'W'
    }