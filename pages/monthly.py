from dash import html, dcc, register_page, callback, Input, Output, State
from components.header import get_header  # Import the header component
from utils.plot_functions import create_3month_mean
from utils.data_queries import fetch_data_by_date
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import calendar
import plotly.express as px

register_page(__name__, path="/monthly")

layout = html.Div([
    get_header("Monthly Weather/Temperature Dashboard"),
    html.Div([
        dcc.Dropdown(
            id="month-dropdown",
            options=[{"label": month, "value": month} for month in [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]],
            value="January",  # Default selection
            placeholder="Select Month",
            className='monthly-dropdown-month'
        ),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": str(year), "value": str(year)} for year in range(2023, 2026)],
            value="2025",  # Default selection
            placeholder="Select Year",
            className='monthly-dropdown-year'
        ),
        html.Button("Go", id="submit-button", n_clicks=0)  # Added 'Go' button
    ], className="dropdown-container"),

    # Monthly graph
    dcc.Loading(
        id="loading2",
        type="circle",
        children=[
        html.Div(
            children=[
                html.Img(
                    id='monthly-graph',
                    className='graph-month'
                ),
            ],
            className='graph-container'
        )]),
    ])

@callback(
    Output("monthly-graph", "src"),
    Input("submit-button", "n_clicks"),  # Only triggers when button is clicked
    State("month-dropdown", "value"),  # Get selected month
    State("year-dropdown", "value")  # Get selected year
)
def update_monthly_graph(n_clicks, selected_month, selected_year):
    if n_clicks == 0:  # Avoid triggering on app load
        return ""  # Placeholder

    mymonth = datetime.strptime(selected_month, "%B").month
    startdate = datetime(int(selected_year), mymonth, 1)
    endmonth = startdate + relativedelta(months=2)
    lastday = calendar.monthrange(endmonth.year, endmonth.month)[1]
    enddate = datetime(endmonth.year, endmonth.month, lastday, 23, 59, 59)
    df = fetch_data_by_date(startdate, enddate)
    img_base64 = create_3month_mean(df, startdate)
    return f"data:image/png;base64,{img_base64}"
