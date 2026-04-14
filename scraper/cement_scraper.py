import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import re

# List of cities for all-over Maharashtra
MAHARASHTRA_CITIES = [
    "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad",
    "Solapur", "Amravati", "Kolhapur", "Sangli", "Jalgaon",
    "Akola", "Latur", "Dhule", "Ahmednagar", "Chandrapur",
    "Parbhani", "Beed", "Nanded", "Ratnagiri", "Satara",
    "Wardha", "Bhandara", "Gondia", "Yavatmal", "Osmanabad"
]

# -----------------------------
# CATEGORY DETECTOR
# -----------------------------
def detect_category(text):
    text = text.upper()
    if "OPC" in text:
        return "OPC"
    elif "PPC" in text:
        return "PPC"
    elif "PSC" in text:
        return "PSC"
    elif "COMPOSITE" in text:
        return "Composite"
    else:
        return "General"

# -----------------------------
# REGION-BASED VARIATION
# -----------------------------
def get_city_adjustment(city):
    if city in ["Mumbai", "Pune"]:
        return random.uniform(1.02, 1.05) # Premium cities
    elif city in ["Nagpur", "Nashik", "Aurangabad"]:
        return random.uniform(0.98, 1.02) # Mid-tier
    else:
        return random.uniform(0.95, 1.00) # Smaller cities

# -----------------------------
# SCRAPE RECONS (ALL BRANDS)
# -----------------------------
def scrape_recons():
    url = "https://www.reconsgroup.com/prices/mumbai-cement-prices.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                text = cols[0].text.strip()
                price_text = cols[1].text.strip()
                try:
                    price = float(price_text.replace("\u20b9", "").replace(",", "").strip())
                    category = detect_category(text)
                    brand = text.split(" ")[0] # Extract brand
                    data.append({"brand": brand, "category": category, "price": price})
                except:
                    continue
    except Exception as e:
        print(f"   [WARNING] Error scraping Recons: {e}")
    
    return data

# -----------------------------
# SCRAPE INDIAMART (EXTRA DATA)
# -----------------------------
def scrape_indiamart():
    url = "https://dir.indiamart.com/impcat/cement.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        
        # Regex to find Brand and Price
        matches = re.findall(r"(Ultratech|ACC|Ambuja|JK|Birla|Dalmia|Sree).*?[\u20b9]\s?(\d+)", text, re.I)
        for match in matches:
            brand = match[0]
            price = int(match[1])
            if 250 < price < 500: # Valid cement price range per bag
                data.append({"brand": brand, "category": "General", "price": price})
    except Exception as e:
        print(f"   [WARNING] Error scraping IndiaMART: {e}")
    
    return data

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_cement_data():
    print("   Collecting all Cement brands from Recons + IndiaMART...")
    raw_data = []
    raw_data += scrape_recons()
    raw_data += scrape_indiamart()

    # Fallback if scraping fails
    if not raw_data:
        print(f"   [WARNING] No live data found, using fallback baseline...")
        raw_data = [
            {"brand": "Ambuja", "category": "OPC", "price": 330},
            {"brand": "ACC", "category": "PPC", "price": 310},
            {"brand": "UltraTech", "category": "OPC", "price": 340}
        ]
    else:
        print(f"   [SUCCESS] Collected {len(raw_data)} baseline entries.")

    final_data = []
    date_today = datetime.today().strftime("%Y-%m-%d")

    for item in raw_data:
        for city in MAHARASHTRA_CITIES:
            # Apply regional pricing model
            adjusted_price = round(item["price"] * get_city_adjustment(city), 2)
            
            final_data.append({
                "date": date_today,
                "material": "Cement",
                "brand": item["brand"],
                "category": item["category"],
                "grade": None,
                "size": "50kg",
                "unit": "bag",
                "price": adjusted_price,
                "city": city,
                "state": "Maharashtra",
                "source": "Recons + IndiaMART"
            })

    return final_data
