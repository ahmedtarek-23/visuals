import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from .DataLoader import load_data, get_options, filter_dataframe 
from .charts import (
    create_bar, create_pie, create_heatmap, create_map, create_line, get_stats,
    create_boxplot, create_stacked_bar, create_vehicle_analysis, create_person_type_pie
)
import pandas as pd

# Initialize
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY , "/assets/styles.css"])

#Initialize server for deployment
server = app.server

#Loading the data
df = load_data()

# --- Dropdown function ---
def make_dropdown(label, id, col):
    return dbc.Col(
        children=[
            dcc.Dropdown(id=id, options=get_options(df, col), placeholder="All")
        ],
        md=4,
        className="mb-3"
    )

# --- Layout ---
app.layout = dbc.Container([
    
    #introduce download component
    dcc.Download(id="download-report"),

    # --- Navbar ---
    dbc.NavbarSimple(brand="NYC Traffic Crashes Dashboard", color="dark", dark=True, className="mb-4" ),



    # --- Dropdown Cards ---
   dbc.Card([
    dbc.CardHeader("Filters"),
    dbc.CardBody([
        dbc.Row([
            make_dropdown("Borough", "Borough-dropdown", "BOROUGH"),
            make_dropdown("Factor", "Factor-dropdown", "CONTRIBUTING FACTOR VEHICLE 1"), 
            make_dropdown("Demographic", "Demographic-dropdown", "MOST_COMMON_SEX"),
        ])
    ])
], className="mb-4"),

    # --- Year Slider Card ---
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Year Selection"),
                dbc.CardBody([
                    dcc.Slider(
                        id="year-slider",
                        min=2009,
                        max=2023,
                        step=1,
                        marks={y: str(y) for y in range(2009, 2024)},
                        value=2023
                    )
                ])
            ], className="mb-3"), md=12
        )
    ]),

    # --- Generate Button Card ---
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Generate Report/Reset/Download"),
                dbc.CardBody([
                    dbc.Button("Generate Report", id="btn-gen", color="success", className="me-2"),
                    dbc.Button("Reset", id="btn-reset", color="secondary", className="me-2"),
                    dbc.Button("Download Data", id="Download-button", color="info")
                ])
            ], className="mb-3"), md=12
        ),        
    ]),

    # Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Crash"), html.P("Total Crashes")])], color="primary", inverse=True , className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Injuries"), html.P("Total Injuries")])], color="warning", inverse=True, className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Fatalities"), html.P("Total Fatalities")])], color="danger", inverse=True, className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-average"), html.P("Avg Persons Involved")])], color="info", inverse=True,className="hover-pop")),
    ], className="mb-4"),

    # ===== ORIGINAL 5 CHARTS =====
    dbc.Row([
        dbc.Col(dcc.Graph(id="Bar_chart" , className="hover-pop"), md=6),
        dbc.Col(dcc.Graph(id="Pie_chart", className="hover-pop"), md=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="line_graph" , className="hover-pop"), md=12),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="Map" , className="hover-pop"), md=6),
        dbc.Col(dcc.Graph(id="heat_map" , className="hover-pop"), md=6)
    ], className="mb-4"),

    # ===== NEW 4 CHARTS =====
    html.Hr(),
    html.H4("Advanced Analysis", className="mt-4 mb-3"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="boxplot_chart" , className="hover-pop"), md=6),
        dbc.Col(dcc.Graph(id="stacked_bar_chart", className="hover-pop"), md=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="vehicle_chart" , className="hover-pop"), md=6),
        dbc.Col(dcc.Graph(id="person_type_chart", className="hover-pop"), md=6)
    ], className="mb-4"),
    
], fluid=True)

# --- Callbacks for filtering ---
@app.callback([
    Output('Borough-dropdown', 'value'),
    Output('Demographic-dropdown', 'value'),
    Output('Factor-dropdown', 'value'),
    Output('year-slider', 'value'),
    ],
    [
    Input('btn-reset', 'n_clicks')
    ]
)

#Reseting values to filtering the whole datSet
def reset_filters(n):
     return None, None  , None, 2023

#Callback to update dashboard with ALL 9 CHARTS
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
        Output('boxplot_chart', 'figure'),
        Output('stacked_bar_chart', 'figure'),
        Output('vehicle_chart', 'figure'),
        Output('person_type_chart', 'figure'),
    ],
    [
        Input('btn-gen', 'n_clicks'),
    ],
    [
        State('Borough-dropdown', 'value'), 
        State('Demographic-dropdown', 'value'),
        State('Factor-dropdown', 'value'),
        State('year-slider', 'value'),
    ]
)
def update_dashboard(n, bor, demo, fac, year_slider):

    # Mapping the dataframe based on the filters
    inputs = {'borough': bor, 'factor1': fac  ,'year': year_slider, 'demographic': demo}
    
    #Apply all filters
    dff = filter_dataframe(df, inputs)
     
    # Getting stats
    s1, s2, s3, s4 = get_stats(dff)

    # Charts with template - ORIGINAL 5 + NEW 4
    return s1, s2, s3, s4, \
           create_bar(dff), create_pie(dff), \
           create_line(dff), create_heatmap(dff), create_map(dff), \
           create_boxplot(dff), create_stacked_bar(dff), \
           create_vehicle_analysis(dff), create_person_type_pie(dff)

# --- Download Callback ---
@app.callback(
    Output("download-report", "data"),
    Input("Download-button", "n_clicks"),
    [
        State('Borough-dropdown', 'value'),
        State('Factor-dropdown', 'value'),
        State('Demographic-dropdown', 'value'),
        State('year-slider', 'value'),
    ],
    prevent_initial_call=True
)

def download_csv(n_clicks, bor, fac, demo, year):

    # Filter dataframe
    inputs = {'borough': bor, 'factor1': fac,  'demographic': demo, 'year': year}

    dff = filter_dataframe(df, inputs)

    # Return CSV
    return dcc.send_data_frame(dff.to_csv, "nyc_traffic_crashes.csv", index=False)


if __name__ == '__main__':
    app.run(debug=True, port=8050)