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