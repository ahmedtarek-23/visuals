import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# IMPORTANT: Assuming data_filters.py and chart_generation.py are in a 'utils' directory
from data_filters import get_filter_options, filter_data
from chart_generation import create_borough_crash_bar_chart

# --- 1. DATA LOADING (Run once at startup) ---
try:
    # Load the single source of truth: the final cleaned and merged data
    DATA_PATH = 'merged_crashes_person.csv'
    df_global = pd.read_csv(DATA_PATH)
    print(f"✅ Data loaded successfully from {DATA_PATH}. Shape: {df_global.shape}")
except FileNotFoundError:
    print(f"❌ Error: {DATA_PATH} not found. Please ensure your integrated CSV is in the root directory.")
    df_global = pd.DataFrame() # Use empty DF as fallback

# Generate dynamic filter options from the loaded data
FILTER_OPTIONS = get_filter_options(df_global)

# Map the frontend names (used in the HTML layout) to the backend column names
FILTER_MAP = {
    'borough': 'BOROUGH',
    'year': 'CRASH_YEAR',
    'factor': 'CONTRIBUTING FACTOR VEHICLE 1',
    'vehicleType': 'VEHICLE TYPE CODE 1'
}


# --- 2. INITIALIZE DASH APP ---
app = dash.Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])
server = app.server # Required for deployment platforms like Heroku


# --- 3. DASHBOARD LAYOUT (UI) ---

# Helper function to create filter dropdowns
def create_dropdown(label, name, options):
    """Creates a standardized Dash Core Component Dropdown."""
    return html.Div(className="flex flex-col space-y-1", children=[
        html.Label(label, className="text-xs font-medium text-gray-500"),
        dcc.Dropdown(
            id=f'{name}-dropdown',
            options=[{'label': i, 'value': i} for i in options],
            value=options[0], # Set default to the first option (usually 'ALL')
            clearable=False,
            className="text-sm border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 hover:border-blue-300"
        )
    ])

app.layout = html.Div(className="min-h-screen bg-gray-100 p-4 sm:p-8 font-sans", children=[
    
    # Header
    html.Header(className="mb-6", children=[
        html.H1("NYC Collision Insights Dashboard (Dash)", className="text-3xl font-extrabold text-gray-800"),
        html.P("Interactive exploration of integrated crash and person data.", className="text-gray-500 mt-1"),
    ]),

    # --- FILTER CONTROLS AREA ---
    html.Div(className="bg-white p-6 rounded-xl shadow-2xl border border-gray-200", children=[
        html.H2("Data Filters & Search Mode", className="text-xl font-bold text-gray-700 mb-4"),
        
        # Dropdown Filters Grid
        html.Div(className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6", children=[
            create_dropdown("1. Borough", "borough", FILTER_OPTIONS.get('BOROUGH', ['ALL'])),
            create_dropdown("2. Crash Year", "year", FILTER_OPTIONS.get('CRASH_YEAR', ['ALL'])),
            create_dropdown("3. Contributing Factor", "factor", FILTER_OPTIONS.get('CONTRIBUTING FACTOR VEHICLE 1', ['ALL'])),
            create_dropdown("4. Vehicle Type", "vehicleType", FILTER_OPTIONS.get('VEHICLE TYPE CODE 1', ['ALL'])),
        ]),

        # Search Mode and Generate Button
        html.Div(className="flex flex-col md:flex-row gap-4 pt-4 border-t border-gray-100", children=[
            
            # Search Input (Search Mode)
            html.Div(className="relative flex-1", children=[
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder="Search mode: e.g., 'Queens 2023 pedestrian accident'",
                    className="w-full pl-4 pr-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm"
                )
            ]),

            # Generate Report Button (CRITICAL REQUIREMENT)
            html.Button(
                'Generate Report',
                id='generate-button',
                n_clicks=0,
                className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition duration-150 transform active:scale-95"
            ),
        ]),
    ]),
    
    # --- VISUALIZATION REPORT AREA ---
    html.Main(className="mt-8", children=[
        html.Div(id='loading-output', className="text-center py-4", children=[
            html.P("Apply filters and click 'Generate Report' to view insights.", className="text-gray-500")
        ]),
        
        # Chart 1 Container
        html.Div(className="p-6 bg-white border border-gray-200 rounded-xl shadow-lg mb-6", children=[
            html.H4("Total Crashes by Borough", className="text-lg font-semibold mb-3"),
            dcc.Graph(id='borough-crash-chart', config={'displayModeBar': False})
        ]),
        
        # Chart 2 Container (Placeholder for another required chart)
        html.Div(className="p-6 bg-white border border-gray-200 rounded-xl shadow-lg", children=[
            html.H4("Injuries by Vehicle Type (Placeholder)", className="text-lg font-semibold mb-3"),
            dcc.Graph(id='injury-vehicle-chart', config={'displayModeBar': False})
        ]),
    ])
])


# --- 4. CALLBACKS (CONNECTING UI TO DATA LOGIC) ---

@app.callback(
    [
        Output('borough-crash-chart', 'figure'),
        Output('injury-vehicle-chart', 'figure'),
        Output('loading-output', 'children')
    ],
    [Input('generate-button', 'n_clicks')],
    [
        State('borough-dropdown', 'value'),
        State('year-dropdown', 'value'),
        State('factor-dropdown', 'value'),
        State('vehicleType-dropdown', 'value'),
        State('search-input', 'value'),
    ]
)
def update_report(n_clicks, borough, year, factor, vehicleType, search_term):
    # Only run the report generation when the button is clicked (n_clicks > 0)
    if n_clicks is None or n_clicks == 0:
        # Initial state: Return empty/placeholder figures
        return (
            px.bar(title=""), 
            px.bar(title=""), 
            "Apply filters and click 'Generate Report' to view insights."
        )

    # Display loading message (or spinner) while processing
    loading_message = html.Div("Generating Report... This may take a moment.", className="text-blue-500 font-semibold")

    # 1. Collect all filter states
    current_filters = {
        'borough': borough,
        'year': year,
        'factor': factor,
        'vehicleType': vehicleType,
    }
    
    # 2. Filter the global dataset using the utility function
    df_filtered = filter_data(df_global, current_filters, search_term or '')
    
    # 3. Generate Charts using the utility function
    fig1 = create_borough_crash_bar_chart(df_filtered)
    
    # Placeholder for a second required chart
    if df_filtered.empty:
         fig2 = px.bar(title="No Data for Injuries by Vehicle Type")
    else:
        # Example: Injuries by Vehicle Type (You need to implement this function in chart_generation.py)
        injury_counts = df_filtered.groupby('VEHICLE TYPE CODE 1')['NUMBER OF PERSONS INJURED'].sum().reset_index()
        fig2 = px.bar(
            injury_counts.head(10), # Show top 10 for performance/clarity
            x='VEHICLE TYPE CODE 1',
            y='NUMBER OF PERSONS INJURED',
            title='Top 10 Injuries by Vehicle Type',
            template='plotly_white'
        )
        
    # Return figures and a success message
    return fig1, fig2, html.P(f"Report Generated successfully for {df_filtered.shape[0]} records.", className="text-green-600 font-semibold")


if __name__ == '__main__':
    app.run_server(debug=True)