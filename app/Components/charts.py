import plotly.express as px
import plotly.graph_objects as go

def bar_chart(df, x_col, y_col, title):
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    return fig

def line_chart(df, x_col, y_col, title):
    fig = px.line(df, x=x_col, y=y_col, title=title)
    return fig

def heatmap(df, x_col, y_col, z_col, title):
    fig = go.Figure(data=go.Heatmap(
        x=df[x_col],
        y=df[y_col],
        z=df[z_col],
        colorscale='Viridis'
    ))
    fig.update_layout(title=title)
    return fig

def pie_chart(df, names_col, values_col, title):
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    return fig

def map_chart(df):
    # Assuming df has LATITUDE and LONGITUDE
    fig = px.scatter_mapbox(df, lat='LATITUDE', lon='LONGITUDE', 
                            hover_name='BOROUGH', zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(title="Collision Map")
    return fig