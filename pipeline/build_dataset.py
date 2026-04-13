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
    print("🚀 Starting data collection...")
    
    print("📡 Scraping Cement data...")
    cement_data = get_cement_data()
    print(f"✅ Collected {len(cement_data)} cement entries.")
    
    print("📡 Scraping Steel data...")
    steel_data = get_steel_data()
    print(f"✅ Collected {len(steel_data)} steel entries.")

    combined_data = cement_data + steel_data

    if not combined_data:
        print("❌ No data collected. Please check your scrapers.")
        return

    df = pd.DataFrame(combined_data)

    # Sort for better readability
    df = df.sort_values(by=["material", "city", "category", "grade"])

    # Ensure the 'data' directory exists in the parent project root
    output_dir = os.path.join(parent_dir, "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "maharashtra_material_dataset.csv")
    df.to_csv(output_file, index=False)

    print(f"\n✨ Dataset created successfully: {output_file}")
    print(f"📊 Total records: {len(df)}")
    print("\nPreview of the data:")
    print(df.head())

if __name__ == "__main__":
    main()
