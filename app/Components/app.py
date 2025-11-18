from dash.dependencies import Input, Output, State
import dash
import plotly.express as px

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts import Bar_chart, Pie_chart
from DataLoader import load_data, Brough_options, CRASH_YEAR, Contributing_Factor1, Contributing_Factor2, Vehicle1, Vehicle2, Injury

df = load_data()  # now your app can use df anywhere

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], suppress_callback_exceptions=True)

app.layout = html.Div([

    html.H1("Analytical Dashboard", style={"text-align": "center", "margin-bottom": "30px"}),

    dbc.Container([

        dbc.Row([
            dcc.Dropdown(id="my-BroughDropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": b, "value": b} for b in Brough_options],
                         placeholder="Select Borough....",
                         multi=False,
                         style={"width": "200px"}),

            dcc.Dropdown(id="year-dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": y, "value": y} for y in CRASH_YEAR],
                         placeholder="Select Year....",
                         multi=False,
                         style={"width": "200px"}),

            dcc.Dropdown(id="Controbuting1_Dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": c, "value": c} for c in Contributing_Factor1],
                         placeholder="Select Contributing factor 1....",
                         multi=False,
                         style={"width": "300px"}),

            dcc.Dropdown(id="Controbuting2_Dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": l, "value": l} for l in Contributing_Factor2],
                         placeholder="Select Contributing factor 2....",
                         multi=False,
                         style={"width": "200px"}),
        ], className="Rows 1"),

        dbc.Row([
            dcc.Dropdown(id="Vehicle1_Dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": v, "value": v} for v in Vehicle1],
                         placeholder="Select Vehicle type 1....",
                         multi=False,
                         style={"width": "200px"}),

            dcc.Dropdown(id="Vehicle2_Dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": f, "value": f} for f in Vehicle2],
                         placeholder="Select Vehicle type 2....",
                         multi=False,
                         style={"width": "200px"}),

            dcc.Dropdown(id="Injury_dropdown",
                         options=[{"label": "All", "value": "ALL"},
                                  {"label": "None", "value": "NONE"}] +
                                 [{"label": i, "value": i} for i in Injury],
                         placeholder="Select Injury Type....",
                         multi=False,
                         style={"width": "200px"}),
        ], className="Rows 2"),

        html.Div([
            html.Button("Generate Report", id="generate-report-button", n_clicks=0)
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="pie-chart"), width=6),
            dbc.Col(dcc.Graph(id="Bar_chart"), width=6)
        ], className="Graphs-Rows"),

        html.Div(id="output")

    ], fluid=True)

])

@app.callback(
    [
        Output('Bar_chart', 'figure'),
        Output('pie-chart', 'figure'),
    ],
    Input('generate-report-button', 'n_clicks'),
    State("my-BroughDropdown", "value"),
    State("year-dropdown", "value"),
    State("Controbuting1_Dropdown", "value"),
    State("Controbuting2_Dropdown", "value"),
    State("Vehicle1_Dropdown", "value"),
    State("Vehicle2_Dropdown", "value"),
    State("Injury_dropdown", "value"),
)
def update_charts(n_clicks, selected_boroughs, selected_year,
                  Selected_Contributing1, Selected_Contributing2,
                  Selected_Vehicle1, Selected_Vehicle2, Selected_Injury):

    if n_clicks == 0:
        return dash.no_update

    df_filtered = df.copy()

    if selected_boroughs == "ALL":
        pass
    elif selected_boroughs == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["BOROUGH"] == selected_boroughs]

    if selected_year == "ALL":
        pass
    elif selected_year == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["CRASH_YEAR"] == selected_year]

    if Selected_Contributing1 == "ALL":
        pass
    elif Selected_Contributing1 == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["CONTRIBUTING FACTOR VEHICLE 1"] == Selected_Contributing1]

    if Selected_Contributing2 == "ALL":
        pass
    elif Selected_Contributing2 == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["CONTRIBUTING FACTOR VEHICLE 2"] == Selected_Contributing2]

    if Selected_Vehicle1 == "ALL":
        pass
    elif Selected_Vehicle1 == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["VEHICLE TYPE CODE 1"] == Selected_Vehicle1]

    if Selected_Vehicle2 == "ALL":
        pass
    elif Selected_Vehicle2 == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["VEHICLE TYPE CODE 2"] == Selected_Vehicle2]

    if Selected_Injury == "ALL":
        pass
    elif Selected_Injury == "NONE":
        pass
    else:
        df_filtered = df_filtered[df_filtered["PERSON_INJURY"] == Selected_Injury]

    # If df_filtered is empty, return empty figures
    if df_filtered.empty:
        return px.bar(title="No data available"), px.pie(title="No data available")

    bar_fig = Bar_chart(df_filtered)
    pie_fig = Pie_chart(df_filtered, "CONTRIBUTING FACTOR VEHICLE 1")

    return bar_fig, pie_fig


if __name__ == "__main__":
    app.run(debug=True)
