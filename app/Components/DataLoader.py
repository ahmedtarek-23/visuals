import pandas as pd


def load_data():
    """
    Loads crash data from Google Cloud Storage.
    Returns a processed pandas DataFrame with datetime features.
    """
    try:
        # For deployment, use a smaller sample or aggregated data
        file_url = "https://storage.googleapis.com/crashes_datadet/merged_crashes.csv"
        print("Loading optimized dataset...")
        
        df = pd.read_csv(file_url, low_memory=False, nrows=10000)
        
        print(f"Loaded {len(df):,} rows (optimized for deployment)")
        
        # Minimal processing
        if 'CRASH_DATETIME' in df.columns:
            df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH_DATETIME'], errors='coerce')
            df['CRASH_MONTH'] = df['CRASH_DATETIME'].dt.month
            df['CRASH_HOUR'] = df['CRASH_DATETIME'].dt.hour
            df['CRASH_YEAR'] = df['CRASH_DATETIME'].dt.year  # Added for year filtering
        
        text_columns = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2', 
                       'VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'MOST_COMMON_SEX']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        print(f"✅ Data processed successfully. Columns: {len(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()  # Print full error traceback for debugging
        # Return empty dataframe as fallback
        return pd.DataFrame()

    
# --- Filtering Functions ---
def get_options(df, column_name):
    """
    Extract unique values from a column for dropdown options.
    
    Args:
        df: pandas DataFrame
        column_name: Name of the column to extract values from
        
    Returns:
        list: List of dictionaries with 'label' and 'value' keys
    """
    # Check if dataframe is empty or column does not exist
    if df.empty or column_name not in df.columns:
        return []
    
    # Get unique values and convert to string
    items = df[column_name].astype(str).unique()
    
    # Filter out nan/null strings
    clean_items = [i for i in items if i.lower() not in ['nan', 'none', '', 'null', 'unknown']]
    
    # Return sorted top 50 (sorted for better UX)
    return [{'label': i, 'value': i} for i in sorted(clean_items)][:50]


# --- Apply all filters function ---
def filter_dataframe(df, inputs):
    """
    Applies multiple filters to the DataFrame based on user input.
    
    Args:
        df: pandas DataFrame to filter
        inputs: dictionary with filter keys and values
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    # Check if dataframe is empty
    if df.empty: 
        return df
    
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
    
    # Looping over the DataFrame to apply filters
    for key, col in filter_map.items():
        value = inputs.get(key)
        
        # Skip if no value or 'ALL' selected or column doesn't exist
        if not value or value == 'ALL' or col not in dff.columns:
            continue
            
        # Handle numeric year vs string columns
        if key == 'year':
            try:
                dff = dff[dff[col] == int(value)]
            except (ValueError, TypeError):
                pass  # Ignore if year conversion fails
        else:
            # For string columns, handle case-insensitive matching
            dff = dff[dff[col].astype(str).str.strip() == str(value).strip()]
                
    return dff
