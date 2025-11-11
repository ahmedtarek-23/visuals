import dash_core_components as dcc
import dash_html_components as html

def create_dropdown(id, options, placeholder="Select an option"):
    return dcc.Dropdown(
        id=id,
        options=[{"label": opt, "value": opt} for opt in options],
        placeholder=placeholder,
        multi=False,
        style={"width": "250px"}
    )

def create_search_bar(id, placeholder="Search..."):
    return dcc.Input(
        id=id,
        type="text",
        placeholder=placeholder,
        style={"width": "300px", "margin": "10px"}
    )