import requests
import json

id = '6cd466d8-9802-413c-b173-65b81d62ceee'

# System time

def getSystemTime():
    response = requests.get('https://hackathon.kvanttori.fi/system')
    time = response.json()['time']
    print(time)
    return time

# Streams

def getSystemTimeStream():
    while True:
        
        response = requests.get('https://hackathon.kvanttori.fi/system/stream', stream=True)
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                line_as_json = json.loads(decoded_line)
                print(line_as_json['time'])

def stream_consumption_data(url):
    response = requests.get(url, stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            
# TODO change the URL to use the id variable
#stream_consumption_data('https://hackathon.kvanttori.fi/buildings/6cd466d8-9802-413c-b173-65b81d62ceee/streams/consumption')


getSystemTimeStream()