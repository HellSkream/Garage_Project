from dash import html, dcc, register_page
from components.header import get_header  # Import the header component

register_page(__name__, path="/monthly")

layout = html.Div([
    get_header("Monthly Weather/Temperature Dashboard"),
    html.P("Under Construction")
    ])


