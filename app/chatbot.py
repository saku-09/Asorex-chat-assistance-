from nlp_utils import extract_entities
from model_utils import get_price, predict_future, compare_prices, predict_future_range, get_past_price
from scraper_utils import scrape_price
import re
from datetime import datetime, date, timedelta

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    try:
        match = re.search(r'(\d{1,2})\s+([a-zA-Z]+)(?:\s+(\d{4}))?', date_str)
        if match:
            day = int(match.group(1))
            month_str = match.group(2)[:3].capitalize()
            month = datetime.strptime(month_str, "%b").month
            year = int(match.group(3)) if match.group(3) else datetime.today().year
            return date(year, month, day)
    except:
        pass
    return None

def get_response(msg, context):
    msg_lower = msg.lower()

    # Greetings
    if any(greet in msg_lower for greet in ["hi", "hello", "hey", "hola"]):
        context = {}
        return "Hello 👋 Welcome to Asorex Assistant! I can help you with cement and steel prices.", context

    if any(word in msg_lower for word in ["thank", "bye"]):
        context = {}
        return "You're welcome! Feel free to ask more. Goodbye!", context

    # Entity Extraction
    material, city, category, grade, future, compare, historical, specific_date, brand, future_days, graph = extract_entities(msg)

    # Context Management & Resetting sub-categories if material changes
    if material and material != context.get('material'):
        context['material'] = material
        context['category'] = None
        context['grade'] = None
        context['brand'] = None
    
    if city: context['city'] = city
    if category: context['category'] = category
    if grade: context['grade'] = grade
    if future: context['future'] = future
    if compare: context['compare'] = compare
    if historical: context['historical'] = historical
    if specific_date: context['specific_date'] = specific_date
    if brand: context['brand'] = brand
    if future_days: context['future_days'] = future_days
    if graph: context['graph'] = graph

    c_material = context.get('material')
    c_city = context.get('city')
    c_category = context.get('category')
    c_grade = context.get('grade')
    c_future = context.get('future')
    c_compare = context.get('compare')
    c_historical = context.get('historical')
    c_date = context.get('specific_date')
    c_brand = context.get('brand')
    c_future_days = context.get('future_days')
    c_graph = context.get('graph')

    # 1. First check if we even have a material
    if not c_material:
        return "I can help with prices for Cement or Steel. Which one are you interested in?", context

    # 1.5. Brand Handling (MANDATORY)
    if not c_brand:
        if c_material == "Cement":
            return "Which brand are you looking for? (Ambuja, UltraTech, ACC, Birla, etc.)", context
        else:
            return "Which brand are you looking for? (Tata, JSW, SAIL, Jindal, etc.)", context

    # 2. Comparison Request (Priority)
    if c_compare:
        if c_material == "Cement" and not c_category:
            return f"To compare Cement prices across cities, please specify if you want OPC, PPC, or PSC.", context
        if c_material == "Steel" and not c_grade:
            return f"To compare Steel prices across cities, please specify the grade (Fe500, Fe550, or Fe415).", context
        
        context['compare'] = False
        cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur"]
        data = compare_prices(c_material, cities, c_category, c_grade, c_brand)

        response = f"**Material:** {c_material} ({c_category or c_grade} - {c_brand})\n\n"
        response += "| City | Current | Past | Future |\n"
        response += "| :--- | :--- | :--- | :--- |\n"

        for row in data:
            response += f"| **{row['City']}** | ₹{row['Current']} | ₹{row['Past']} | ₹{row['Future']} |\n"

        return response, context

    # 3. Check for specific details needed
    if c_material == "Cement" and not c_category:
        return f"Got it, Cement prices. Would you like to check for OPC, PPC, or PSC?", context

    if c_material == "Steel" and not c_grade:
        return f"Got it, Steel prices. Would you like to check for Fe500, Fe550, or Fe415?", context

    if not c_city:
        label = c_category if c_material == "Cement" else c_grade
        return f"Which city in Maharashtra should I check for {c_material} ({label}) prices? (e.g., Pune, Mumbai, Nagpur)", context

    if c_grade == "fe_ambiguous":
        return "Do you mean Fe500, Fe550, or Fe415?", context

    # 4. Handle Price Requests (Current, Future, or Historical)
    base_label = c_category if c_material == "Cement" else c_grade
    label = f"{base_label} - {c_brand}" if c_brand else base_label

    if c_date:
        parsed = parse_date(c_date)
        if parsed:
            today = date.today()
            display_date = c_date
            context['specific_date'] = None
            
            if parsed < today:
                # Past Date
                price = get_price(c_material, c_city, c_category, c_grade, historical=True, target_date_str=parsed.strftime("%Y-%m-%d"))
                if price:
                    return f"📊 {c_material} ({label}) price in {c_city} on {display_date} was ₹{price}", context
                else:
                    return "Data not available for the selected date.", context
            elif parsed == today:
                # Today's Date
                price = get_price(c_material, c_city, c_category, c_grade)
                if price:
                    return f"💰 {c_material} ({label}) price in {c_city} today is ₹{price}", context
                else:
                    return "Data not available for the selected date.", context
            else:
                # Future Date
                price = predict_future(c_material, c_category, c_grade, city=c_city, target_date=parsed)
                if price:
                    return f"📈 Predicted {c_material} ({label}) price in {c_city} on {display_date} is ₹{price}", context
                else:
                    return "Data not available for the selected date.", context

    if c_future:
        future_days_val = c_future_days if c_future_days else 1
        current_price = get_price(c_material, c_city, c_category, c_grade)
        
        # future multi-day
        if future_days_val > 1:
            preds = predict_future_range(c_material, c_category, c_grade, days=future_days_val, current_price=current_price)
            
            response = f"📈 Predicted {c_material} ({c_category or c_grade} - {c_brand}) prices:\n\n"
            for i, p in enumerate(preds):
                response += f"Day {i+1} → ₹{p}\n"
            
            context['future'] = False
            context['future_days'] = None
            return response, context

        # future single day
        if future_days_val == 1:
            price = predict_future_range(c_material, c_category, c_grade, days=1, current_price=current_price)[0]
            context['future'] = False
            context['future_days'] = None
            return f"📈 Predicted {c_material} ({c_category or c_grade} - {c_brand}) price in {c_city} tomorrow is ₹{price}", context

    if c_historical:
        price = get_past_price(c_material, c_city, c_category, c_grade, c_brand)
        context['historical'] = False
        display_date = "approximately a week ago"
        if price:
            return f"📊 Average past {c_material} ({label}) price in {c_city} was ₹{price}", context
        else:
            return "Data not available for the selected date.", context

    # Current Price
    price = get_price(c_material, c_city, c_category, c_grade)

    if price is None:
        price = scrape_price(c_material, c_city, c_category, c_grade)
        if price is None:
            # Fallback to ML prediction if not found
            price = predict_future(c_material, c_category, c_grade, city=c_city)
            if isinstance(price, (int, float)):
                return f"Using estimated data based on trends...\n<br>💰 {c_material} ({label}) price in {c_city} today is ₹{price}", context
            else:
                return "Data not available at the moment.", context
        else:
            return f"Using live data...\n<br>💰 {c_material} ({label}) price in {c_city} today is ₹{price}", context

    return f"💰 {c_material} ({label}) price in {c_city} today is ₹{price}", context
