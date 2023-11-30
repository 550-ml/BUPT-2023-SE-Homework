import datetime


class Room:
    def __init__(self, room_id, initial_env_temp) -> None:
        self.power = False
        self.room_id = room_id
        self.initial_env_temp = initial_env_temp
        self.current_temp = initial_env_temp
        self.current_speed = None
        self.target_temp = None
        self.target_speed = None
        self.start_time = None
        self.last_fee = 0
        self.fee = 0
    
    # power on
    def power_on(self):
        self.power = True
        return True

    # power off
    def power_off(self):
        self.power = False
        return True
    
    def set_target_temp(self, target_temp):
        self.target_temp = target_temp

    def set_target_speed(self, target_speed):
        self.target_speed = target_speed

    def get_target_speed(self):
        return self.target_speed

    def get_state(self):
        ret = {'fee': self.fee, 'currTemp': self.current_temp, 'targetTemp': self.target_temp,
               'acState': 'on' if self.power is True else 'off'}
        if ret['acState'] != 'off':
            ret['speed'] = self.current_speed.lower()
        return ret

    def start_service(self):
        self.start_time = datetime.datetime.now()

    def get_rdr_fee(self):
        ans = self.fee - self.last_fee
        self.last_fee = self.fee
        return ans
