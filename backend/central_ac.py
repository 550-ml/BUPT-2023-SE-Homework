import time
from datetime import datetime


class CentralAc:
    def __init__(self):
        self.mode = 'cold'
        self.fee_rate = 1.0
        self.temp_section = [18, 28]
        self.default_temp = 25
        self.default_speed = 'MID'
        self.power_rate = {'HIGH': 1, 'MID': 0.5, 'LOW': 1/3}  # Electricity consumption rate
        self.temperature_change_rate = {'HIGH': 1, 'MID': 0.5, 'LOW': 0.25}  # Temperature change rate

    def service(self, current_temp, target_temp, target_speed, total_cost):
        time.sleep(10)
        current_temp = self.update_temperature(current_temp, target_temp, target_speed)
        total_cost = self.update_cost(total_cost, target_speed)

        return current_temp, total_cost

    def update_temperature(self, current_temp, target_temp, target_speed):
        temp = current_temp - self.temperature_change_rate[target_speed]
        if temp >= target_temp:
            current_temp = temp
        return current_temp

    def update_cost(self, total_cost, target_speed):
        total_cost += self.fee_rate * self.power_rate[target_speed]
        return total_cost
