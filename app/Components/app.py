import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import filters
import charts

# Initialize
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df = filters.load_data()

# --- Components Helper ---
def make_dropdown(label, id, col):
    return dbc.Col([
        dbc.Label(label, className="fw-bold"),
        dcc.Dropdown(id=id, options=filters.get_options(df, col), placeholder="All")
    ], md=4, className="mb-3")

# --- Layout ---
app.layout = dbc.Container([
    dbc.NavbarSimple(brand="NYC Traffic Crashes Dashboard", color="dark", dark=True, className="mb-4"),
    
    # Filters Section (7 Filters as requested)
    dbc.Card([
        dbc.CardHeader("Data Filters"),
        dbc.CardBody([
            dbc.Row([
                make_dropdown("Borough", "f-borough", "BOROUGH"),
                make_dropdown("Year", "f-year", "CRASH_YEAR"),
                make_dropdown("Demographic", "f-demo", "MOST_COMMON_SEX"),
            ]),
            dbc.Row([
                make_dropdown("Factor 1", "f-fac1", "CONTRIBUTING FACTOR VEHICLE 1"),
                make_dropdown("Factor 2", "f-fac2", "CONTRIBUTING FACTOR VEHICLE 2"),
                make_dropdown("Vehicle 1", "f-veh1", "VEHICLE TYPE CODE 1"),
            ]),
            dbc.Row([
                dbc.Col(make_dropdown("Vehicle 2", "f-veh2", "VEHICLE TYPE CODE 2"), md=8),
                dbc.Col([
                    html.Br(),
                    dbc.Button("Generate Report", id="btn-gen", color="success", className="me-2"),
                    dbc.Button("Reset", id="btn-reset", color="secondary")
                ], md=4, className="d-flex align-items-center")
            ])
        ])
    ], className="mb-4"),

    # Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="s-crash"), html.P("Total Crashes")])], color="primary", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="s-inj"), html.P("Total Injuries")])], color="warning", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="s-fat"), html.P("Total Fatalities")])], color="danger", inverse=True)),
        dbc.Col(dbc.Card([dbc.CardBody([html.H3(id="s-avg"), html.P("Avg Persons Involved")])], color="info", inverse=True)),
    ], className="mb-4"),

    # Charts Grid
    dbc.Row([
        dbc.Col(dcc.Graph(id="c-bar"), md=6),
        dbc.Col(dcc.Graph(id="c-pie"), md=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="c-line"), md=6),
        dbc.Col(dcc.Graph(id="c-heat"), md=6),
    ], className="mb-4"),
    
    dbc.Row(dbc.Col(dcc.Graph(id="c-map"), md=12))

], fluid=True)

# --- Callbacks ---
@app.callback(
    [Output('f-borough', 'value'), Output('f-year', 'value'), Output('f-demo', 'value'),
     Output('f-fac1', 'value'), Output('f-fac2', 'value'), Output('f-veh1', 'value'), Output('f-veh2', 'value')],
    [Input('btn-reset', 'n_clicks')]
)
def reset_filters(n):
    return [None] * 7

@app.callback(
    [Output('s-crash', 'children'), Output('s-inj', 'children'), Output('s-fat', 'children'), Output('s-avg', 'children'),
     Output('c-bar', 'figure'), Output('c-pie', 'figure'), Output('c-line', 'figure'), Output('c-heat', 'figure'), Output('c-map', 'figure')],
    [Input('btn-gen', 'n_clicks')],
    [State('f-borough', 'value'), State('f-year', 'value'), State('f-demo', 'value'),
     State('f-fac1', 'value'), State('f-fac2', 'value'), State('f-veh1', 'value'), State('f-veh2', 'value')]
)
def update(n, bor, year, demo, fac1, fac2, veh1, veh2):
    # Gather inputs into a dict
    inputs = {'borough': bor, 'year': year, 'demographic': demo, 
              'factor1': fac1, 'factor2': fac2, 'vehicle1': veh1, 'vehicle2': veh2}
    
    # Filter
    dff = filters.filter_dataframe(df, inputs)
    
    # Stats
    s1, s2, s3, s4 = charts.get_stats(dff)
    
    # Charts
    return s1, s2, s3, s4, \
           charts.create_bar(dff), charts.create_pie(dff), \
           charts.create_line(dff), charts.create_heatmap(dff), charts.create_map(dff)

if __name__ == '__main__':
    app.run(debug=True, port=8050)