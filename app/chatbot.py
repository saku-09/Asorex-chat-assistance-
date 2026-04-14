from nlp_utils import extract_entities
from model_utils import get_price, predict_future, get_comparison
from scraper_utils import scrape_price

def get_response(msg, context):
    msg_lower = msg.lower()

    # Greetings
    if any(greet in msg_lower for greet in ["hi", "hello", "hey", "hola"]):
        context = {}
        return "Hello! Welcome to Asorex Assistant. How can I help you today?", context

    if any(word in msg_lower for word in ["thank", "bye"]):
        context = {}
        return "You're welcome! Feel free to ask more. Goodbye!", context

    # Entity Extraction
    material, city, category, grade, future, compare, historical, specific_date = extract_entities(msg)

    # Context Management & Resetting sub-categories if material changes
    if material and material != context.get('material'):
        context['material'] = material
        context['category'] = None
        context['grade'] = None
    
    if city: context['city'] = city
    if category: context['category'] = category
    if grade: context['grade'] = grade
    if future: context['future'] = future
    if compare: context['compare'] = compare
    if historical: context['historical'] = historical
    if specific_date: context['specific_date'] = specific_date

    c_material = context.get('material')
    c_city = context.get('city')
    c_category = context.get('category')
    c_grade = context.get('grade')
    c_future = context.get('future')
    c_compare = context.get('compare')
    c_historical = context.get('historical')
    c_date = context.get('specific_date')

    # 1. First check if we even have a material
    if not c_material:
        return "I can help with prices for Cement or Steel. Which one are you interested in?", context

    # 2. Comparison Request (Priority)
    if c_compare:
        if c_material == "Cement" and not c_category:
            return f"To compare Cement prices across cities, please specify if you want OPC, PPC, or PSC.", context
        if c_material == "Steel" and not c_grade:
            return f"To compare Steel prices across cities, please specify the grade (Fe500, Fe550, or Fe415).", context
        
        context['compare'] = False
        return get_comparison(c_material, c_category, c_grade), context

    # 3. Check for specific details needed
    if c_material == "Cement" and not c_category:
        return f"Got it, Cement prices. Would you like to check for OPC, PPC, or PSC?", context

    if c_material == "Steel" and not c_grade:
        return f"Got it, Steel prices. Would you like to check for Fe500, Fe550, or Fe415?", context

    if not c_city:
        label = c_category if c_material == "Cement" else c_grade
        return f"Which city in Maharashtra should I check for {c_material} ({label}) prices? (e.g., Pune, Mumbai, Nagpur)", context

    # 4. Handle Price Requests (Current, Future, or Historical)
    label = c_category if c_material == "Cement" else c_grade

    if c_future:
        context['future'] = False 
        return predict_future(c_material, c_category, c_grade), context

    if c_historical or c_date:
        price = get_price(c_material, c_city, c_category, c_grade, historical=True, target_date_str=c_date)
        context['historical'] = False
        context['specific_date'] = None
        
        display_date = c_date if c_date else "approximately a week ago"
        if price:
            return f"[Historical Data]: {c_material} ({label}) price in {c_city} on {display_date} was Rs. {price}.", context
        else:
            return f"I don't have historical data for {c_material} ({label}) in {c_city} for that period.", context

    # Current Price
    price = get_price(c_material, c_city, c_category, c_grade)

    if price is None:
        price = scrape_price(c_material, c_city, c_category, c_grade)
        if price:
            return f"{c_material} ({label}) price in {c_city} is currently Rs. {price}.", context
        else:
            return f"I couldn't find available price data for {c_material} in {c_city} at the moment.", context

    return f"{c_material} ({label}) price in {c_city} is Rs. {price}.", context
