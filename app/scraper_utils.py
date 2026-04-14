import sys
import os

# Connect to the scraper folder in the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

try:
    from scraper.cement_scraper import get_cement_data
    from scraper.steel_scraper import get_steel_data
except ImportError:
    # Fallback if names differ slightly
    get_cement_data = None
    get_steel_data = None

def scrape_price(material, city, category=None, grade=None):
    try:
        if material == "Cement" and get_cement_data:
            print(f"🔄 Fetching Live Cement data for {city}...")
            data = get_cement_data()
            # Filter by city + category
            result = [
                item for item in data
                if item["city"].lower() == city.lower()
                and (category is None or item["category"] == category)
            ]
            
        elif material == "Steel" and get_steel_data:
            print(f"🔄 Fetching Live Steel data for {city}...")
            data = get_steel_data()
            # Filter by city + grade
            result = [
                item for item in data
                if item["city"].lower() == city.lower()
                and (grade is None or item["grade"] == grade)
            ]
        else:
            return None

        if not result:
            return None

        # Return latest or average price from live scrape
        prices = [item["price"] for item in result]
        return round(sum(prices) / len(prices), 2)
        
    except Exception as e:
        print("Scraping error:", e)
        return None
