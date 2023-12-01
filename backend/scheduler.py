from room1 import Room
from queues import Queues
from central_ac import CentralAc


class Scheduler:
    def __init__(self, central_ac: CentralAc):
        self.central_ac = central_ac
        self.queues = Queues()
        self.room_threads = []
        self.priority = {'HIGH': 1, 'MID': 2, 'LOW': 3}

        self.max_be_served = 3

    def add_room(self, room_ids: list, initial_env_temp: list):
        for idx, id in enumerate(room_ids):
            room = Room(id, 'INIT', initial_env_temp[idx], self.central_ac.service)
            self.room_threads.append(room)

    def deal_with_on_and_off(self, room_id, target_temp, target_speed, ac_state):
        if target_temp is None:
            target_temp = self.central_ac.default_temp
        if target_speed is None:
            target_speed = self.central_ac.default_speed

        room_priority = self.priority[target_speed]

        if ac_state == 'ON':
            for room in self.room_threads:
                if room.room_id == room_id:
                    room.target_temp = target_temp
                    room.target_speed = target_speed
                    self.queues.add_into_ready_queue(room, room_priority)
        else:
            for room in self.room_threads:
                if room.room_id == room_id:
                    room.stop()
                    room.state = 'FINISH'
                    self.queues.pop_service_by_room_id(room_id)

    def schedule(self):
        while 1:
            ready_be_served = self.queues.get_from_ready_queue()
            ready_served_priority = self.priority[ready_be_served.current_speed]
            if ready_be_served is None:
                # ready_queue is empty
                continue
            elif len(self.queues.running_queue) < self.max_be_served:
                # running_queue has vacancies
                self.queues.pop_ready_queue()
                self.queues.add_into_running_queue(ready_be_served)

                ready_be_served.power = True
                ready_be_served.current_speed = ready_be_served.target_speed
                ready_be_served.run()
            else:
                # running_queue is full
                room_with_lowest_priority = self.queues.get_running_room_with_lowest_priority()
                room_priority = self.priority[room_with_lowest_priority.current_speed]

                if ready_served_priority < room_priority:
                    # priority scheduling
                    room_with_lowest_priority.stop()
                    self.queues.pop_service_by_room_id(room_with_lowest_priority.room_id)
                    self.queues.add_into_suspend_queue(room_with_lowest_priority)
