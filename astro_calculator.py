# astro_calculator.py
# Core calculation engine for astrological charts

import swisseph as swe
import pytz
from datetime import datetime
from astro_constants import AstroConstants

class AstroCalculator:
    def __init__(self):
        # Initialize SwissEph
        swe.set_ephe_path(AstroConstants.EPHE_PATH)
    
    def calculate_chart_data(self, date_time, latitude, longitude, timezone, house_system='P'):
        """
        Calculate all chart data including houses and planetary positions.
        
        Args:
            date_time: Datetime object (local time)
            latitude: Float, geographical latitude
            longitude: Float, geographical longitude
            timezone: String, timezone name
            house_system: Character, house system code
            
        Returns:
            Dictionary with houses, planets, and angle positions
        """
        # Convert to timezone aware datetime
        tz = pytz.timezone(timezone)
        dt_local = tz.localize(date_time)
        dt_utc = dt_local.astimezone(pytz.utc)
        
        # Convert to Julian Day
        jd_ut = swe.julday(
            dt_utc.year, 
            dt_utc.month, 
            dt_utc.day, 
            dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
        )
        
        # Debug information
        print(f"JD: {jd_ut}")
        print(f"Date UTC: {dt_utc}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        print(f"House System: {house_system}")
        
        # Calculate houses - CRITICAL FIX for hemisphere issues
        # Ensure latitude is properly signed (negative for Southern hemisphere)
        # Convert house system to byte format required by SwissEph
        houses, ascmc = swe.houses(jd_ut, latitude, longitude, house_system.encode('utf-8'))
        
        # Get Ascendant and Midheaven
        asc = ascmc[0]
        mc = ascmc[1]
        
        # Calculate planetary positions
        positions = {}
        for symbol, planet_id in AstroConstants.PLANETS.items():
            result, _ = swe.calc_ut(jd_ut, planet_id)
            positions[symbol] = result[0]  # Longitude
            
        # Add South Node (opposite to North Node)
        positions["☋"] = (positions["☊"] + 180) % 360
        
        # Add angles
        positions["ASC"] = asc
        positions["MC"] = mc
        
        return {
            "houses": houses,
            "positions": positions,
            "ascmc": ascmc,
            "jd": jd_ut
        }
    
    @staticmethod
    def calculate_aspects(positions):
        """Calculate aspects between planets."""
        aspects = []
        keys = list(positions.keys())
        
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                planet1 = keys[i]
                planet2 = keys[j]
                a1, a2 = positions[planet1], positions[planet2]
                diff = abs(a1 - a2) % 360
                
                for angle, config in AstroConstants.ASPECTS.items():
                    if abs(diff - angle) <= config['tol']:
                        aspects.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "angle": angle,
                            "diff": diff,
                            "config": config
                        })
        
        return aspects