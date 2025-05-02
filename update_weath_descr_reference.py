import requests
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client
#from datetime import datetime

load_dotenv()

weath_codes = {'light intensity shower rain': 'Rain',
               'light rain': 'Rain',
               'overcast clouds':'Cloudy',
               'clear sky':'Clear',
               'few clouds':'Clear',
               'scattered clouds':'Clear',
               'broken clouds':'Clear',
               'drizzle': 'Rain',
               'mist':'Cloudy',
               'fog':'Cloudy',
               'light intensity drizzle':'Cloudy',
               'shower rain':'Rain',
               'heavy intensity shower rain':'Rain',
               'moderate rain':'Rain',
               'heavy intensity drizzle':'Rain',
               'haze':'Clear',
               'smoke':'Clear',
               'thunderstorm with light rain':'Rain',
               'thunderstorm with rain':'Rain',
               'heavy intensity rain':'Rain',
               'thunderstorm with heavy rain':'Rain',
               'thunderstorm':'Rain',
               'dust':'Clear',
               'light thunderstorm':'Rain',
               'very heavy rain':'Rain',
               'extreme rain':'Rain',
              }

# Supabase settings
SUPABASE_URL = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
SUPABASE_API_KEY = os.getenv("GP_SUPABASE_API_KEY")
TABLE_NAME = "weath_desc"  # or whatever your table is called

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

for index, record in enumerate(weath_codes.keys()):
    response = supabase.table(TABLE_NAME).insert(
        {"id":index,
         "description": record,
         "weath_type": weath_codes[record]}
    ).execute()
    # Output result
    # print("Status Code:", response.status_code)
    print("Response Text:", response)
