import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Common template to fix the bug you had earlier
TEMPLATE = "plotly_white"

def empty_fig(text="No Data"):
    return {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [{"text": text, "showarrow": False}]
        }
    }

def get_stats(df):
    """Calculates the 4 numbers for the top cards."""
    if df.empty: return "0", "0", "0", "0"
    
    crashes = len(df)
    injuries = df['NUMBER OF PERSONS INJURED'].sum() if 'NUMBER OF PERSONS INJURED' in df.columns else 0
    
    # Summing all fatality columns
    fatality_cols = ['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']
    fatalities = df[fatality_cols].sum().sum() if all(c in df.columns for c in fatality_cols) else 0
    
    avg_people = df['PERSONS_INVOLVED_COUNT'].mean() if 'PERSONS_INVOLVED_COUNT' in df.columns else 0
    
    return f"{crashes:,}", f"{int(injuries):,}", f"{int(fatalities):,}", f"{avg_people:.1f}"

def create_bar(df):
    """Bar: Total Injuries by Borough."""
    if df.empty: return empty_fig()
    data = df.groupby('BOROUGH')['NUMBER OF PERSONS INJURED'].sum().reset_index()
    fig = px.bar(data, x='BOROUGH', y='NUMBER OF PERSONS INJURED', title="Injuries by Borough")
    fig.update_layout(template=TEMPLATE)
    return fig

def create_pie(df):
    """Pie: Top Contributing Factors."""
    if df.empty: return empty_fig()
    data = df['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(10)
    fig = px.pie(names=data.index, values=data.values, title="Top Contributing Factors")
    fig.update_layout(template=TEMPLATE)
    return fig

def create_line(df):
    """Line: Crashes per Month."""
    if df.empty or 'CRASH_MONTH' not in df.columns: return empty_fig()
    data = df.groupby('CRASH_MONTH').size().reset_index(name='COUNT')
    fig = px.line(data, x='CRASH_MONTH', y='COUNT', title="Crashes per Month", markers=True)
    fig.update_layout(template=TEMPLATE, xaxis=dict(tickmode='linear', tick0=1, dtick=1))
    return fig

def create_heatmap(df):
    """Heatmap: Hour vs Month."""
    if df.empty or 'CRASH_HOUR' not in df.columns: return empty_fig()
    data = df.groupby(['CRASH_MONTH', 'CRASH_HOUR']).size().reset_index(name='COUNT')
    fig = px.density_heatmap(data, x='CRASH_HOUR', y='CRASH_MONTH', z='COUNT', 
                             title="Heatmap: Month vs Hour", color_continuous_scale='Viridis')
    fig.update_layout(template=TEMPLATE)
    return fig

def create_map(df):
    """Map: Crash Locations (Sampled)."""
    if df.empty or 'LATITUDE' not in df.columns: return empty_fig("No Location Data")
    # Sample 2000 points
    data = df.dropna(subset=['LATITUDE', 'LONGITUDE']).head(2000)
    fig = px.scatter_mapbox(data, lat='LATITUDE', lon='LONGITUDE', color='NUMBER OF PERSONS INJURED',
                            zoom=9, mapbox_style="open-street-map", title="Crash Locations")
    fig.update_layout(template=TEMPLATE, margin={"r":0,"t":40,"l":0,"b":0})
    return fig