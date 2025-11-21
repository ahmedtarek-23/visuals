import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from .DataLoader import load_data, get_options, filter_dataframe 
from .charts import create_bar, create_pie, create_heatmap, create_map, create_line, get_stats
import pandas as pd
import os
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
            dbc.Label(label, className="fw-bold"),
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

    # --- Search Card ---
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Search"),
                dbc.CardBody([
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Type to search...",
                        debounce=True,
                        style={"width": "100%"}
                    )
                ])
            ], className="mb-3"), md=7
        ),

        # --- Generate Button Card ---
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Generate Report/Reset/Download"),
                dbc.CardBody([
                    dbc.Button("Generate Report", id="btn-gen", color="success", className="me-2"),
                      dbc.Button("Reset", id="btn-reset", color="secondary", className="me-2"),
                      dbc.Button("Download Data", id="Download-button", color="info")
                ])
            ], className="me-2"), md=5
        ),        
    ]),

    # Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Crash"), html.P("Total Crashes")])], color="primary", inverse=True , className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Injuries"), html.P("Total Injuries")])], color="warning", inverse=True, className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-Fatalities"), html.P("Total Fatalities")])], color="danger", inverse=True, className="hover-pop")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="C-average"), html.P("Avg Persons Involved")])], color="info", inverse=True,className="hover-pop")),
    ], className="mb-4"),

    # Grid Charts
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
])
    
], fluid=True)
 
# ---Search Function ---
def apply_search_filter(dataframe, search_text, logic="AND"):
    """
    Filters the dataframe based on search_text across multiple columns.
    Handles categoricals, numeric, and string columns safely.
    """
    if not search_text or not isinstance(search_text, str) or search_text.strip() == "":
        return dataframe

    # Normalize column names
    dataframe.columns = dataframe.columns.str.strip().str.upper()

    search_text_lower = search_text.lower().strip()
    search_terms = search_text_lower.split()

    # Define searchable columns
    search_columns = [
        'BOROUGH', 
        'VEHICLE TYPE CODE 1', 
        'CONTRIBUTING FACTOR VEHICLE 1',
        'MOST_COMMON_SEX',
        'VEHICLE TYPE CODE 2',
        'CONTRIBUTING FACTOR VEHICLE 2',
        'VEHICLE TYPE CODE 3', 
        'CONTRIBUTING FACTOR VEHICLE 3',
        'VEHICLE TYPE CODE 4',
        'CONTRIBUTING FACTOR VEHICLE 4',
        'VEHICLE TYPE CODE 5',
        'CONTRIBUTING FACTOR VEHICLE 5'
    ]

    # Include year/date columns if they exist
    year_cols = [col for col in dataframe.columns if any(term in col for term in ['YEAR','DATE','TIME'])]
    search_columns.extend(year_cols)

    # Filter columns that actually exist
    available_columns = [col for col in search_columns if col in dataframe.columns]

    if not available_columns:
        print("❌ No searchable columns found!")
        return dataframe

    # Convert all searchable columns to string safely
    for col in available_columns:
        dataframe[col] = dataframe[col].astype(str).fillna('')

    # Initialize final mask
    if logic.upper() == "AND":
        final_mask = pd.Series(True, index=dataframe.index)
    else:
        final_mask = pd.Series(False, index=dataframe.index)

    # Apply search terms
    for term in search_terms:
        term_mask = pd.Series(False, index=dataframe.index)
        for col in available_columns:
            # Safe string contains
            term_mask |= dataframe[col].str.lower().str.contains(term, na=False)
        if logic.upper() == "AND":
            final_mask &= term_mask
        else:
            final_mask |= term_mask

    filtered_df = dataframe[final_mask]
    return filtered_df





# --- Callbacks for filtering ---
@app.callback([
    Output('Borough-dropdown', 'value'),
    Output('Demographic-dropdown', 'value'),
    Output('Factor-dropdown', 'value'),
    Output('year-slider', 'value'),
    Output('search-input', 'value')

    ],

    [
    Input('btn-reset', 'n_clicks')
    ]
)

#Reseting values to filtering the whole datSet
def reset_filters(n):
     return None, None  , None, 2023 , ""

#Callback to update dashboard
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
        State('Factor-dropdown', 'value'),
        State('year-slider', 'value'),
        State('search-input', 'value')
    ]
)
def update_dashboard(n, bor, demo, fac, year_slider, search_text):

    # Mapping the dataframe based on the filters
    inputs = {'borough': bor, 'factor1': fac  ,'year': year_slider, 'demographic': demo}
    
    #Apply all filters
    dff = filter_dataframe(df, inputs)

    #Apllying the searhc function filter     
    dff = apply_search_filter(dff, search_text)
     
    # Getting stats
    s1, s2, s3, s4 = get_stats(dff)

    # Charts with template
    return s1, s2, s3, s4, \
           create_bar(dff), create_pie(dff), \
           create_line(dff), create_heatmap(dff), create_map(dff)

# --- Download Callback ---
@app.callback(
    Output("download-report", "data"),
    Input("Download-button", "n_clicks"),
    [
        State('Borough-dropdown', 'value'),
        State('Factor-dropdown', 'value'),
        State('Demographic-dropdown', 'value'),
        State('year-slider', 'value'),
        State('search-input', 'value')
    ],
    prevent_initial_call=True
)

def download_csv(n_clicks, bor, fac,  demo, year, search_text):

    # Filter dataframe
    inputs = {'borough': bor, 'factor1': fac,  'demographic': demo, 'year': year}

    dff = filter_dataframe(df, inputs)
    dff = apply_search_filter(dff, search_text)

    # Apply search filter
    if search_text:
        search_text_lower = search_text.lower()
        search_cols = ['BOROUGH', 'VEHICLE TYPE CODE 1', 'CONTRIBUTING FACTOR VEHICLE 1' , "MOST_COMMON_SEX", "CRASH_YEAR"]
        dff = dff[dff[search_cols].apply(lambda row: row.astype(str).str.lower().str.contains(search_text_lower).any(), axis=1)]

    # Return CSV
    return dcc.send_data_frame(dff.to_csv, "nyc_traffic_crashes.csv", index=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)