import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import calendar
from utils.data_queries import fetch_data_by_date
import matplotlib.pyplot as plt
import io
import base64

def create_gauge(title, value, min_val=0, max_val=100, unit="°C"):
    mygauge = go.Figure(go.Indicator(
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
    return mygauge

def create_daily_line(df, days):
    fig = px.line(
        df,
        x="Log Time",
        y=["Garage Temp", "Perth Temp"],
        labels={"value": "Temperature (°C)", "Log Time": "Time"},
        title=f"Temperature (Last {days} Day{'s' if days > 1 else ''})"
    )
    fig.update_layout(legend_title_text="Series", xaxis_title="Time", yaxis_title="Temperature (°C)")
    return fig

def create_3month_mean(df, startdate):
    df = df.resample('10min', on='Log Time', label='right').agg(agg_rules)
    df.reset_index(inplace=True)
    df['DN'] = df['Log Time'].apply(lambda x: DayNight(x))
    df['Date'] = df['Log Time'].dt.date
    df['Month'] = df['Log Time'].dt.month
    df['Month_Name'] = df['Log Time'].dt.month_name()
    df['Year'] = df['Log Time'].dt.year
    df['Time'] = df['Log Time'].dt.time
    df['StrTime'] = df['Log Time'].dt.strftime('%H:%M')
    df['Insulated'] = df['Date'].apply(lambda x: Code_Insulate(x))
    df['Ins_Colour'] = df['Insulated'].apply(lambda x: coldict[x])
    df.set_index(['Date', 'Time'], inplace=True)

    month1 = (startdate.strftime('%B'), startdate.strftime('%Y') )
    month2 = ((startdate + relativedelta(months=1)).strftime('%B'), (startdate + relativedelta(months=1)).strftime('%Y'))
    month3 = ((startdate + relativedelta(months=2)).strftime('%B'), (startdate + relativedelta(months=2)).strftime('%Y'))

    fig, ax = plt.subplots(2, 3, figsize=(20, 12))
    for xi, x in enumerate([month1,month2,month3]):
        filter = (df.DN == 'Day') & (df.Month_Name == x[0]) & (df.Year == int(x[1]))
        pdf = df[filter][['Garage Temp', 'Perth Temp', 'CPU Temp', 'Ins_Colour']].unstack()
        pdf.sort_index(level=0, axis=1, inplace=True)
        pdf.dropna(inplace=True)

        for d in pdf.index:
            pdf.loc[d]['Garage Temp'].plot(alpha=0.2, color=pdf.loc[d]['Ins_Colour'], ax=ax[0, xi])
            pdf.loc[d]['Perth Temp'].plot(alpha=0.2, color='red', ax=ax[1, xi])
        pdf['Garage Temp'].mean().plot(color='gray', label='Garage Temp', ax=ax[0, xi])
        pdf['Perth Temp'].mean().plot(color='red', label='Perth Temp', ax=ax[1, xi])
        for i in [0, 1]:
            ax[i, xi].set_ylim(10, 45)
            for j in pd.date_range('06:00', '18:00', freq='3h').time:
                ax[i, xi].axvline(j, alpha=0.5)
        ax[0, xi].set_title(f'Daytime Garage Temps - {x[0]}-{x[1]}')
        ax[1, xi].set_title(f'Daytime Perth Temps - {x[0]}-{x[1]}')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    encodedimg = base64.b64encode(buf.read()).decode("utf-8")
    return encodedimg

def DayNight(xtime):
    x = int(xtime.ceil('6h').strftime('%H'))
    if x == 12 or x == 18:
        return 'Day'
    else:
        return 'Night'


def Code_Insulate(logdate):
    if logdate > pd.Timestamp('2023-11-22').date():
        return 'Yes'
    else:
        return 'No'


coldict = {'Yes': 'blue',
           'No': 'gray'}

agg_rules = {'Garage Temp': 'mean',
             'Perth Temp': 'mean',
             'CPU Temp': 'mean',
             'Weather Desc': 'first'}

if __name__ == "__main__":
    mymonth = 11
    myyear = 2024

    startdate = datetime(myyear, mymonth, 1)
    endmonth = startdate + relativedelta(months=2)
    lastday = calendar.monthrange(endmonth.year, endmonth.month)[1]
    enddate = datetime(endmonth.year, endmonth.month, lastday, 23, 59, 59)
    df = fetch_data_by_date(startdate, enddate)
    fig = create_3month_mean(df, startdate)
    fig.show()

