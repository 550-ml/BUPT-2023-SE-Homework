import threading


class Room(threading.Thread):
    def __init__(self, room_id, state, initial_env_temp, target, **kwargs):
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
        self.last_fee = 0
        self.fee = 0

        self.running = True
        self.target = target

    def run(self):
        while self.running:
            self.current_temp, self.fee = self.target(
                self.current_temp,
                self.target_temp,
                self.target_speed,
                self.fee
            )
            if self.current_temp == self.target_temp:
                self.running = False

    def stop(self):
        self.running = False
