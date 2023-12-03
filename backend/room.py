import threading
from datetime import datetime
from database import add_to_detail


class Room(threading.Thread):
    def __init__(self, room_id, state, target, state_lock: threading.Lock, **kwargs):
        super().__init__(**kwargs)
        self.power = False
        self.room_id = room_id
        self.state = state
        self.initial_env_temp = None
        self.current_temp = None
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
                self.end_time = datetime.now()
                self.power = False
                self.state = 'FINISH'

                self.write_into_db(self.end_time)

            self.state_lock.release()
            self.running_lock.release()

    def stop(self):
        self.running = False
        self.running_lock.acquire()

        self.end_time = datetime.now()
        self.write_into_db(self.end_time)

        self.running_lock.release()

    def write_into_db(self, end_time):
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
            duration
        )
