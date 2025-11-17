import plotly.express as px

def Bar_chart(df_filtered):
    figBar = px.bar(
        df_filtered,
        x='BROUGH',
        y='PERSON_INJURY',
        title='Number of Crashes by Borough'
    )
    return figBar


def Pie_chart(df_filtered, column_name):
    """
    Creates a pie chart for any categorical column.

    Args:
        df_filtered (pd.DataFrame): filtered data based on user selection
        column_name (str): name of column to visualize in pie chart
    """

    pie_data = (
        df_filtered[column_name]
        .dropna()
        .value_counts()
        .reset_index()
    )

    pie_data.columns = ["Category", "Count"]

    figPie = px.pie(
        pie_data,
        names="Category",
        values="Count",
        title=f"Distribution of {column_name}",
    )

    return figPie
