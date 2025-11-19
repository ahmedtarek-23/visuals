import pandas as pd
import os

def load_data():
    """Loads the merged CSV file from the same folder as this script."""
    # 1. Find the folder where this script is running
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Create the full path to the CSV
    file_path = os.path.join(current_folder, 'merged_crashes.csv')

    print(f"Looking for data at: {file_path}")

    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"SUCCESS: Loaded {len(df)} rows.")
        
        # Ensure date/time columns exist for the Line/Heatmap charts
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'])
            df['CRASH_MONTH'] = df['CRASH_DATETIME'].dt.month
            df['CRASH_HOUR'] = df['CRASH_DATETIME'].dt.hour
        return df
        
    except FileNotFoundError:
        print(f"\n[ERROR] Could not find 'merged_crashes.csv'")
        print(f"Please make sure the file is inside this folder: {current_folder}\n")
        return pd.DataFrame()

def get_options(df, column_name):
    """Get sorted options for dropdowns (Top 50 for performance)."""
    if df.empty or column_name not in df.columns:
        return []
    
    # Get unique values and convert to string
    items = df[column_name].astype(str).unique()
    
    # Filter out nan/null strings
    clean_items = [i for i in items if i.lower() not in ['nan', 'none', '', 'null']]
    
    # Return sorted top 50
    return [{'label': i, 'value': i} for i in sorted(clean_items)][:50]

def filter_dataframe(df, inputs):
    """Applies all 7 filters to the dataframe."""
    if df.empty: return df
    dff = df.copy()
    
    # Map of 'Filter ID' -> 'Column Name'
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
            # Handle numeric year vs string columns
            if key == 'year':
                try:
                    dff = dff[dff[col] == int(value)]
                except ValueError:
                    pass # Ignore if year conversion fails
            else:
                dff = dff[dff[col] == value]
                
    return dff