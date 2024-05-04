import requests

id = '6cd466d8-9802-413c-b173-65b81d62ceee'

def stream_consumption_data(url):
    response = requests.get(url, stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            
# TODO change the URL to use the id variable
stream_consumption_data('https://hackathon.kvanttori.fi/buildings/6cd466d8-9802-413c-b173-65b81d62ceee/streams/consumption')