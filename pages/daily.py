import plotly.express as px
from dash import dcc, html, Input, Output, register_page, callback
from datetime import timedelta
from components.header import get_header  # Import the header component
from utils.data_queries import fetch_data
from utils.plot_functions import create_gauge

register_page(__name__, path="/daily")

layout = html.Div([
    get_header(),
    # Title
    html.Div(
        children=[html.H1("Daily Weather/Temperature Dashboard")],
        className='title-container'
    ),

    # Dropdown
    html.Div(
        children=[
            dcc.Dropdown(
                id='days-dropdown',
                options=[
                    {'label': f'{i} Days', 'value': i} for i in [1,2,3,5,7,10,15,20]
                ],
                value=7,
                className='days-dropdown'
            ),
        ],
        className='dropdown-container'
    ),
    # Gauges
    dcc.Loading(
        id="loading1",
        type="circle",
        children=[
        html.Div(
            children=[
            dcc.Graph(id='cpu-gauge', className='gauge'),
            dcc.Graph(id='garage-gauge', className='gauge'),
            html.Div(
                className="gauge",
                children=[
                    dcc.Graph(id='perth-gauge', config={"displayModeBar": False}),
                    html.Div(id='weather-description', className="weather-description")
                ]
            ),
        ],
            className='gauge-container'
        )]),

    # Daily graph
    dcc.Loading(
        id="loading2",
        type="circle",
        children=[
        html.Div(
            children=[
                dcc.Graph(
                    id='temp-graph',
                    className='graph'
                ),
            ],
            className='graph-container'
        )]),

])


# Callback to update graph
@callback(
    Output('temp-graph', 'figure'),
    Output('cpu-gauge', 'figure'),
    Output('garage-gauge', 'figure'),
    Output('perth-gauge', 'figure'),
    Output('weather-description', 'children'),
    Input('days-dropdown', 'value')
)
def update_dashboard(days):
    df = fetch_data(days)
    latest_time = df["Log Time"].max()
    cutoff_time = latest_time - timedelta(days=days)
    df = df[df["Log Time"] >= cutoff_time]

    # Line chart
    fig = px.line(
        df,
        x="Log Time",
        y=["Garage Temp", "Perth Temp"],
        labels={"value": "Temperature (°C)", "Log Time": "Time"},
        title=f"Temperature (Last {days} Day{'s' if days > 1 else ''})"
    )
    fig.update_layout(legend_title_text="Series", xaxis_title="Time", yaxis_title="Temperature (°C)")

    # Latest values for gauges
    latest = df.sort_values("Log Time").iloc[-1]
    cpu_temp = latest.get("CPU Temp", 0)
    garage_temp = latest.get("Garage Temp", 0)
    perth_temp = latest.get("Perth Temp", 0)
    weath_text = latest.get("Weather Desc", "No description")
    perth_weather_desc = f"The current weather in Perth:\n{weath_text}"

    cpu_gauge = create_gauge("CPU Temp", cpu_temp, min_val=20, max_val=80)
    garage_gauge = create_gauge("Garage Temp", garage_temp, min_val=0, max_val=50)
    perth_gauge = create_gauge("Perth Temp", perth_temp, min_val=0, max_val=50)

    return fig, cpu_gauge, garage_gauge, perth_gauge, perth_weather_desc
