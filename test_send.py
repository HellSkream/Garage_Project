import requests
import json
from dotenv import load_dotenv
#from datetime import datetime

load_dotenv()

# Supabase settings
SUPABASE_URL = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
SUPABASE_API_KEY = os.getenv("GP_SUPABASE_API_KEY")
TABLE_NAME = "test1"  # or whatever your table is called

# Sample record to insert
data = {
    "garage_temp": 26.5,
    "cpu_temp": 60.0,
    "description": "test send 2"
}

# Headers
headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# URL to your table via REST
url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"

# POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Output result
print("Status Code:", response.status_code)
print("Response Text:", response.text)
