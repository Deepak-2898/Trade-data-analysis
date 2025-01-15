# trade_pipeline.py

import os
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Paths
EXPORT_DATA_PATH = 'data/Export_Data.csv'
IMPORT_DATA_PATH = 'data/Import_Data.csv'
COMBINED_DATA_PATH = 'data/combined_trade_data.csv'
DB_PATH = 'data/trade_analysis.db'
TABLE_NAME = 'trade_data'

# Step 1: Data Ingestion
def load_data():
    print("[INFO] Loading data files...")
    if not os.path.exists(EXPORT_DATA_PATH):
        raise FileNotFoundError(f"Export data file not found at {EXPORT_DATA_PATH}. Ensure the file exists.")
    if not os.path.exists(IMPORT_DATA_PATH):
        raise FileNotFoundError(f"Import data file not found at {IMPORT_DATA_PATH}. Ensure the file exists.")

    export_data = pd.read_csv(EXPORT_DATA_PATH)
    import_data = pd.read_csv(IMPORT_DATA_PATH)
    print("[INFO] Data files loaded successfully.")
    return export_data, import_data

# Step 2: Data Cleaning
def clean_data(export_data, import_data):
    print("[INFO] Cleaning data...")
    export_data.columns = export_data.columns.str.strip().str.lower().str.replace(' ', '_')
    import_data.columns = import_data.columns.str.strip().str.lower().str.replace(' ', '_')

    export_data = export_data.copy()
    import_data = import_data.copy()

    export_data['export_value'] = export_data['export_value'].fillna(0)
    import_data = import_data.dropna(subset=['import_value_of_each_commodity'])

    export_data['export_value'] = pd.to_numeric(export_data['export_value'], errors='coerce')
    import_data['import_value_of_each_commodity'] = pd.to_numeric(import_data['import_value_of_each_commodity'], errors='coerce')

    export_data['yearcode'] = pd.to_numeric(export_data['yearcode'], errors='coerce')
    import_data['yearcode'] = pd.to_numeric(import_data['yearcode'], errors='coerce')

    print("[INFO] Data cleaning complete.")
    return export_data, import_data

# Step 3: Data Integration
def integrate_data(export_data, import_data):
    print("[INFO] Integrating data...")
    combined_data = pd.merge(
        export_data,
        import_data,
        on=['country', 'yearcode'],
        how='outer',
        suffixes=('_export', '_import')
    )

    combined_data['trade_balance'] = combined_data['export_value'] - combined_data['import_value_of_each_commodity']
    print("[INFO] Data integration complete.")
    return combined_data

# Step 4: Save to Database
def save_to_database(combined_data):
    print("[INFO] Saving data to database...")
    engine = create_engine(f'sqlite:///{DB_PATH}')
    combined_data.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    print(f"[INFO] Data saved to database at {DB_PATH}.")

# Step 5: Visualization
def visualize_data(combined_data):
    print("[INFO] Creating visualization...")
    top_export_countries = combined_data.groupby('name_of_the_export_country').agg(
        total_exports=('export_value', 'sum')
    ).sort_values(by='total_exports', ascending=False).head(5)

    plt.figure(figsize=(10, 6))
    plt.bar(top_export_countries.index, top_export_countries['total_exports'], color='skyblue')
    plt.title('Top 5 Export Destinations', fontsize=16)
    plt.xlabel('Countries', fontsize=12)
    plt.ylabel('Total Export Value (in billions)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('output/top_export_destinations.png')
    print("[INFO] Visualization saved to 'output/top_export_destinations.png'.")

# Main Pipeline
def main():
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    try:
        export_data, import_data = load_data()
    except FileNotFoundError as e:
        print(e)
        return

    export_data, import_data = clean_data(export_data, import_data)
    combined_data = integrate_data(export_data, import_data)
    combined_data.to_csv(COMBINED_DATA_PATH, index=False)
    print(f"[INFO] Combined data saved to {COMBINED_DATA_PATH}.")
    save_to_database(combined_data)
    visualize_data(combined_data)

if __name__ == '__main__':
    main()
