import pandas as pd
import numpy as np
import os

# --- 1. ROBUST PATH HANDLING ---
# Get the folder where THIS script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the CSV (assumes it's next to this script)
OUTPUT_FILE = os.path.join(script_dir, "merged_crashes_person.csv")

def load_data():
    """
    Loads the final cleaned dataset with robust path handling.
    """
    if not os.path.exists(OUTPUT_FILE):
        print(f"❌ CRITICAL ERROR: Data file not found at: {OUTPUT_FILE}")
        return pd.DataFrame() # Return empty to prevent immediate crash

    try:
        df = pd.read_csv(OUTPUT_FILE, low_memory=False)
        
        # 1. Post-Load Typing
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'], errors='coerce')
        
        if 'CRASH_YEAR' in df.columns:
            df['CRASH_YEAR'] = df['CRASH_YEAR'].astype('Int64') 
        
        # 2. Standardization for Filtering
        # NOTE: 'PERSON_INJURY' was removed because it was aggregated into counts.
        # We use 'MOST_COMMON_SEX' instead.
        cols_to_standardize = [
            'BOROUGH', 
            'CONTRIBUTING FACTOR VEHICLE 1', 
            'CONTRIBUTING FACTOR VEHICLE 2',
            'VEHICLE TYPE CODE 1', 
            'VEHICLE TYPE CODE 2', 
            'MOST_COMMON_SEX' 
        ]
        
        for col in cols_to_standardize:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper().replace(['NAN', 'NULL', ''], 'UNKNOWN')
        
        return df.dropna(subset=['COLLISION_ID']) 
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# --- Load data once ---
df_loaded = load_data()

# --- Simplified Filter Option Generation ---
def generate_options(column_name):
    """Retrieves unique, clean, and uppercase options for dropdowns."""
    if df_loaded.empty or column_name not in df_loaded.columns:
        return []
    
    # Filter out bad values
    options = [
        str(opt).upper() 
        for opt in df_loaded[column_name].dropna().unique() 
        if str(opt).strip() not in ('UNKNOWN', 'NONE', 'NAN', '')
    ]
    return sorted(list(set(options)))

# Generate options (Check if df_loaded is not empty first)
if not df_loaded.empty:
    Borough_options = generate_options('BOROUGH')
    
    # Handle Year safely
    CRASH_YEAR = []
    if "CRASH_YEAR" in df_loaded.columns:
        unique_years = df_loaded["CRASH_YEAR"].dropna().unique()
        CRASH_YEAR = sorted([str(int(y)) for y in unique_years])

    Contributing_Factor1 = generate_options('CONTRIBUTING FACTOR VEHICLE 1')
    Contributing_Factor2 = generate_options('CONTRIBUTING FACTOR VEHICLE 2') # Added to match requirements
    Vehicle1 = generate_options('VEHICLE TYPE CODE 1')
    Vehicle2 = generate_options('VEHICLE TYPE CODE 2') # Added to match requirements
    
    # Changed from 'PERSON_INJURY' to 'MOST_COMMON_SEX' to match merged data
    Demographic_Options = generate_options('MOST_COMMON_SEX')
else:
    # Fallback if data fails to load
    Borough_options, CRASH_YEAR, Contributing_Factor1, Contributing_Factor2, Vehicle1, Vehicle2, Demographic_Options = [], [], [], [], [], [], []

print("✅ Data Loaded and Options Generated Successfully.")