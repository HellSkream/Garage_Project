from dash import html, dcc

def get_header():
    return html.Div([
        html.Div("The Garage Project", className="header"),
        html.Div([
            dcc.Link("Home", href="/", className="nav-links"),
            dcc.Link("Daily Data", href="/daily", className="nav-links"),
            dcc.Link("Monthly Data", href="/monthly", className="nav-links"),
        ], className="nav-links")
    ])
