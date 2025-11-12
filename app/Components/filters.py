import pandas as pd
import plotly.express as px

# --- 1. FILTER GENERATION ---

def get_filter_options(df):
    """
    Generates dynamic lists of unique values for dropdown filters.
    
    Args:
        df (pd.DataFrame): The fully cleaned and merged dataset.
        
    Returns:
        dict: Dictionary containing lists of filter options.
    """
    # Use a set to hold columns that must be dynamically generated
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
             # Fallback if a key column is missing (e.g., from pre-cleaning)
             options[col] = ['ALL', 'Data Missing'] 

    return options


# --- 2. DATA FILTERING ---

def filter_data(df, filters, search_term):
    """
    Filters the DataFrame based on dropdown selections and search query.
    
    Args:
        df (pd.DataFrame): The full integrated dataset.
        filters (dict): Dictionary of user-selected dropdown values.
        search_term (str): User input for the search mode.
        
    Returns:
        pd.DataFrame: The filtered subset of the data.
    """
    df_filtered = df.copy()
    
    # 1. Apply Dropdown Filters
    for key, value in filters.items():
        # Map the filter key to the actual column name in your CSV
        col_map = {
            'borough': 'BOROUGH',
            'year': 'CRASH_YEAR',
            'factor': 'CONTRIBUTING FACTOR VEHICLE 1',
            'vehicleType': 'VEHICLE TYPE CODE 1'
        }
        
        col_name = col_map.get(key)
        
        if col_name and value != 'ALL':
            df_filtered = df_filtered[df_filtered[col_name].astype(str) == str(value)]

    # 2. Apply Search Term (Example: filter by partial match in contributing factor or borough)
    if search_term:
        search_term_lower = search_term.lower()
        
        # Combine relevant columns into a single string for robust searching
        search_columns = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 1']
        
        # Create a boolean mask: True if search term is found in any of the search columns
        search_mask = False
        for col in search_columns:
            if col in df_filtered.columns:
                search_mask |= df_filtered[col].astype(str).str.lower().str.contains(search_term_lower, na=False)
        
        df_filtered = df_filtered[search_mask]
        
    return df_filtered


# --- 3. PLOTLY VISUALIZATION FUNCTION ---

def create_borough_crash_bar_chart(df_filtered):
    """
    Generates a Plotly Bar Chart showing the count of crashes per Borough.
    
    Args:
        df_filtered (pd.DataFrame): The data subset after filtering.
        
    Returns:
        plotly.graph_objects.Figure: The interactive Plotly chart object.
    """
    if df_filtered.empty:
        return px.bar(title="No Data to Display")

    # Count crashes per borough
    crash_counts = df_filtered['BOROUGH'].value_counts().reset_index()
    crash_counts.columns = ['Borough', 'Crash Count']

    fig = px.bar(
        crash_counts, 
        x='Borough', 
        y='Crash Count', 
        color='Borough',
        title='Total Crashes by Borough',
        labels={'Crash Count': 'Number of Collisions', 'Borough': 'NYC Borough'},
        template='plotly_white'
    )
    
    # Make the chart interactive and visually appealing
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig

# Note: You would add more functions here for other required charts (e.g., Line Chart for Trends, Heatmap, etc.)
