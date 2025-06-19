# astro_utils.py
# Utility functions for astrological calculations

import unicodedata

class AstroUtils:
    @staticmethod
    def normalize_text(text):
        """Remove accents and lowercase text for searching."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', text.lower())
            if unicodedata.category(c) != 'Mn'
        )
    
    @staticmethod
    def format_degrees(degrees):
        """Format degrees to show degrees and minutes."""
        total = degrees % 30
        deg = int(total)
        mins = int((total - deg) * 60)
        return f"{deg}° {mins:02d}′"
    
    @staticmethod
    def find_location_offline(city_name):
        """Find latitude and longitude from city name."""
        normalized_name = AstroUtils.normalize_text(city_name)
        
        try:
            with open("allCountries.txt", encoding="utf-8") as f:
                for line in f:
                    parts = line.split("\t")
                    if len(parts) > 5:
                        line_name = AstroUtils.normalize_text(parts[1])
                        if normalized_name == line_name:
                            return float(parts[4]), float(parts[5])
        except FileNotFoundError:
            print("Warning: Location database file 'allCountries.txt' not found")
            return None, None
        except Exception as e:
            print(f"Error reading location database: {str(e)}")
            return None, None
            
        return None, None