<<<<<<< HEAD
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Common Template ---
TEMPLATE = "plotly_white"

def empty_fig(message="No Data"):
    """Returns a blank figure with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        title={'text': message, 'x': 0.5},
        height=500,
        plot_bgcolor='white'
    )
    return fig

# --- Stats for top cards ---
def get_stats(df):
    if df.empty: return "0", "0", "0", "0"
    
    crashes = len(df)
    injuries = df['NUMBER OF PERSONS INJURED'].sum() if 'NUMBER OF PERSONS INJURED' in df.columns else 0
    fatality_cols = ['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']
    fatalities = df[fatality_cols].sum().sum() if all(c in df.columns for c in fatality_cols) else 0
    avg_people = df['PERSONS_INVOLVED_COUNT'].mean() if 'PERSONS_INVOLVED_COUNT' in df.columns else 0
    
    return f"{crashes:,}", f"{int(injuries):,}", f"{int(fatalities):,}", f"{avg_people:.1f}"

# --- Bar Chart ---
def create_bar(df):
    """Bar chart: Total Injuries by Borough"""
    if df.empty or 'BOROUGH' not in df.columns: return empty_fig("No Data for Bar Chart")
    
    data = df.groupby('BOROUGH')['NUMBER OF PERSONS INJURED'].sum().reset_index()
    fig = px.bar(
        data,
        x='BOROUGH',
        y='NUMBER OF PERSONS INJURED',
        title="Total Injuries by Borough",
        text_auto=True
    )
    fig.update_layout(template=TEMPLATE, xaxis_title="Borough", yaxis_title="Total Injuries")
    return fig

# --- Pie Chart ---
def create_pie(df, column_name='CONTRIBUTING FACTOR VEHICLE 1'):
    """Pie chart: Top N categories"""
    if df.empty or column_name not in df.columns: 
        return empty_fig(f"No Data for {column_name}")
    
    pie_data = df[column_name].value_counts().head(10).reset_index()
    pie_data.columns = ["Category", "Count"]

    fig = px.pie(
        pie_data,
        names="Category",
        values="Count",
        title=f"Top 10 {column_name}",
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(template=TEMPLATE)
    return fig

# --- Heatmap ---
def create_heatmap(df):
    """Heatmap of crashes by borough and hour"""
    if df.empty: return empty_fig("No Data for Heatmap")
    
    try:
        dff = df.copy()
        if 'CRASH_HOUR' not in dff.columns or 'BOROUGH' not in dff.columns:
            return empty_fig("Insufficient data for heatmap")
        
        pivot_data = dff.pivot_table(
            index='BOROUGH',
            columns='CRASH_HOUR',
            values='NUMBER OF PERSONS INJURED',
            aggfunc='sum',
            fill_value=0
        )
        fig = px.imshow(
            pivot_data,
            color_continuous_scale='Viridis',
            aspect="auto",
            title="Crash Injuries by Borough and Hour"
        )
        fig.update_layout(height=500, template=TEMPLATE)
        return fig
    except Exception as e:
        print(f"Error in create_heatmap: {e}")
        return empty_fig("Error generating heatmap")

# --- Map ---
def create_map(df):
    """Map: Sample crash locations"""
    if df.empty or 'LATITUDE' not in df.columns or 'LONGITUDE' not in df.columns:
        return empty_fig("No Location Data")
    
    data = df.dropna(subset=['LATITUDE', 'LONGITUDE']).head(2000)
    fig = px.scatter_mapbox(
        data,
        lat='LATITUDE',
        lon='LONGITUDE',
        color='NUMBER OF PERSONS INJURED',
        zoom=9,
        mapbox_style="open-street-map",
        title="Crash Locations"
    )
    fig.update_layout(template=TEMPLATE, margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# --- Line Chart ---
def create_line(df):
    """Line chart: Crash trends over time"""
    try:
        dff = df.copy()
        if 'CRASH_DATETIME' in dff.columns:
            dff['DATE'] = pd.to_datetime(dff['CRASH_DATETIME'], errors='coerce')
        elif 'CRASH_DATE' in dff.columns:
            dff['DATE'] = pd.to_datetime(dff['CRASH_DATE'], errors='coerce')
        else:
            return create_empty_line("No date column found")
        
        dff = dff.dropna(subset=['DATE'])
        if dff.empty: return create_empty_line("No valid date data")
        
        # Monthly trend
        time_data = dff.groupby(dff['DATE'].dt.to_period('M')).size().reset_index(name='CRASH_COUNT')
        time_data['DATE_STR'] = time_data['DATE'].astype(str)
        fig = px.line(
            time_data,
            x='DATE_STR',
            y='CRASH_COUNT',
            title="Crash Trends (Monthly)",
            labels={'DATE_STR': 'Month', 'CRASH_COUNT': 'Number of Crashes'}
        )
        fig.update_traces(mode='lines+markers', marker=dict(size=8), line=dict(width=3))
        fig.update_layout(template=TEMPLATE, height=500, xaxis_tickangle=45)
        return fig
    except Exception as e:
        print(f"Error in create_line: {e}")
        return create_empty_line("Error generating line chart")

def create_empty_line(message):
    """Fallback for line chart"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        title={'text': 'Crash Trends', 'x': 0.5},
        height=500,
        plot_bgcolor='white'
    )
    return fig
=======
import plotly.express as px

def Bar_chart(df_filtered):
    """
    Generates a bar chart showing total injuries by borough.
    """
    # PERFORMANCE FIX: Aggregate data before plotting.
    # Without this, px.bar tries to plot individual rows (thousands of bars), 
    # which will crash the browser.
    bar_data = (
        df_filtered.groupby('BOROUGH')['NUMBER OF PERSONS INJURED']
        .sum()
        .reset_index()
    )
    
    figBar = px.bar(
        bar_data,
        x='BOROUGH',
        y='NUMBER OF PERSONS INJURED',
        title='Total Injuries by Borough', # Updated title to match data (Injuries, not just crash counts)
        text_auto=True # Displays the numbers on top of the bars
    )
    
    # Optional: Make it look cleaner
    figBar.update_layout(xaxis_title="Borough", yaxis_title="Total Injuries")
    
    return figBar


def Pie_chart(df_filtered, column_name):
    """
    Creates a pie chart for any categorical column.

    Args:
        df_filtered (pd.DataFrame): filtered data based on user selection
        column_name (str): name of column to visualize in pie chart
    """
    # Safety check: ensure column exists
    if column_name not in df_filtered.columns:
        return px.pie(title=f"Error: {column_name} not found")

    pie_data = (
        df_filtered[column_name]
        .dropna()
        .value_counts()
        .reset_index()
    )

    pie_data.columns = ["Category", "Count"]

    figPie = px.pie(
        pie_data,
        names="Category", # Syntax error fixed here (removed the trailing 'a')
        values="Count",
        title=f"Distribution of {column_name}",
        hole=0.3 # Adds a donut style for better aesthetics
    )
    
    figPie.update_traces(textinfo='percent+label')

    return figPie
>>>>>>> 2578d97bd5cb1d8a7481b4701ed58e89af6a41af
