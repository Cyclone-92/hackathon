import requests
from optimization import set_id

def setup(value):
    url = 'https://hackathon.kvanttori.fi/buildings/create'
    data = {'team_name': value}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Request was successful.")
        print(response.text)
        id = response.json()['id']
        set_id(id)
        
    else:
        print(f"Request failed with status code {response.status_code}.")