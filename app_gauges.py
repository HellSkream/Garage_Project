import dash
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import dcc, html, Input, Output
from supabase import create_client
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

# Supabase config
url = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
key = os.getenv("GP_SUPABASE_API_KEY")
supabase = create_client(url, key)

# Fetch all data from Supabase
def fetch_data(days):
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
        gauge={'axis': {'range': [min_val, max_val]}},
        number={'suffix': f" {unit}"}
    ))

# Dash app setup
app = dash.Dash(__name__)
app.title = "Temperature Dashboard"

# Layout
app.layout = html.Div([
    html.Div(
        children=[html.H1("Temperature Data Dashboard")],
        className='title-container'
    ),

    html.Div(
        children=[
            dcc.Dropdown(
                id='days-dropdown',
                options=[{'label': f'{i} Days', 'value': i} for i in range(1, 8)],
                value=7,
                className='dcc-dropdown'
            ),
        ],
        className='dropdown-container'
    ),

    html.Div(id='gauge-row', className='gauge-row'),

    html.Div(
        children=[
            dcc.Graph(id='temp-graph', className='graph-container'),
        ],
        className='graph-container'
    ),
])

# Callback to update graph and gauges
@app.callback(
    [Output('temp-graph', 'figure'),
     Output('gauge-row', 'children')],
    [Input('days-dropdown', 'value')]
)
def update_graph(days):
    df = fetch_data(days)
    latest_time = df["Log Time"].max()
    cutoff_time = latest_time - timedelta(days=days)
    df = df[df["Log Time"] >= cutoff_time]

    latest = df.sort_values("Log Time").iloc[-1]
    cpu_temp = latest.get("CPU Temp", 0)
    garage_temp = latest.get("Garage Temp", 0)
    perth_temp = latest.get("Perth Temp", 0)
    weather_desc = latest.get("Weather Description", "N/A")

    fig = px.line(
        df,
        x="Log Time",
        y=["Garage Temp", "Perth Temp"],
        labels={"value": "Temperature (°C)", "Log Time": "Time"},
        title=f"Temperature (Last {days} Day{'s' if days > 1 else ''})"
    )
    fig.update_layout(legend_title_text="Series", xaxis_title="Time", yaxis_title="Temperature (°C)")

    gauges = [
        html.Div([
            dcc.Graph(figure=create_gauge("CPU Temp", cpu_temp), className="gauge"),
            html.P(f"Weather: {weather_desc}", className="gauge-label")
        ]),
        html.Div([
            dcc.Graph(figure=create_gauge("Garage Temp", garage_temp), className="gauge"),
            html.P("Garage Weather", className="gauge-label")
        ]),
        html.Div([
            dcc.Graph(figure=create_gauge("Perth Temp", perth_temp), className="gauge"),
            html.P("Perth Weather", className="gauge-label")
        ])
    ]

    return fig, gauges

if __name__ == '__main__':
    render_port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=render_port, debug=False)
