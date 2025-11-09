from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Load the data
df = pd.read_csv('../data/cleaned_integrated_crashes_persons.csv')

# App layout
app.layout = html.Div([
    html.H1('NYC Traffic Crashes Dashboard'),
    
    # Add your visualization components here
    
])

if __name__ == '__main__':
    app.run_server(debug=True)