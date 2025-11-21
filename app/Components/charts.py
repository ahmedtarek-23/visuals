import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Common template to fix the bug you had earlier
TEMPLATE = "plotly_white"

# --- Empty Figure function ---
def empty_fig(text="No Data"):

    # Returns an empty figure with a message
    return {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [{"text": text, "showarrow": False}]
        }
    }

# --- Stats Calculation function ---
def get_stats(df):

    # If the dataframe is empty, return zeros
    if df.empty: return "0", "0", "0", "0"
    

    crashes = len(df)
    injuries = df['NUMBER OF PERSONS INJURED'].sum() if 'NUMBER OF PERSONS INJURED' in df.columns else 0
    
    # Summing all fatality columns
    fatality_cols = ['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']
    fatalities = df[fatality_cols].sum().sum() if all(c in df.columns for c in fatality_cols) else 0
    
    #Averaging people involved if the column exists
    avg_people = df['PERSONS_INVOLVED_COUNT'].mean() if 'PERSONS_INVOLVED_COUNT' in df.columns else 0
    

    return f"{crashes:,}", f"{int(injuries):,}", f"{int(fatalities):,}", f"{avg_people:.1f}"

# --- Bar chart Creation Functions ---
def create_bar(df):

    """Bar: Total Injuries by Borough."""
    if df.empty: return empty_fig()
    data = df.groupby('BOROUGH')['NUMBER OF PERSONS INJURED'].sum().reset_index()
    fig = px.bar(data, x='BOROUGH', y='NUMBER OF PERSONS INJURED', title="Injuries by Borough")
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E6EEF6"
)

    return fig

# --- Pie chart Creation Functions ---
def create_pie(df):
    """Pie: Top Contributing Factors."""
    if df.empty: return empty_fig()
    data = df['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(10)
    fig = px.pie(names=data.index, values=data.values, title="Top Contributing Factors")
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E6EEF6"
)

    return fig

# --- Heatmap Creation Functions ---
def create_empty_heatmap(message):
    """Create an empty heatmap with error message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        title={
            'text': 'Crash Frequency by Time and Day',
            'x': 0.5,
            'xanchor': 'center',
        },
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
         paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E6EEF6"
    )
    return fig

def create_heatmap(df):
    """
    Simple heatmap focusing on time patterns
    """
    try:
        # Sample data creation if your dataframe doesn't have time/date columns
        # Replace this with your actual data processing
        dff = df.copy()
        
        # If you don't have time data, create a sample heatmap with available data
        # This is a fallback - adjust based on your actual data structure
        if all(col in dff.columns for col in ['BOROUGH', 'NUMBER OF PERSONS INJURED']):
            # Example: Heatmap of injuries by borough and crash hour (if available)
            if 'CRASH TIME' in dff.columns:
                dff['HOUR'] = pd.to_datetime(dff['CRASH TIME'], errors='coerce').dt.hour
                pivot_data = dff.pivot_table(
                    index='BOROUGH',
                    columns='HOUR',
                    values='NUMBER OF PERSONS INJURED',
                    aggfunc='sum',
                    fill_value=0
                )
            else:
                # Fallback: use whatever columns you have
                numeric_cols = dff.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    pivot_data = dff[numeric_cols[:5]].corr()
                else:
                    return create_empty_heatmap("Insufficient data for heatmap")
        
        fig = px.imshow(
            pivot_data,
            color_continuous_scale='Viridis',
            aspect="auto",
            title="Crash Data Heatmap"
        )
        
        fig.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#E6EEF6"
)
        return fig
        
    except Exception as e:
        print(f"Error in create_heatmap: {e}")
        return create_empty_heatmap("Error generating heatmap")

# --- Map Creation Functions ---
def create_map(df):
    """Map: Crash Locations (Sampled)."""
    if df.empty or 'LATITUDE' not in df.columns: return empty_fig("No Location Data")
    # Sample 2000 points
    data = df.dropna(subset=['LATITUDE', 'LONGITUDE']).head(2000)
    fig = px.scatter_mapbox(data, lat='LATITUDE', lon='LONGITUDE', color='NUMBER OF PERSONS INJURED',
                            zoom=9, mapbox_style="open-street-map", title="Crash Locations")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E6EEF6",
     margin={"r":0,"t":40,"l":0,"b":0})
    
    return fig

# --- Line chart Creation Functions ---
def create_line(df):
    """
    Create a line chart showing crash trends over time
    """
    try:
        dff = df.copy()
        
        
        # Option 1: Try to use date column for monthly/daily trends
        date_columns = ['CRASH DATE', 'CRASH_DATE', 'Date', 'date']
        date_col = None
        
        for col in date_columns:
            if col in dff.columns:
                date_col = col
                break
        
        if date_col:
            return create_date_based_line(dff, date_col)
        
        # Option 2: Use year column if that's all we have
        year_col = 'CRASH_YEAR'
        if year_col in dff.columns:
            return create_year_based_line(dff, year_col)
        
        return create_empty_line("No date or year columns found")
        
    except Exception as e:
        print(f"Error creating line chart: {e}")
        import traceback
        traceback.print_exc()
        return create_empty_line("Error generating line chart")

# ---functions for line chart ---
def create_date_based_line(df, date_col):
    """Create line chart using date column for proper time series"""
    dff = df.copy()
    
    # Convert to datetime
    dff['DATE'] = pd.to_datetime(dff[date_col], errors='coerce')
    dff = dff.dropna(subset=['DATE'])
    
    if dff.empty:
        return create_empty_line("No valid date data available")
    
    # Extract different time periods
    dff['YEAR'] = dff['DATE'].dt.year
    dff['MONTH'] = dff['DATE'].dt.month
    dff['YEAR_MONTH'] = dff['DATE'].dt.to_period('M')
    dff['DATE_ONLY'] = dff['DATE'].dt.date
    
    print(f"Date range: {dff['DATE'].min()} to {dff['DATE'].max()}")
    print(f"Years in data: {sorted(dff['YEAR'].unique())}")
    
    # Determine the best time grouping based on data span
    date_range = dff['DATE'].max() - dff['DATE'].min()
    
    if date_range.days <= 31:  # Less than 1 month - use daily
        time_data = dff.groupby('DATE_ONLY').size().reset_index(name='CRASH_COUNT')
        time_data = time_data.sort_values('DATE_ONLY')
        x_col = 'DATE_ONLY'
        x_title = "Date"
        title_suffix = "Daily"
        
    elif date_range.days <= 365:  # Less than 1 year - use monthly
        time_data = dff.groupby('YEAR_MONTH').size().reset_index(name='CRASH_COUNT')
        time_data = time_data.sort_values('YEAR_MONTH')
        time_data['YEAR_MONTH_STR'] = time_data['YEAR_MONTH'].astype(str)
        x_col = 'YEAR_MONTH_STR'
        x_title = "Month"
        title_suffix = "Monthly"
        
    else:  # More than 1 year - use yearly
        time_data = dff.groupby('YEAR').size().reset_index(name='CRASH_COUNT')
        time_data = time_data.sort_values('YEAR')
        x_col = 'YEAR'
        x_title = "Year"
        title_suffix = "Yearly"
    
    print(f"Using {title_suffix} grouping")
    print(f"Time data points: {len(time_data)}")
    
    # Create line chart
    fig = px.line(
        time_data,
        x=x_col,
        y='CRASH_COUNT',
        title=f'Crash Trends ({title_suffix})',
        labels={x_col: x_title, 'CRASH_COUNT': 'Number of Crashes'}
    )
    
    # Add markers and customize
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        hovertemplate=f'<b>{x_title}: %{{x}}</b><br>Crash Count: %{{y:,}}<extra></extra>'
    )
    
    fig.update_layout(
        title={'text': f'Crash Trends ({title_suffix})', 'x': 0.5, 'font': {'size': 20}},
        xaxis_title=x_title,
        yaxis_title="Number of Crashes",
        height=500,
        showlegend=False,
        margin=dict(l=60, r=50, t=80, b=80),
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E6EEF6",
        paper_bgcolor="rgba(0,0,0,0)",

    )
    
    # Rotate x-axis labels if there are many points
    if len(time_data) > 6:
        fig.update_xaxes(tickangle=45)
    
    fig.update_yaxes(tickformat=',')
    
    return fig

# ---functions for line chart ---
def create_year_based_line(df, year_col):
    """Create line chart using only year column"""
    dff = df.copy()
    
    # Clean year data
    dff['YEAR'] = pd.to_numeric(dff[year_col], errors='coerce')
    dff = dff.dropna(subset=['YEAR'])
    
    if dff.empty:
        return create_empty_line("No valid year data available")
    
    # Group by year
    yearly_trend = dff.groupby('YEAR').size().reset_index(name='CRASH_COUNT')
    yearly_trend = yearly_trend.sort_values('YEAR')
    
    print(f"Years: {yearly_trend['YEAR'].tolist()}")
    print(f"Counts: {yearly_trend['CRASH_COUNT'].tolist()}")
    
    # If we only have one year, show a message
    if len(yearly_trend) <= 1:
        return create_empty_line(f"Only one year of data available ({yearly_trend['YEAR'].iloc[0]})")
    
    # Create line chart
    fig = px.line(
        yearly_trend,
        x='YEAR',
        y='CRASH_COUNT',
        title='Yearly Crash Trends',
        labels={'YEAR': 'Year', 'CRASH_COUNT': 'Number of Crashes'}
    )
    
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=10),
        line=dict(width=4),
        hovertemplate='<b>Year: %{x}</b><br>Crash Count: %{y:,}<extra></extra>'
    )
    
    fig.update_layout(
        title={'text': 'Yearly Crash Trends', 'x': 0.5, 'font': {'size': 20}},
        xaxis_title="Year",
        yaxis_title="Number of Crashes",
        height=500,
        showlegend=False,
        margin=dict(l=60, r=50, t=80, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E6EEF6"
    )
    
    fig.update_xaxes(tickformat='d')
    fig.update_yaxes(tickformat=',')
    
    return fig

# --- Empty line chart function ---
def create_empty_line(message):
    """Create empty line chart with message"""
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E6EEF6"
    )
    return fig
