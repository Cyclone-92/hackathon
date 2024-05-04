import requests
import json
from datetime import datetime, timedelta
import time as t

id = '6cd466d8-9802-413c-b173-65b81d62ceee'

# System time

def get_system_time():
    response = requests.get('https://hackathon.kvanttori.fi/system')
    time = response.json()['time']
    print(time)
    return time

# Consumption

def get_consumption(start, end):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/measurements/consumption'
    parameters = {'start': start, 'end': end}
    response = requests.get(url, params=parameters, timeout=30)
    return response

# Streams

def get_system_time_stream():
    response = requests.get('https://hackathon.kvanttori.fi/system/stream', stream=True)
        
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            line_as_json = json.loads(decoded_line)
            print(line_as_json['time'])
            
def get_time_weather_consumption():
    response = requests.get('https://hackathon.kvanttori.fi/system')
    time = response.json()['time']
    start = time
    
    # Parse the time string into a datetime object
    date_time_end = datetime.fromisoformat(time)

    # Add the specified number of minutes
    date_time_end += timedelta(minutes=5)

    # Convert the datetime object back into a string
    end = date_time_end.isoformat()
    t.sleep(10)
    consumption = get_consumption(start, end)
    weather = response.json()['weather']
    value = consumption.json()['consumption'][0]
    print(time, weather, value)

def stream_consumption_data(url):
    response = requests.get(url, stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            
# TODO change the URL to use the id variable
#stream_consumption_data('https://hackathon.kvanttori.fi/buildings/6cd466d8-9802-413c-b173-65b81d62ceee/streams/consumption')
while True:
    get_time_weather_consumption()
    t.sleep(2)