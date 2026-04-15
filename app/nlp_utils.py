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
    brand = None
    graph = False
    future = False
    future_days = 0

    # Greeting / generic checks
    if any(word in msg for word in ["trend", "graph"]):
        graph = True

    # single future (with typo handling)
    if any(word in msg for word in ["tomorrow","tommorow","tommoro","tmooorow","tmrw"]):
        future = True
        future_days = 1

    # day after tomorrow
    if "day after tomorrow" in msg:
        future = True
        future_days = 2

    # after X days
    match = re.search(r'after\s*(\d+)\s*days', msg)
    if match:
        future = True
        future_days = int(match.group(1))

    # next X days
    match2 = re.search(r'next\s*(\d+)\s*days', msg)
    if match2:
        future = True
        future_days = int(match2.group(1))

    # next week
    if "next week" in msg:
        future = True
        future_days = 7

    # Date detection (DD/MM/YYYY, YYYY-MM-DD, or "10 April", "5 May")
    date_match = re.search(r'(\d{1,2}\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:\s+\d{4})?)|(\d{1,2}/\d{1,2}/\d{4})|(\d{4}-\d{2}-\d{2})', msg, re.IGNORECASE)
    if date_match:
        specific_date = date_match.group(0)
        # We don't automatically set historical=True anymore, chatbot will decide based on date

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
    if any(w in msg for w in ["oppc", "ppc", "ppc cement"]):
        category = "PPC"
    elif any(w in msg for w in ["opc", "opc cement"]):
        category = "OPC"
    elif "psc" in msg:
        category = "PSC"
    elif "composite" in msg:
        category = "Composite"

    # steel grade detection
    msg_no_space = msg.replace(" ", "").replace("-", "")
    if "fe500" in msg_no_space:
        grade = "Fe500"
    elif "fe550" in msg_no_space:
        grade = "Fe550"
    elif "fe415" in msg_no_space:
        grade = "Fe415"
    elif re.search(r'\bfe\b', msg):
        grade = "fe_ambiguous"

    # brand detection
    brand_match = re.search(r'\b(ambuja|ultratech|acc|birla|tata|jsw|sail|jindal)\b', msg)
    if brand_match:
        brand = brand_match.group(1).capitalize()

    # future detection fallback
    if future_days == 0 and any(word in msg for word in ["future", "next", "predict", "forecast", "coming"]):
        future = True

    return material, city, category, grade, future, compare, historical, specific_date, brand, future_days, graph
