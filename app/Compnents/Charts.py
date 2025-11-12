import plotly.express as px
import pandas as pd # Needed for value_counts() and reset_index()

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

# Note: Add more functions here for other required charts (e.g., Line Chart for Trends, Heatmap, etc.)