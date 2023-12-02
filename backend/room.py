import threading
from datetime import datetime


class Room(threading.Thread):
    def __init__(self, room_id, state, initial_env_temp, target, state_lock: threading.Lock, **kwargs):
        super().__init__(**kwargs)
        self.power = False
        self.room_id = room_id
        self.state = state
        self.initial_env_temp = initial_env_temp
        self.current_temp = initial_env_temp
        self.current_speed = None
        self.target_temp = None
        self.target_speed = None
        self.start_time = None
        self.end_time = None
        self.current_fee = 0
        self.last_fee = 0
        self.fee = 0

        self.running = True
        self.target = target
        self.running_lock = threading.Lock()
        self.state_lock = state_lock

    def run(self):
        self.start_time = datetime.now()
        while self.running:
            self.running_lock.acquire()
            self.state_lock.acquire()

            self.current_temp, self.current_fee = self.target(
                self.current_temp,
                self.target_temp,
                self.target_speed,
                self.current_fee
            )
            if self.current_temp == self.target_temp:
                self.running = False

            self.state_lock.release()
            self.running_lock.release()

    def stop(self):
        self.running = False
        self.running_lock.acquire()

        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        print(duration)

        self.fee += self.current_fee
        self.last_fee = self.current_fee
        self.current_fee = 0

        self.running_lock.release()
