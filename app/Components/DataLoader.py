import pandas as pd
import os

def load_data():
    """Loads data from a local Parquet or CSV file."""
    # Get the folder where this script lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths (Look in the main project folder, one level up if inside 'app/Components')
    # Adjust these paths if your file is in a different spot!
    parquet_path = os.path.join(current_dir, '..', '..', 'merged_crashes.parquet')
    csv_path = os.path.join(current_dir, '..', '..', 'merged_crashes.csv')
    
    # Fallback: Look in the same folder (if running script directly)
    if not os.path.exists(parquet_path) and not os.path.exists(csv_path):
        parquet_path = "merged_crashes.parquet"
        csv_path = "merged_crashes.csv"

    df = pd.DataFrame()

    try:
        # 1. Try Parquet (Best for performance)
        if os.path.exists(parquet_path):
            print(f"Loading local Parquet: {parquet_path}...")
            df = pd.read_parquet(parquet_path, engine='pyarrow')
            
        # 2. Try CSV (Fallback)
        elif os.path.exists(csv_path):
            print(f"Loading local CSV: {csv_path}...")
            df = pd.read_csv(csv_path, low_memory=False)
            
        else:
            print(f"❌ ERROR: No data file found at {parquet_path} or {csv_path}")
            return pd.DataFrame()

        # 3. Standardize Date/Time
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'], errors='coerce')
            df['CRASH_MONTH'] = df['CRASH_DATETIME'].dt.month
            df['CRASH_HOUR'] = df['CRASH_DATETIME'].dt.hour
            
        print(f"✅ Loaded {len(df):,} rows successfully.")
        return df

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# --- Filtering Functions (Keep these unchanged) ---
def get_options(df, column_name):
    if df.empty or column_name not in df.columns:
        return []
    items = df[column_name].astype(str).unique()
    clean_items = [i for i in items if i.lower() not in ['nan', 'none', '', 'null', 'unknown']]
    return [{'label': i, 'value': i} for i in sorted(clean_items)][:50]

def filter_dataframe(df, inputs):
    if df.empty: return df
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