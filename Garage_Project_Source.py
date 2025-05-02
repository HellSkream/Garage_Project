import os
import glob
import time
import requests
import json
from datetime import datetime
from gpiozero import CPUTemperature
from dotenv import load_dotenv

def read_temp_raw():
    with  open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def Get_Sensor_Temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def myNow():
    return datetime.now().strftime('%H:%M:%S %d-%b-%Y')


def dbTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def Get_Weath():
    api_key = "432dacf8f1e2875179ffefaeb14dc246"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=perth,au"  # 2063523
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        mytime = datetime.fromtimestamp(x['dt'])
        # print(f' Temperature (in degrees Celsius) = {current_temperature - 273.15:.1f}')
        # print(f' Atmospheric pressure (in hPa unit) = {str(current_pressure)}')
        # print(f' Humidity (in percentage) = {str(current_humidity)}')
        # print(f' Description = {str(weather_description)}')
        # print(f' Temp recoded at: {mytime}')
        return current_temperature - 273.15, weather_description, mytime.strftime('%H:%M:%S %d-%b-%Y'), mytime.strftime(
            '%Y-%m-%d %H:%M:%S')
    else:
        return None, None, None


def Send_Data(data):
    SUPABASE_URL = "https://arqnxrnhenqqgwnwtgjc.supabase.co"
    SUPABASE_API_KEY = os.getenv("GP_SUPABASE_API_KEY")
    TABLE_NAME = "temp_data_duplicate"  # or whatever your table is called

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
    requests.post(url, headers=headers, data=json.dumps(data))

def Write_Data(cputemp, roomtemp, weather, log):
    myline = (f'{myNow()},{cputemp},{roomtemp},{weather[0]},{weather[1]},{weather[2]}\n')
    with open(log, 'a') as txt:
        txt.write(myline)
    print('sent: ' + myline)


def main():
    load_dotenv()
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    logpath = '/home/hellskream01/Documents'
    logfile = 'mylogfile_temp.csv'
    log = os.path.join(logpath, logfile)
    myCPUtemp = CPUTemperature().temperature
    myRoomTemp = Get_Sensor_Temp(device_file)
    myWeath = Get_Weath()
    Write_Data(myCPUtemp, myRoomTemp, myWeath, log)
    Send_Data({"Log Time": dbTime(),
               "CPU Temp": myCPUtemp,
               "Garage Temp": myRoomTemp,
               "Perth Temp": myWeath[0],
               "Weather Desc": myWeath[1],
               "Weath Time": myWeath[3]})

if __name__ == "__main__":
    main()