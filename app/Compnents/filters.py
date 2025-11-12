import pandas as pd

# --- 1. FILTER GENERATION ---

def get_filter_options(df):
    """
    Generates dynamic lists of unique values for dropdown filters.
    
    Args:
        df (pd.DataFrame): The fully cleaned and merged dataset.
        
    Returns:
        dict: Dictionary containing lists of filter options, keyed by column name.
    """
    # Use a set to hold columns that must be dynamically generated
    # NOTE: These column names must exactly match those in your merged_crashes_person.csv
    filter_cols = {
        'BOROUGH', 
        'CRASH_YEAR', 
        'CONTRIBUTING FACTOR VEHICLE 1', 
        'VEHICLE TYPE CODE 1'
    }
    
    options = {}
    
    for col in filter_cols:
        # Check if the column exists in the dataframe before processing
        if col in df.columns:
            # Drop nulls, convert to string, get unique values, and sort
            unique_values = sorted(
                df[col].astype(str).dropna().unique().tolist()
            )
            # Add 'ALL' option at the beginning
            options[col] = ['ALL'] + unique_values
        else:
             # Fallback if a key column is missing 
             options[col] = ['ALL', 'Data Missing'] 

    return options


# --- 2. DATA FILTERING ---

def filter_data(df, filters, search_term):
    """
    Filters the DataFrame based on dropdown selections and search query.
    
    Args:
        df (pd.DataFrame): The full integrated dataset.
        filters (dict): Dictionary of user-selected dropdown values (e.g., {'borough': 'QUEENS'}).
        search_term (str): User input for the search mode.
        
    Returns:
        pd.DataFrame: The filtered subset of the data.
    """
    df_filtered = df.copy()
    
    # 1. Apply Dropdown Filters
    for key, value in filters.items():
        # Map the filter key used in the frontend (e.g., 'borough') to the actual CSV column name
        col_map = {
            'borough': 'BOROUGH',
            'year': 'CRASH_YEAR',
            'factor': 'CONTRIBUTING FACTOR VEHICLE 1',
            'vehicleType': 'VEHICLE TYPE CODE 1'
        }
        
        col_name = col_map.get(key)
        
        if col_name and value != 'ALL':
            # Ensure comparison is robust by converting column to string
            df_filtered = df_filtered[df_filtered[col_name].astype(str) == str(value)]

    # 2. Apply Search Term 
    if search_term:
        search_term_lower = search_term.lower()
        
        # Columns to check for the search term
        search_columns = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 1']
        
        # Initialize a boolean mask to False
        search_mask = False
        for col in search_columns:
            if col in df_filtered.columns:
                # Use |= (bitwise OR assignment) to combine masks
                search_mask |= df_filtered[col].astype(str).str.lower().str.contains(search_term_lower, na=False)
        
        df_filtered = df_filtered[search_mask]
        
    return df_filtered