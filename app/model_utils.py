import pandas as pd
import os
from datetime import datetime, timedelta

def get_price(material, city, category=None, grade=None, historical=False, target_date_str=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_path = os.path.join(root_dir, "data", "maharashtra_material_dataset.csv")
    
    if not os.path.exists(data_path):
        return None

    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])

    if material == "Cement":
        mask = (df["material"] == "Cement") & (df["city"].str.lower() == city.lower())
        if category: mask &= (df["category"] == category)
    elif material == "Steel":
        mask = (df["material"] == "Steel") & (df["city"].str.lower() == city.lower())
        if grade: mask &= (df["grade"] == grade)
    else:
        return None

    result = df[mask].sort_values(by="date", ascending=False)
    
    if result.empty:
        return None

    if historical:
        if target_date_str:
            try:
                # Handle multiple formats if needed, but NLP-extracted is usually simple
                fmt = "%Y-%m-%d" if "-" in target_date_str else "%d/%m/%Y"
                target_date = pd.to_datetime(target_date_str, format=fmt)
            except:
                target_date = result.iloc[0]['date'] - timedelta(days=7)
        else:
            # Default to 7 days before the latest date available
            target_date = result.iloc[0]['date'] - timedelta(days=7)
            
        past_data = result[result['date'] <= target_date]
        if not past_data.empty:
            return round(past_data.iloc[0]["price"], 2)
        else:
            # Return oldest available if target is too far back
            return round(result.iloc[-1]["price"], 2)

    return round(result.iloc[0]["price"], 2)

def get_comparison(material, category=None, grade=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_path = os.path.join(root_dir, "data", "maharashtra_material_dataset.csv")
    
    if not os.path.exists(data_path):
        return "Comparison data currently unavailable."

    df = pd.read_csv(data_path)
    
    if material == "Cement":
        sub_df = df[(df["material"] == "Cement")]
        if category: sub_df = sub_df[sub_df["category"] == category]
        label = category if category else "standard"
    else:
        sub_df = df[(df["material"] == "Steel")]
        if grade: sub_df = sub_df[sub_df["grade"] == grade]
        label = grade if grade else "standard"

    if sub_df.empty:
        return f"No comparison data found for {material} ({label})."

    latest_prices = sub_df.sort_values('date').groupby('city').tail(1)
    
    # Select key cities for comparison
    sample_cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur"]
    report = [f"📊 {material} ({label}) Comparison across Major Cities:"]
    
    found = False
    for city in sample_cities:
        city_data = latest_prices[latest_prices['city'].str.lower() == city.lower()]
        if not city_data.empty:
            price = city_data.iloc[0]['price']
            report.append(f"• {city}: Rs. {price}")
            found = True
    
    if not found:
        return f"Could not find city-specific pricing for {material} ({label})."

    return "\n".join(report)

def predict_future(material, category, grade):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    pred_path = os.path.join(root_dir, "outputs", "predictions", f"{material.lower()}_prices.csv")
    
    if not os.path.exists(pred_path):
        return "Sorry, future predictions are still being processed."

    df = pd.read_csv(pred_path)
    avg_price = df["predicted_price"].mean()

    label = (category if material == "Cement" else grade) if (category or grade) else "standard"
    return f"📈 Predicted {label} {material.lower()} price for next week is Rs. {round(avg_price,2)}."
