import dash
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import dcc, html, Input, Output
from supabase import create_client
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from Garage_Project.components.header import get_header

load_dotenv()

# Fetch all data from Supabase
def fetch_data(days):
    # Supabase config
    url = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
    key = os.getenv("GP_SUPABASE_API_KEY")
    supabase = create_client(url, key)
    # Calculate cutoff datetime in UTC
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
    all_rows = []
    batch_size = 1000
    offset = 0

    while True:
        response = (
            supabase
            .table("temperature_data")
            .select("*")
            .gte("Log Time", cutoff_time.isoformat())
            .range(offset, offset + batch_size - 1)
            .execute()
        )

        rows = response.data
        if not rows:
            break

        all_rows.extend(rows)
        offset += batch_size

    df = pd.DataFrame(all_rows)
    df["Log Time"] = pd.to_datetime(df["Log Time"], utc=True)
    return df


def create_gauge(title, value, min_val=0, max_val=100, unit="°C"):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [min_val, max_val],
                        'tickmode': 'linear',  # Default is linear
                        'tick0': 0,  # Starting tick
                        'dtick': 10  # Step size (e.g., ticks every 10°C)
                        }},
        number={'suffix': f" {unit}"},
        domain={'x': [0, 1], 'y': [0, 1]}
    )).update_layout(
    margin=dict(t=30, b=30, l=30, r=30),
    height=250  # increase height for better visibility
)


# Dash app_gauges.py setup
app = dash.Dash(__name__)
app.title = "Temperature Dashboard"

# Layout
app.layout = html.Div([
    get_header(),
    # Title
    html.Div(
        children=[html.H1("Temperature Data Dashboard")],
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
@app.callback(
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


if __name__ == '__main__':
    render_port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=render_port, debug=False)
