from PySide6.QtCore import QThread, Signal
import requests
import json

class LogicThread(QThread):

    data_update = Signal(float, float, float)  # Signal to indicate image update
    message_updated = Signal(str)

    def emit_data_opt(self, consumption, grid, storage):
        self.data_update.emit(consumption, grid, storage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_url = "https://hackathon.kvanttori.fi"
        self.id = ""

    def get_consumption(self):
        url = f'{self.base_url}/buildings/{self.id}/measurements'
        response = requests.get(url).json()
        print(response)
        return response['consumer']['consumption'][-1]['value']

    def get_production(self):
        url = f'{self.base_url}/buildings/{self.id}/measurements'
        response = requests.get(url).json()
        sum_of_production = response['producer']['to_consumption'][-1]['value'] + \
                            response['producer']['to_grid'][-1]['value'] + \
                            response['producer']['to_storage'][-1]['value']
        return sum_of_production

    def calculate_proportion_of_production_needed_for_consumption(self):
        consumption = self.get_consumption()
        production = self.get_production()
        proportion = round(consumption / production, 2)
        return proportion

    def set_production_allocations(self, consumption, grid, storage):
        url = f'{self.base_url}/buildings/{self.id}/allocations/production_allocation'
        data = {"to_consumption": consumption,
                "to_grid": grid,
                "to_storage": storage}

        response = requests.post(url, json=data)

        if response.status_code == 200:
            # print("Request was successful.")
            # print(f"production allocations were adjusted to: consumption {consumption}, grid: {grid}, storage: {storage}")
            # print(data)
            self.emit_data_opt(consumption, grid, storage)
            return data
        else:
            print(f"Request failed with status code {response.status_code}.")

    def get_storage_charge(self):
        url = f'{self.base_url}/buildings/{self.id}/measurements/storage'
        response = requests.get(url).json()
        return response['charge'][-1]['value']

    def adjust_energy_allocations(self):
        proportion = self.calculate_proportion_of_production_needed_for_consumption()
        storage_charge = self.get_storage_charge()
        # print(f"Proportion of consumption/production: {proportion}")
        # print(f"Storage charge: {storage_charge}")
        if proportion <= 1:
            # consumption is lower than production
            if storage_charge < 250:
                # there is space in storage
                # use all production needed for consumption and send the rest to the storage
                self.set_production_allocations(proportion, 0, 1 - proportion)
            elif storage_charge == 250:
                # storage is full
                # use all production for consumption and send rest to grid because storage is full
                self.set_production_allocations(proportion, 1 - proportion, 0)
        else:
            # production is lower than consumption
            self.set_production_allocations(1, 0, 0)

    def run(self):
        while True:
            self.adjust_energy_allocations()


