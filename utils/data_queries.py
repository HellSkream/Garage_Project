import os
from supabase import create_client
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

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
