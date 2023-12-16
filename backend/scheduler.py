import threading
from datetime import datetime
import copy

from room import Room
from queues import Queues
from central_ac import CentralAc
from database import add_to_order
from utils import recover_temp


class Scheduler:
    def __init__(self, central_ac: CentralAc):
        self.central_ac = central_ac
        self.queues = Queues()
        self.room_threads = {}
        self.priority = {'HIGH': 1, 'MID': 2, 'LOW': 3}

        self.max_be_served = 3
        self.RR_SLOT = 40

        self.state_lock = {}
        # self.read_lock = {}
        self.write_lock = threading.Lock()
        self.recover_lock = threading.Lock()
        self.access_room_lock = threading.Lock()

    def add_room(self, room_ids: list):
        self.access_room_lock.acquire()
        for room_id in room_ids:
            self.state_lock[room_id] = threading.Lock()
            # self.read_lock[room_id] = threading.Lock()
            room = Room(room_id, 'INIT', self.central_ac.service, 
                        self.state_lock[room_id], self.write_lock)
            self.room_threads[room_id] = room

            add_to_order(room_id)
        self.access_room_lock.release()

    def delete_room(self, room_ids: list):
        self.access_room_lock.acquire()
        for room_id in room_ids:
            self.room_threads.pop(room_id)
            self.queues.pop_off_queue(room_id)
        self.access_room_lock.release()

    def get_available_room(self):
        available_room_ids = []
        for room_id in self.room_threads.keys():
            available_room_ids.append(room_id)
        return available_room_ids
    
    def get_room_message(self, room_id): 
        # self.read_lock[room_id].acquire()
        room_message = {
            'room': self.room_threads[room_id].room_id,
            'temperature': self.room_threads[room_id].current_temp,
            'wind_speed': self.room_threads[room_id].current_speed,
            'mode': 'cold',
            'is_on': self.room_threads[room_id].power,
            'is_ruzu': True
        }
        # self.recover_lock.release()
        # self.read_lock[room_id].release()
        return room_message

    def set_room_initial_env_temp(self, room_ids: list, initial_env_temp: list):
        for index, room_id in enumerate(room_ids):
            self.room_threads[room_id].initial_env_temp = initial_env_temp[index]
            self.room_threads[room_id].current_temp = self.room_threads[room_id].initial_env_temp

    def deal_with_on_and_off(self, room_id: str, target_temp: int, target_speed: str, ac_state: str):
        if target_temp is None:
            target_temp = self.central_ac.default_temp
        if target_speed is None:
            target_speed = self.central_ac.default_speed

        room_priority = self.priority[target_speed]

        if ac_state == 'ON':
            self.room_threads[room_id].current_speed = target_speed
            self.room_threads[room_id].target_temp = target_temp
            self.room_threads[room_id].target_speed = target_speed
            self.queues.pop_off_queue(room_id)
            self.queues.add_into_ready_queue(room_id, room_priority)
            return 'on'
        else:
            if self.queues.remove_from_suspend_queue(room_id):
                self.room_threads[room_id].state = False
                self.queues.add_into_off_queue(room_id)
                return 'off_remove_from_suspend'
            elif self.queues.remove_from_ready_queue(room_id):
                self.room_threads[room_id].state = False
                self.queues.add_into_off_queue(room_id)
                return 'off_remove_from_ready'
            else:
                self.room_threads[room_id].stop()
                self.room_threads[room_id].state = 'FINISH'
                self.room_threads[room_id].power = False
                self.queues.pop_service_by_room_id(room_id)
                self.queues.add_into_off_queue(room_id)
                return 'off_remove_from_running'

    def deal_with_speed_temp_change(self, room_id, target_temp, target_speed):
        if target_temp is None and target_speed is not None:
            self.state_lock[room_id].acquire()
            self.room_threads[room_id].target_speed = target_speed
            self.room_threads[room_id].current_speed = target_speed
            self.room_threads[room_id].change_flag = 1
            self.state_lock[room_id].release()
        elif target_temp is not None and target_speed is None:
            self.state_lock[room_id].acquire()
            self.room_threads[room_id].target_temp = target_temp
            self.room_threads[room_id].change_flag = 1
            self.state_lock[room_id].release()
        else:
            self.state_lock[room_id].acquire()
            self.room_threads[room_id].target_temp = target_temp
            self.room_threads[room_id].target_speed = target_speed
            self.room_threads[room_id].current_speed = target_speed
            self.room_threads[room_id].change_flag = 1
            self.state_lock[room_id].release()

    def schedule(self):
        while 1:
            # recover temp
            self.access_room_lock.acquire()
            read_to_recover_in_off = self.queues.get_all_rooms_from_off_queue()
            self.access_room_lock.release()

            ready_to_recover_in_ready = self.queues.get_all_rooms_from_ready_queue()
            ready_to_recover_in_suspend = self.queues.get_all_rooms_from_suspend_queue()
            if read_to_recover_in_off:
                for room_id in read_to_recover_in_off:
                    recover_temp(self.room_threads[room_id])
                    # print(self.room_threads['test'].current_temp)
            if ready_to_recover_in_ready:
                for room_id in ready_to_recover_in_ready:
                    recover_temp(self.room_threads[room_id])
            if ready_to_recover_in_suspend:
                for room_id in ready_to_recover_in_suspend:
                    recover_temp(self.room_threads[room_id])

            # if room's current_temp <= target_temp, pop running_queue and add into suspend_queue
            self.access_room_lock.acquire()
            for room in self.room_threads.values():
                if room.target_temp == 0:
                    continue
                if room.current_temp == room.target_temp:
                    self.queues.pop_service_by_room_id(room.room_id)
                    self.queues.add_into_suspend_queue(room)
                # elif room.current_temp < room.target_temp:
                #     room.stop()
                #     room.state = 'SUSPEND'
                #     room.power = False
                #     self.queues.pop_service_by_room_id(room.room_id)
                #     self.queues.add_into_suspend_queue(room)
            self.access_room_lock.release()

            # pop suspend_queue and add into ready_queue
            ready_to_pop_suspend = self.queues.pop_suspend_queue()
            if ready_to_pop_suspend is None:
                pass
            else:
                for room in ready_to_pop_suspend:
                    priority = self.priority[room.current_speed]
                    self.queues.add_into_ready_queue(room.room_id, priority)

            ready_running_room_id, start_waiting_time = self.queues.get_from_ready_queue()

            if ready_running_room_id is not None:
                # print(ready_running_room_id)
                ready_running_priority = self.priority[
                    self.room_threads[ready_running_room_id].current_speed
                ]

            if ready_running_room_id is None:
                # ready_queue is empty
                continue
            elif len(self.queues.running_queue) < self.max_be_served:
                # running_queue has vacancies
                self.queues.pop_ready_queue()
                self.queues.add_into_running_queue(ready_running_room_id)

                self.room_threads[ready_running_room_id].state = 'RUNNING'
                self.room_threads[ready_running_room_id].power = True
                self.room_threads[ready_running_room_id].current_speed = \
                    self.room_threads[ready_running_room_id].target_speed
                if self.room_threads[ready_running_room_id].is_start_first == 1:
                    self.room_threads[ready_running_room_id].is_start_first = 0
                    self.room_threads[ready_running_room_id].start()
                else:
                    self.room_threads[ready_running_room_id].resume()
            else:
                # running_queue is full
                # start scheduling
                room_with_lowest_priority = self.queues.get_running_room_with_lowest_priority(
                    self.room_threads
                )
                # print('priority lowest:', room_with_lowest_priority)

                room_priority = self.priority[
                    self.room_threads[room_with_lowest_priority].current_speed
                ]

                if ready_running_priority < room_priority:
                    # priority scheduling
                    self.room_threads[room_with_lowest_priority].stop()
                    self.room_threads[room_with_lowest_priority].state = 'SUSPEND'
                    self.room_threads[room_with_lowest_priority].power = True
                    self.queues.pop_service_by_room_id(room_with_lowest_priority)
                    self.queues.add_into_suspend_queue(
                        self.room_threads[room_with_lowest_priority]
                    )

                    self.queues.pop_ready_queue()
                    self.queues.add_into_running_queue(ready_running_room_id)
                    self.room_threads[ready_running_room_id].state = 'RUNNING'
                    self.room_threads[ready_running_room_id].power = True
                    self.room_threads[ready_running_room_id].current_speed = \
                        self.room_threads[ready_running_room_id].target_speed
                    if self.room_threads[ready_running_room_id].is_start_first == 1:
                        self.room_threads[ready_running_room_id].is_start_first = 0
                        self.room_threads[ready_running_room_id].start()
                    else:
                        self.room_threads[ready_running_room_id].resume()
                else:
                    # RR scheduling
                    time_now = datetime.now()
                    if (time_now - start_waiting_time).total_seconds() >= self.RR_SLOT:
                        self.room_threads[room_with_lowest_priority].stop()
                        self.room_threads[room_with_lowest_priority].state = 'SUSPEND'
                        self.room_threads[room_with_lowest_priority].power = True
                        self.queues.pop_service_by_room_id(room_with_lowest_priority)
                        self.queues.add_into_suspend_queue(
                            self.room_threads[room_with_lowest_priority]
                        )

                        self.queues.pop_ready_queue()
                        self.queues.add_into_running_queue(ready_running_room_id)
                        self.room_threads[ready_running_room_id].state = 'RUNNING'
                        self.room_threads[ready_running_room_id].power = True
                        self.room_threads[ready_running_room_id].current_speed = \
                            self.room_threads[ready_running_room_id].target_speed
                        if self.room_threads[ready_running_room_id].is_start_first == 1:
                            self.room_threads[ready_running_room_id].is_start_first = 0
                            self.room_threads[ready_running_room_id].start()
                        else:
                            self.room_threads[ready_running_room_id].resume()
