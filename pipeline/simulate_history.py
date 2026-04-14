import pandas as pd
import os
import sys
import random
from datetime import datetime, timedelta

# Add parent directory to sys.path to import scrapers
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from scraper.cement_scraper import get_cement_data
from scraper.steel_scraper import get_steel_data

def main():
    print("--- Starting Historical Data Simulation (30 Days) ---")
    
    # Get current fresh data as a baseline
    cement_base = get_cement_data()
    steel_base = get_steel_data()
    
    combined_base = cement_base + steel_base
    
    historical_rows = []
    
    # Simulate for the last 30 days
    for i in range(1, 31):
        target_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"Generating data for: {target_date}")
        
        for entry in combined_base:
            # Create a copy to avoid modifying the original
            simulated_entry = entry.copy()
            simulated_entry["date"] = target_date
            
            # Simulate historical price variation (±5% overall trend variation)
            trend_variation = random.uniform(0.95, 1.05)
            simulated_entry["price"] = round(entry["price"] * trend_variation, 2)
            
            historical_rows.append(simulated_entry)

    # Convert to DataFrame
    df_history = pd.DataFrame(historical_rows)
    
    # Output path
    output_dir = os.path.join(parent_dir, "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "maharashtra_material_dataset.csv")
    
    # Load today's data if it exists
    if os.path.exists(output_file):
        df_today = pd.read_csv(output_file)
        df_final = pd.concat([df_today, df_history], ignore_index=True)
    else:
        df_final = df_history
        
    # Remove duplicates and sort
    df_final = df_final.drop_duplicates(subset=["date", "material", "brand", "category", "grade", "city"])
    df_final = df_final.sort_values(by=["date", "material", "city", "brand"], ascending=[False, True, True, True])
    
    df_final.to_csv(output_file, index=False)
    
    print(f"\nSimulation complete!")
    print(f"Total records in historical dataset: {len(df_final)}")
    print(f"File location: {output_file}")

if __name__ == "__main__":
    main()
