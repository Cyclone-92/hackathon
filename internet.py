import requests
import json

# Define the URL to which you want to send the POST request
url = 'https://hackathon.kvanttori.fi'

uuID = "88cf343b-4080-4d30-8de9-dfa905d6eb9b"


user_type = input("if its Get type 1 if its post type 2 : ")

if 

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers to indicate that the data is in JSON format
headers = {'Content-Type': 'application/json'}

# Send the POST request with JSON data and headers
response = requests.post(url, data=json_data, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("POST request was successful!")
    print("Returned message:", response.text)
else:
    print("POST request failed with status code:", response.status_code)
