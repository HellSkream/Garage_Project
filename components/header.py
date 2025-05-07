from dash import html, dcc

def get_header(pagetitle):
    return html.Div([
        html.Div("The Garage Project", className="header"),
        html.Div(f"{pagetitle}", className="page-title"),
        html.Nav([
            dcc.Link("Home", href="/", className="nav-links"),
            dcc.Link("Daily Data", href="/daily", className="nav-links"),
            dcc.Link("Monthly Data", href="/monthly", className="nav-links"),
        ], className="nav-container"),
    ], className="header-container")
