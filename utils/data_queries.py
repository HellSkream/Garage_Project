import os

from numpy.f2py.crackfortran import endifs
from supabase import create_client
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import calendar

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

def fetch_data_by_date(startdate, enddate):
    # Supabase config
    url = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
    key = os.getenv("GP_SUPABASE_API_KEY")
    supabase = create_client(url, key)
    all_rows = []
    batch_size = 1000
    offset = 0

    while True:
        response = (
            supabase
            .table("temperature_data")
            .select("*")
            .gte("Log Time", startdate.isoformat())
            .lt("Log Time", enddate.isoformat())
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

if __name__ == "__main__":
    mymonth = 11
    myyear = 2024

    startdate = datetime(myyear, mymonth, 1)
    endmonth = startdate + relativedelta(months=2)
    lastday = calendar.monthrange(endmonth.year, endmonth.month)[1]
    enddate = datetime(endmonth.year, endmonth.month, lastday, 23, 59, 59)
    df = fetch_data_by_date(startdate, enddate)
    
