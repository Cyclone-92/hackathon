import requests

id = "88cf343b-4080-4d30-8de9-dfa905d6eb9b"

def stream_consumption_data(building_id):
    url = f'https://hackathon.kvanttori.fi/buildings/{building_id}/streams/consumption'
    response = requests.get(url, stream=True)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            
# Call the function with the id variable
stream_consumption_data(id)
