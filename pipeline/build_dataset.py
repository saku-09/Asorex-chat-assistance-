import pandas as pd
import os
import sys

# Add the parent directory to sys.path so we can import 'scraper'
# This allows the script to be run from anywhere
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from scraper.cement_scraper import get_cement_data
from scraper.steel_scraper import get_steel_data

def main():
    print("Starting data collection...")
    
    print("Scraping Cement data...")
    cement_data = get_cement_data()
    print(f"Collected {len(cement_data)} cement entries.")
    
    print("Scraping Steel data...")
    steel_data = get_steel_data()
    print(f"Collected {len(steel_data)} steel entries.")

    combined_data = cement_data + steel_data

    if not combined_data:
        print("Error: No data collected. Please check your scrapers.")
        return

    df = pd.DataFrame(combined_data)

    # Sort for better readability
    df = df.sort_values(by=["material", "city", "category", "grade"])

    # Ensure the 'data' directory exists in the parent project root
    output_dir = os.path.join(parent_dir, "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "maharashtra_material_dataset.csv")
    
    # --- APPEND LOGIC FOR HISTORICAL DATA ---
    if os.path.exists(output_file):
        print(f"Found existing dataset, appending new data...")
        old_df = pd.read_csv(output_file)
        df = pd.concat([old_df, df], ignore_index=True)
        
        # Remove duplicates (in case the script is run multiple times on same day)
        df = df.drop_duplicates(subset=["date", "material", "brand", "category", "grade", "city"])
    
    # Sort for better readability
    df = df.sort_values(by=["date", "material", "city", "brand"], ascending=[False, True, True, True])
    
    df.to_csv(output_file, index=False)

    print(f"\nDataset updated successfully: {output_file}")
    print(f"Total records in dataset: {len(df)}")
    print("\nPreview of the data:")
    print(df.head())

if __name__ == "__main__":
    main()
