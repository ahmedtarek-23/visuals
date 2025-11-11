import dash
from dash import html
from Components.filters import create_dropdown, create_search_bar
from Components.charts import create_bar_chart
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("cleaned_dataset.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("NYC Motor Vehicle Collisions Dashboard"),
    
    # Filters
    html.Div([
        create_dropdown("borough-dropdown", df["BOROUGH"].dropna().unique(), "Select Borough"),
        create_dropdown("year-dropdown", sorted(df["CRASH_YEAR"].dropna().unique()), "Select Year"),
        create_search_bar("search-bar")
    ], style={"display": "flex", "gap": "20px"}),

    html.Button("Generate Report", id="generate-btn", n_clicks=0),

    # Charts
    html.Div(id="charts-container")
])

@app.callback(
    dash.dependencies.Output("charts-container", "children"),
    [dash.dependencies.Input("generate-btn", "n_clicks")],
    [dash.dependencies.State("borough-dropdown", "value"),
     dash.dependencies.State("year-dropdown", "value"),
     dash.dependencies.State("search-bar", "value")]
)
def update_charts(n_clicks, borough, year, search):
    if n_clicks == 0:
        return []
    
    filtered_df = df.copy()
    if borough:
        filtered_df = filtered_df[filtered_df["BOROUGH"] == borough]
    if year:
        filtered_df = filtered_df[filtered_df["CRASH_YEAR"] == year]
    if search:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    
    return [
        create_bar_chart(filtered_df, "VEHICLE_TYPE_CODE1", "NUMBER_OF_PERSONS_INJURED", "Injuries by Vehicle Type")
    ]

if __name__ == "__main__":
    app.run_server(debug=True)