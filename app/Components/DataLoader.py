import pandas as pd


import pandas as pd

def load_data():
    try:
        # Deployment CSV (hosted online)
        file_url = "https://storage.googleapis.com/crashes_datadet/merged_crashes.csv"
        print("Loading optimized dataset...")

        # Specify only the columns your app actually uses
        needed_columns = [
            'CRASH_DATETIME', 'CRASH_YEAR', 'BOROUGH',
            'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2',
            'VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2',
            'MOST_COMMON_SEX',
            'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED'
        ]

        # Load only first 500-1000 rows (adjust based on memory)
        df = pd.read_csv(
            file_url,
            usecols=needed_columns,
            nrows=500,        # small sample for free deploy
            low_memory=False
        )

        # Convert datetime
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'], errors='coerce')
            df['CRASH_MONTH'] = df['CRASH_DATETIME'].dt.month
            df['CRASH_HOUR'] = df['CRASH_DATETIME'].dt.hour

        # Convert categorical columns to category type (saves memory)
        for col in ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2',
                    'VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'MOST_COMMON_SEX']:
            if col in df.columns:
                df[col] = df[col].astype('category')

        print(f"✅ Loaded {len(df)} rows (optimized for deployment)")

        return df

    except Exception as e:
        print(f"ERROR: {e}")
        return pd.DataFrame()

    
# --- Filtering Functions ---
def get_options(df, column_name):
    
    #Check if dataframe is empty or column does not exist
    if df.empty or column_name not in df.columns:
        return []
    
    # Get unique values and convert to string
    items = df[column_name].astype(str).unique()
    
    # Filter out nan/null strings
    clean_items = [i for i in items if i.lower() not in ['nan', 'none', '', 'null']]
    
    # Return sorted top 50
    return [{'label': i, 'value': i} for i in sorted(clean_items)][:50]

# --- Apply all filters function ---
def filter_dataframe(df, inputs):
    
    # Check if dataframe is empty
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
    
    #Looping over the dataFrame to apply filters
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