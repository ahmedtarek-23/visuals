from dash import html, dcc
import dash_bootstrap_components as dbc

def create_dropdown(id, options, placeholder):
    return dcc.Dropdown(
        id=id,
        options=[{'label': opt, 'value': opt} for opt in options],
        placeholder=placeholder,
        multi=False,
        style={'width': '100%'}
    )

def create_search_bar(id):
    return dbc.Input(
        id=id,
        type='text',
        placeholder='Search...',
        style={'width': '100%'}
    )
