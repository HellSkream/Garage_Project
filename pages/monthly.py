from dash import html, dcc, register_page
from components.header import get_header  # Import the header component

register_page(__name__, path="/monthly")

layout = html.Div([
    get_header(),
    # Title
    html.Div(
        children=[html.H1("Monthly Weather/Temperature Dashboard")],
        className='title-container'
    ),
    html.P("Under Construction")
    ])


