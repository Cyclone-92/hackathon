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

# Get storage charge

def get_storage_charge():
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/measurements/storage'
    response = requests.get(url).json()
    return response['charge'][-1]['value']

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

def stream_consumption_data():
    response = requests.get(f'https://hackathon.kvanttori.fi/buildings/{id}/streams/consumption', stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
  
# Post allocations

def set_production_allocations(consumption, grid, storage):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/allocations/production_allocation'
    data = {"to_consumption": consumption,
            "to_grid": grid,
            "to_storage": storage}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Request was successful.")
    else:
        print(f"Request failed with status code {response.status_code}.")
        
def set_grid_allocations(value):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/allocations/grid_allocation'
    data = {"to_storage": value}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Request was successful.")
    else:
        print(f"Request failed with status code {response.status_code}.")
        
def set_storage_allocations(cons, grid):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/allocations/storage_allocation'
    data = {"to_consumption": cons,
            "to_grid": grid}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Request was successful.")
    else:
        print(f"Request failed with status code {response.status_code}.")
        
    

#stream_consumption_data('https://hackathon.kvanttori.fi/buildings/6cd466d8-9802-413c-b173-65b81d62ceee/streams/consumption')

# You can print a stream of time-weather-consumption like this
""" while True:
    get_time_weather_consumption()
    t.sleep(2) """
get_storage_charge()