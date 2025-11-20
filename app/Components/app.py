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

