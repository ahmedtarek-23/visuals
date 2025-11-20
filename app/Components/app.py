<<<<<<< HEAD
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import DataLoader
import charts

# Initialize
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df = DataLoader.load_data()

LIGHT_THEME = dbc.themes.BOOTSTRAP
DARK_THEME  = dbc.themes.DARKLY

# --- Components Helper ---
def make_dropdown(label, id, col):
    return dbc.Col(
        children=[
            dbc.Label(label, className="fw-bold"),
            dcc.Dropdown(id=id, options=DataLoader.get_options(df, col), placeholder="All")
        ],
        md=4,
        className="mb-3"
    )

# --- Layout ---
app.layout = dbc.Container([


    dbc.NavbarSimple(brand="NYC Traffic Crashes Dashboard", color="dark", dark=True, className="mb-4" ),
    
    # Filters Section (7 Filters as requested)
    dbc.Card([
        dbc.CardHeader("Data Filters"),
        dbc.CardBody([
            dbc.Row([
                make_dropdown("Borough", "Borough-dropdown", "BOROUGH"),
                make_dropdown("Factor", "Factor-dropdown", "CONTRIBUTING FACTOR VEHICLE 1"),
                make_dropdown("Vehicle ", "Vehicle-dropdown", "VEHICLE TYPE CODE 1"),
                make_dropdown("Demographic", "Demographic-dropdown", "MOST_COMMON_SEX"),
            ]),

            dbc.Row([
                dcc.Slider(id="year-slider", min=2009, max=2023, step=1, marks={y: str(y) for y in range(2009, 2024)}, value=2023),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dbc.Button("Generate Report", id="btn-gen", color="success", className="me-2"),
                    dbc.Button("Reset", id="btn-reset", color="secondary")
                ], md=4, className="d-flex align-items-center")
            ]),
            dbc.Row([
             dbc.Col([
               dbc.Label("Search", className="fw-bold"),
                 dcc.Input(
                 id="search-input",
                 type="text",
                 placeholder="Type to search...",
                 debounce=True,  # triggers callback after user stops typing
                style={"width": "100%"}
              )], md=4, className="mb-3"),
           ])
            
        ])
    ], className="mb-4"),

    # Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Crash"), html.P("Total Crashes")])], color="primary", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Injuries"), html.P("Total Injuries")])], color="warning", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Fatalities"), html.P("Total Fatalities")])], color="danger", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-average"), html.P("Avg Persons Involved")])], color="info", inverse=True)),
    ], className="mb-4"),

    # Charts Grid
    dbc.Row([
        dbc.Col(dcc.Graph(id="Bar_chart"), md=6),
        dbc.Col(dcc.Graph(id="Pie_chart"), md=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="line_graph"), md=6),
        dbc.Col(dcc.Graph(id="heat_map"), md=6),
    ], className="mb-4"),
    
    dbc.Row(dbc.Col(dcc.Graph(id="Map"), md=12))

], fluid=True)

# --- Callbacks ---
@app.callback([
    Output('Borough-dropdown', 'value'),
    Output('Demographic-dropdown', 'value'),
    Output('Vehicle-dropdown', 'value'),
    Output('Factor-dropdown', 'value'),
    Output('year-slider', 'value'),
    Output('search-input', 'value')

    ],

    [
    Input('btn-reset', 'n_clicks')
    ]
)
def reset_filters(n):
     return None, None , None , None, 2023 , ""

@app.callback(
    [
        Output('C-Crash', 'children'), 
        Output('C-Injuries', 'children'), 
        Output('C-Fatalities', 'children'), 
        Output('C-average', 'children'),
        Output('Bar_chart', 'figure'), 
        Output('Pie_chart', 'figure'), 
        Output('line_graph', 'figure'), 
        Output('heat_map', 'figure'), 
        Output('Map', 'figure'),
    ],
    [
        Input('btn-gen', 'n_clicks'),
    ],
    [
        State('Borough-dropdown', 'value'), 
        State('Demographic-dropdown', 'value'),
        State('Vehicle-dropdown', 'value'),
        State('Factor-dropdown', 'value'),
        State('year-slider', 'value'),
        State('search-input', 'value')
    ]
)
def update_dashboard(n, bor, demo, veh, fac, year_slider, search_text):

    # Filter data
    inputs = {'borough': bor, 'factor1': fac , 'vehicle1': veh  ,'year': year_slider, 'demographic': demo}
    dff = DataLoader.filter_dataframe(df, inputs)
    
    
    if search_text:
        search_text = search_text.lower()
        # Example: search in borough, vehicle, and factor columns
        search_cols = ['BOROUGH', 'VEHICLE TYPE CODE 1', 'CONTRIBUTING FACTOR VEHICLE 1']
        dff = dff[dff[search_cols].apply(lambda row: row.astype(str).str.lower().str.contains(search_text).any(), axis=1)]

    # Stats
    s1, s2, s3, s4 = charts.get_stats(dff)

    # Charts with template
    return s1, s2, s3, s4, \
           charts.create_bar(dff), charts.create_pie(dff), \
           charts.create_line(dff), charts.create_heatmap(dff), charts.create_map(dff)



if __name__ == '__main__':
    app.run(debug=True, port=8050)

=======
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
>>>>>>> 480bb322dd19cd8d6c794cce494e2c0854070169
