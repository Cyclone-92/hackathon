import requests
import json

base_url = 'https://hackathon.kvanttori.fi'
id = 'a918af6e-b5ff-4b18-8961-fdccfd76eea3'


def get_consumption():
    url = f'{base_url}/buildings/{id}/measurements'
    response = requests.get(url).json()
    return response['consumer']['consumption'][-1]['value']


def get_production():
    url = f'{base_url}/buildings/{id}/measurements'
    response = requests.get(url).json()
    sum_of_production = response['producer']['to_consumption'][-1]['value'] + response['producer']['to_grid'][-1][
        'value'] + response['producer']['to_storage'][-1]['value']
    return sum_of_production


# print(get_consumption())
# print(get_production())

def calculate_propotion_of_production_needed_for_consumption():
    consumption = get_consumption()
    production = get_production()
    proportion = round(consumption / production, 2)
    return proportion


#print(calculate_propotion_of_production_needed_for_consumption())


def set_production_allocations(consumption, grid, storage):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/allocations/production_allocation'
    data = {"to_consumption": consumption,
            "to_grid": grid,
            "to_storage": storage}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Request was successful.")
        print(f"production allocations were adjusted to: consumption {consumption}, grid: {grid}, storage: {storage}")
        return data
    else:
        print(f"Request failed with status code {response.status_code}.")


def get_storage_charge():
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/measurements/storage'
    response = requests.get(url).json()
    return response['charge'][-1]['value']


def set_storage_allocations(cons, grid):
    url = f'https://hackathon.kvanttori.fi/buildings/{id}/allocations/storage_allocation'
    data = {"to_consumption": cons,
            "to_grid": grid}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Request was successful.")
    else:
        print(f"Request failed with status code {response.status_code}.")

def adjust_energy_allocations():
    proportion = calculate_propotion_of_production_needed_for_consumption()
    storage_charge = get_storage_charge()
    print(f"Proportion of consumption/production: {proportion}")
    print(f"Storage charge: {storage_charge}")
    if proportion <= 1:
        # consumption is lower than production
        # no need to feed from storage, so set it to 0,0
        set_storage_allocations(0,0)
        if storage_charge < 250:
            # there is space in storage
            # use all production needed for consumption and send the rest to the storage
            set_production_allocations(proportion, 0, 1 - proportion)
        elif storage_charge == 250:
            # storage is full
            # use all production for consumption and send rest to grid because storage is full
            set_production_allocations(proportion, 1 - proportion, 0)
    else:
        # production is lower than consumption
        # use all of production for consumption
        set_production_allocations(1,0,0)
        # feed all of the storage to the consumption
        set_storage_allocations(1,0)

