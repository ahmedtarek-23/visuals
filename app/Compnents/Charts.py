import plotly.express as px
import dash_core_components as dcc

def create_bar_chart(df, x_col, y_col, title="Bar Chart"):
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    return dcc.Graph(figure=fig)

def create_line_chart(df, x_col, y_col, title="Line Chart"):
    fig = px.line(df, x=x_col, y=y_col, title=title)
    return dcc.Graph(figure=fig)

def create_heatmap(df, x_col, y_col, z_col, title="Heatmap"):
    fig = px.density_heatmap(df, x=x_col, y=y_col, z=z_col, title=title)
    return dcc.Graph(figure=fig)