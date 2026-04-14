import re

def extract_entities(msg):
    msg = msg.lower()

    material = None
    city = None
    category = None
    grade = None
    future = False
    compare = False
    historical = False
    specific_date = None

    # Date detection (DD/MM/YYYY or YYYY-MM-DD)
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})|(\d{4}-\d{2}-\d{2})', msg)
    if date_match:
        specific_date = date_match.group(0)
        historical = True # Treat specific date as historical lookup for now

    # Comparison detection
    if any(word in msg for word in ["compare", "comparison", "across", "cities", "vise", "difference"]):
        compare = True

    # Historical detection
    if any(word in msg for word in ["last week", "yesterday", "past", "history", "historical", "was", "previous", "7 days", "earlier", "ago"]):
        historical = True

    # material detection
    if "cement" in msg:
        material = "Cement"
    elif "steel" in msg:
        material = "Steel"

    # city detection
    cities = [
        "mumbai", "pune", "nagpur", "nashik", "aurangabad",
        "solapur", "amravati", "kolhapur", "sangli", "jalgaon",
        "akola", "latur", "dhule", "ahmednagar", "chandrapur",
        "parbhani", "beed", "nanded", "ratnagiri", "satara",
        "wardha", "bhandara", "gondia", "yavatmal", "osmanabad"
    ]
    for c in cities:
        if c in msg:
            city = c.capitalize()
            break

    # cement type detection
    if "opc" in msg:
        category = "OPC"
    elif "ppc" in msg:
        category = "PPC"
    elif "psc" in msg:
        category = "PSC"
    elif "composite" in msg:
        category = "Composite"

    # steel grade detection
    if "fe500" in msg:
        grade = "Fe500"
    elif "fe550" in msg:
        grade = "Fe550"
    elif "fe415" in msg:
        grade = "Fe415"

    # future detection
    if any(word in msg for word in ["future", "tomorrow", "next", "predict", "forecast", "coming"]):
        future = True

    return material, city, category, grade, future, compare, historical, specific_date
