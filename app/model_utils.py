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

def get_past_price(material, city, category=None, grade=None, brand=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_path = os.path.join(root_dir, "data", "maharashtra_material_dataset.csv")

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date", ascending=False)

    if material == "Cement":
        df = df[
            (df["city"].str.lower() == city.lower()) &
            (df["category"].str.upper() == category.upper()) &
            (df["brand"].str.lower() == brand.lower())
        ]
    else:
        df = df[
            (df["city"].str.lower() == city.lower()) &
            (df["grade"].str.upper() == grade.upper()) &
            (df["brand"].str.lower() == brand.lower())
        ]

    if len(df) < 2:
        return None

    return round(df.iloc[1]["price"], 2)

from scraper_utils import scrape_price

def compare_prices(material, cities, category=None, grade=None, brand=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_path = os.path.join(root_dir, "data", "maharashtra_material_dataset.csv")

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])

    results = []

    for city in cities:
        # filter dataset
        if material == "Cement":
            data = df[
                (df["material"] == "Cement") &
                (df["city"].str.lower() == city.lower()) &
                (df["category"] == category) &
                (df["brand"].str.lower() == brand.lower())
            ]
        else:
            data = df[
                (df["material"] == "Steel") &
                (df["city"].str.lower() == city.lower()) &
                (df["grade"] == grade) &
                (df["brand"].str.lower() == brand.lower())
            ]

        # 🔥 IF DATA NOT FOUND → FALLBACK
        if data.empty:
            print(f"Fallback triggered for {city}")

            # use scraping
            price = scrape_price(material, city, category, grade)

            if price is None:
                # final fallback (baseline)
                price = 320 if material == "Cement" else 60000

            current = price
            past = price - 5
            future = price + 5
        else:
            current = round(data["price"].mean(), 2)
            past = round(data.tail(7)["price"].mean(), 2)
            future = round(current + 5, 2)  # or ML

        results.append({
            "City": city,
            "Current": current,
            "Past": past,
            "Future": future
        })

    return results

def predict_future(material, category, grade, city=None, target_date=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    pred_path = os.path.join(root_dir, "outputs", "predictions", f"{material.lower()}_prices.csv")
    
    label = (category if material == "Cement" else grade) if (category or grade) else "standard"
    
    if not os.path.exists(pred_path):
        return None

    df = pd.read_csv(pred_path)
    
    if target_date:
        if isinstance(target_date, str):
            try:
                target_date_obj = pd.to_datetime(target_date).date()
            except:
                target_date_obj = None
        else:
            target_date_obj = target_date
            
        if target_date_obj:
            df['date_obj'] = pd.to_datetime(df['date']).dt.date
            target_pred = df[df['date_obj'] == target_date_obj]
            if not target_pred.empty:
                future_val = target_pred.iloc[0]['predicted_price']
            else:
                future_val = df["predicted_price"].mean()
        else:
            future_val = df["predicted_price"].mean()
    else:
        future_val = df["predicted_price"].mean()

    # Apply city multiplier if city is provided
    if city:
        data_path = os.path.join(root_dir, "data", "maharashtra_material_dataset.csv")
        if os.path.exists(data_path):
            orig_df = pd.read_csv(data_path)
            orig_df['date'] = pd.to_datetime(orig_df['date'])
            sub_df = orig_df[orig_df["material"].str.lower() == material.lower()]
            
            city_data = sub_df[sub_df['city'].str.lower() == city.lower()].sort_values(by="date", ascending=False)
            if not city_data.empty:
                current_price = city_data.iloc[0]['price']
                avg_current = sub_df[sub_df["date"] == city_data.iloc[0]['date']]['price'].mean()
                if pd.notna(avg_current) and avg_current > 0:
                    future_val = current_price * (future_val / avg_current)
                else:    
                    future_val = current_price * 1.05

    if target_date and city:
        return round(future_val, 2)
    
    # Original behavior if not date/city explicitly requested (or fallback)
    if city: 
        return round(future_val, 2)
    return f"📈 Predicted {label} {material.lower()} price for next week is Rs. {round(future_val,2)}."

import random

def predict_future_range(material, category=None, grade=None, days=1, current_price=None):
    preds = []

    if current_price is None:
        current_price = 320 if material == "Cement" else 60000

    for i in range(days):

        # 🔥 BASE ON CURRENT PRICE ONLY
        base = current_price

        # 🔥 SMALL INCREMENT (REALISTIC MARKET)
        growth_rate = 0.005  # 0.5%

        next_price = base * (1 + growth_rate)

        # 🔥 ADD SMALL RANDOM VARIATION (OPTIONAL)
        variation = random.uniform(-0.002, 0.002)  # ±0.2%
        next_price = next_price * (1 + variation)

        next_price = round(next_price, 2)

        preds.append(next_price)

        # update base for next loop
        current_price = next_price

    return preds
