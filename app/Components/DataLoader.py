import pandas as pd
<<<<<<< HEAD
import os

# --- 1. ROBUST PATH HANDLING ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(script_dir, 'Visuals', 'merged_crashes_person.csv')
=======
import numpy as np
import os

# --- 1. ROBUST PATH HANDLING ---
# Get the folder where THIS script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the CSV (assumes it's next to this script)
OUTPUT_FILE = os.path.join(script_dir, "merged_crashes_person.csv")
>>>>>>> 2578d97bd5cb1d8a7481b4701ed58e89af6a41af

def load_data():
    """
    Loads the final cleaned dataset with robust path handling.
    """
<<<<<<< HEAD
    if not os.path.exists(DATA_FILE):
        print(f"❌ CRITICAL ERROR: Data file not found at: {DATA_FILE}")
        return pd.DataFrame()  # Return empty to prevent crash

    try:
        df = pd.read_csv(DATA_FILE, low_memory=False)

        # --- Post-Load Typing ---
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'], errors='coerce')
            df['CRASH_MONTH'] = df['CRASH_DATETIME'].dt.month
            df['CRASH_HOUR'] = df['CRASH_DATETIME'].dt.hour

        if 'CRASH_YEAR' in df.columns:
            df['CRASH_YEAR'] = df['CRASH_YEAR'].astype('Int64')

        # --- Standardize string columns for filtering ---
=======
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
>>>>>>> 2578d97bd5cb1d8a7481b4701ed58e89af6a41af
        cols_to_standardize = [
            'BOROUGH', 
            'CONTRIBUTING FACTOR VEHICLE 1', 
            'CONTRIBUTING FACTOR VEHICLE 2',
            'VEHICLE TYPE CODE 1', 
            'VEHICLE TYPE CODE 2', 
<<<<<<< HEAD
            'MOST_COMMON_SEX'
        ]
        for col in cols_to_standardize:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper().replace(['NAN', 'NULL', ''], 'UNKNOWN')

        return df.dropna(subset=['COLLISION_ID'])

=======
            'MOST_COMMON_SEX' 
        ]
        
        for col in cols_to_standardize:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper().replace(['NAN', 'NULL', ''], 'UNKNOWN')
        
        return df.dropna(subset=['COLLISION_ID']) 
        
>>>>>>> 2578d97bd5cb1d8a7481b4701ed58e89af6a41af
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()

<<<<<<< HEAD

# --- Load data once ---
df = load_data()


# --- Dropdown Options Helper ---
def get_options(df, column_name, top_n=50):
    """
    Get sorted dropdown options for a column, filtered for clean values.
    """
    if df.empty or column_name not in df.columns:
        return []

    items = df[column_name].dropna().astype(str).str.upper()
    clean_items = [i for i in items if i not in ['UNKNOWN', 'NONE', 'NAN', '']]
    clean_items = sorted(list(set(clean_items)))

    return [{'label': i, 'value': i} for i in clean_items[:top_n]]


# --- Filter Helper ---
def filter_dataframe(df, inputs):
    """
    Apply multiple filters to the dataframe.
    Expected keys in `inputs` dict: borough, year, factor1, factor2, vehicle1, vehicle2, demographic
    """
    if df.empty:
        return df

    dff = df.copy()
    filter_map = {
        'borough': 'BOROUGH',
        'year': 'CRASH_YEAR',
        'factor1': 'CONTRIBUTING FACTOR VEHICLE 1',
        'factor2': 'CONTRIBUTING FACTOR VEHICLE 2',
        'vehicle1': 'VEHICLE TYPE CODE 1',
        'vehicle2': 'VEHICLE TYPE CODE 2',
        'demographic': 'MOST_COMMON_SEX'
    }

    for key, col in filter_map.items():
        value = inputs.get(key)
        if value and value != 'ALL' and col in dff.columns:
            if key == 'year':
                try:
                    dff = dff[dff[col] == int(value)]
                except ValueError:
                    pass
            else:
                dff = dff[dff[col] == value]

    return dff


# --- Pre-generate options for dropdowns ---
Borough_options = get_options(df, 'BOROUGH')
CRASH_YEAR_options = get_options(df, 'CRASH_YEAR')
Contributing_Factor1_options = get_options(df, 'CONTRIBUTING FACTOR VEHICLE 1')
Contributing_Factor2_options = get_options(df, 'CONTRIBUTING FACTOR VEHICLE 2')
Vehicle1_options = get_options(df, 'VEHICLE TYPE CODE 1')
Vehicle2_options = get_options(df, 'VEHICLE TYPE CODE 2')
Demographic_options = get_options(df, 'MOST_COMMON_SEX')

print("✅ Data loaded and dropdown options generated successfully.")
=======
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
>>>>>>> 2578d97bd5cb1d8a7481b4701ed58e89af6a41af
