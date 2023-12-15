import threading
from datetime import datetime
import copy

from database import add_to_detail


class Room(threading.Thread):
    def __init__(self, room_id, state, target, 
                 state_lock: threading.Lock, write_lock: threading.Lock,
                 **kwargs):
        super().__init__(**kwargs)
        self.power = False
        self.room_id = room_id
        self.state = state
        # need to change
        self.initial_env_temp = 25
        self.current_temp = 25
        self.current_speed = None
        self.target_temp = None
        self.target_speed = None
        self.start_time = None
        self.end_time = None
        self.current_fee = 0
        self.last_fee = 0
        self.fee = 0

        self.last_off_temp = 0
        self.on_temp = self.initial_env_temp

        self.running = True
        self.target = target
        self.running_lock = threading.Lock()
        self.state_lock = state_lock
        self.write_lock = write_lock
        self.change_flag = 0

    # def __deepcopy__(self, memo):
    #     new_room = Room(self.room_id, self.state, self.target,
    #                     self.state_lock, self.write_lock)
    #
    #     new_room.current_temp = copy.deepcopy(self.current_temp, memo)
    #     new_room.current_speed = copy.deepcopy(self.current_speed, memo)
    #     new_room.target_temp = copy.deepcopy(self.target_temp, memo)
    #     new_room.target_speed = copy.deepcopy(self.target_speed, memo)
    #     new_room.start_time = copy.deepcopy(self.start_time, memo)
    #     new_room.end_time = copy.deepcopy(self.end_time, memo)
    #
    #     new_room.power = self.power
    #     new_room.room_id = self.room_id
    #     new_room.state = self.state
    #     new_room.initial_env_temp = self.initial_env_temp
    #     new_room.current_fee = self.current_fee
    #     new_room.last_fee = self.last_fee
    #     new_room.fee = self.fee
    #     new_room.running = self.running
    #     new_room.target = self.target
    #     new_room.running_lock = self.running_lock
    #     new_room.change_flag = self.change_flag
    #     new_room.state_lock = self.state_lock
    #     new_room.write_lock = self.write_lock
    #
    #     return new_room

    def run(self):
        self.start_time = datetime.now()
        self.on_temp = self.current_temp
        while self.running:
            self.running_lock.acquire()
            self.state_lock.acquire()

            self.is_changed()

            self.current_temp, self.current_fee = self.target(
                self.on_temp,
                self.target_temp,
                self.target_speed,
                self.start_time
            )
            if self.current_temp == self.target_temp:
                self.running = False
                self.end_time = datetime.now()
                self.power = False
                self.state = 'FINISH'
                self.last_off_temp = self.current_temp

                self.write_into_db(self.end_time)

            self.state_lock.release()
            self.running_lock.release()

    def stop(self):
        self.running = False
        self.running_lock.acquire()

        self.end_time = datetime.now()
        self.last_off_temp = self.current_temp
        self.write_into_db(self.end_time)

        self.running_lock.release()

    def is_changed(self):
        if self.change_flag:
            self.end_time = datetime.now()
            self.write_into_db(self.end_time)
            self.start_time = datetime.now()
            self.change_flag = 0

    def write_into_db(self, end_time):
        self.write_lock.acquire()
        duration = (end_time - self.start_time).total_seconds()

        self.fee += self.current_fee
        self.last_fee = self.current_fee
        self.current_fee = 0

        add_to_detail(
            self.room_id,
            self.start_time,
            self.end_time,
            self.current_speed,
            self.fee,
            duration,
            self.target_temp
        )
        self.write_lock.release()
