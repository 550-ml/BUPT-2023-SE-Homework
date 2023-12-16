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

    def set_params(self, mode, fee_rate, temp_section, default_temp, default_speed):
        self.mode = mode
        self.fee_rate = fee_rate
        self.temp_section = temp_section
        self.default_temp = default_temp
        self.default_speed = default_speed

    def service(self, on_temp, target_temp, target_speed, start_time, cold_or_heat):
        duration = (datetime.now() - start_time).total_seconds()
        current_temp = self.update_temperature(on_temp, target_temp, target_speed, duration, cold_or_heat)
        total_cost = self.update_cost(target_speed, duration)

        return current_temp, total_cost

    def update_temperature(self, on_temp, target_temp, target_speed, duration, cold_or_heat):
        current_temp = on_temp + cold_or_heat * self.temperature_change_rate[target_speed] / 30 * duration

        if cold_or_heat == -1 and current_temp <= target_temp:
            return target_temp
        elif cold_or_heat == 1 and current_temp >= target_temp:
            return target_temp
        else:
            return current_temp

    def update_cost(self, target_speed, duration):
        total_cost = self.fee_rate * self.power_rate[target_speed] / 30 * duration
        return total_cost
