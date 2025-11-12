import plotly.express as px
import pandas as pd # Needed for value_counts() and reset_index()

# --- 1. CRASHES BY BOROUGH CHART ---

def create_borough_crash_bar_chart(df_filtered):
    """
    Generates a Plotly Bar Chart showing the count of crashes per Borough.
    
    Args:
        df_filtered (pd.DataFrame): The data subset after filtering.
        
    Returns:
        plotly.graph_objects.Figure: The interactive Plotly chart object.
    """
    if df_filtered.empty:
        # Create a blank plot if no data is available
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
    
    # Apply aesthetic updates for better visualization
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig


# --- 2. INJURIES BY VEHICLE TYPE CHART (NEW) ---

def create_injury_vehicle_bar_chart(df_filtered):
    """
    Generates a Plotly Bar Chart showing total injuries summed up by Vehicle Type.
    
    Args:
        df_filtered (pd.DataFrame): The data subset after filtering.
        
    Returns:
        plotly.graph_objects.Figure: The interactive Plotly chart object.
    """
    if df_filtered.empty:
        return px.bar(title="No Data to Display")

    # Group by Vehicle Type and sum the number of injured persons
    injury_counts = df_filtered.groupby('VEHICLE TYPE CODE 1')['NUMBER OF PERSONS INJURED'].sum().reset_index()
    injury_counts.columns = ['Vehicle Type', 'Total Injuries']
    
    # Sort and take the top 10 for clarity on the chart
    injury_counts = injury_counts.sort_values(by='Total Injuries', ascending=False).head(10)

    fig = px.bar(
        injury_counts, 
        x='Vehicle Type', 
        y='Total Injuries', 
        color='Vehicle Type',
        title='Top 10 Total Injuries by Vehicle Type',
        labels={'Total Injuries': 'Sum of Injured Persons', 'Vehicle Type': 'Vehicle Type Code'},
        template='plotly_white'
    )
    
    fig.update_layout(
        font_family="Inter",
        title_font_size=20,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig
