from dash import html, dcc, register_page
from components.header import get_header  # Import the header component

register_page(__name__, path="/")

layout = html.Div([
    get_header("Home"),

    html.Div([
        html.P("""
            The Garage Project is a personal initiative to build an interactive weather dashboard.
            It collects and visualizes local temperature data, leveraging Raspberry Pi, Supabase, and Dash.
            The project is designed to explore data visualization, user experience, and efficient deployment.
        """),

        html.P("""
            Why did I build this? Simply put—curiosity. I wanted to create a structured,
            modular system that could elegantly display weather trends in an interactive format.
        """),
        html.Ul([
            html.H3("Project Links"),

            html.Li([
                html.Img(src="/assets/rasp-pi-logo.png", className="link-logo"),
                html.A("Data collected on a Raspberry Pi", href="hhttps://www.raspberrypi.com/", target="_blank")
            ], className="link-item"),

            html.Li([
                html.Img(src="/assets/render-logo.png", className="link-logo"),
                html.A("Hosted on Render - Weather Dashboard", href="https://render.com/", target="_blank")
            ], className="link-item"),

            html.Li([
                html.Img(src="/assets/github-logo.png", className="link-logo"),
                html.A("GitHub Repository", href="hhttps://github.com/HellSkream/Garage_Project", target="_blank")
            ], className="link-item"),

            html.Li([
                html.Img(src="/assets/supabase-logo.png", className="link-logo"),
                html.A("Supabase Database", href="https://supabase.com/", target="_blank")
            ], className="link-item"),
        ], className="link-list")
    ], className="home-content")
])



