"""
Title: Room Management for Central Air Conditioning System
Module Description:
    This module provides the functionality for managing individual rooms in a central air conditioning system.
    It includes features for controlling and monitoring the temperature, state, \
    and other environmental parameters of each room.
    The module is designed to be part of a larger system that oversees the air conditioning needs of \
    multiple rooms or zones, offering individualized control and monitoring.

Main Algorithms:
    - Room state management: Controls and monitors power state, target temperature, and current temperature of the room.
    - Thread-based operation: Each room instance operates as a separate thread for concurrent management.
    - Integration with central system: Communicates with a central database and \
        air conditioning system for coordinated control.

Interface Description:
    - __init__(room_id, state, target, state_lock, write_lock, **kwargs): Initializes a room with specific parameters
        including room ID, state, and target temperature. Utilizes threading locks for concurrent operations.
    - run(): Starts the room's thread, primarily called by the scheduler for operation initiation.
    - stop(): Stops the room's thread, used by the scheduler to cease room operation.
    - resume(): Resumes the room's thread, allowing the scheduler to restart room operation after a pause.

Development Record:
    Creator: Lisheng Gong
    Creation Date: 2023/12/01
    Modifier: Lisheng Gong
    Modification Date: 2023/12/17
    Modification Content:
        - add preamble notes
    Version: 3.0.0
"""


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
        self.initial_env_temp = 30
        self.current_temp = self.initial_env_temp
        self.current_speed = ''
        self.target_temp = 0
        self.target_speed = ''

        self.start_time = 0
        self.end_time = 0

        self.current_fee = 0
        self.last_fee = 0
        self.fee = 0

        self.last_off_temp = 0  # temperature when off, used to recover temperature
        self.on_temp = self.initial_env_temp  # temperature when on, used to adjust temperature

        self.running = True  # control running and stop
        self.target = target  # target function

        self.running_condition = threading.Condition()
        self.running_lock = threading.Lock()
        self.state_lock = state_lock  # the lock of state change
        self.write_lock = write_lock  # the lock of writing into database
        self.change_flag = 0  # when state changes, set to 1. write into database

        self.is_start_first = 1
        self.be_running = 1

        self.route = ''  # debug, record the process of generating detailed orders

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
        while True:
            if self.running:
                self.running_lock.acquire()
                self.state_lock.acquire()

                if self.be_running:
                    self.start_time = datetime.now()
                    self.on_temp = self.current_temp
                    self.be_running = 0

                self.is_changed()

                self.current_temp, self.current_fee = self.target(
                    self.on_temp,
                    self.target_temp,
                    self.target_speed,
                    self.start_time,
                    -1 if self.current_temp > self.target_temp else 1
                )

                # current_temp = target_temp, stop
                if self.current_temp == self.target_temp:
                    self.running = False
                    self.power = True
                    self.state = 'FINISH'
                    self.end_time = datetime.now()
                    self.last_off_temp = self.current_temp
                    self.route = 'current_temp=target_temp'
                    self.write_into_db(self.end_time, self.route)

                self.state_lock.release()
                self.running_lock.release()
            else:
                with self.running_condition:
                    self.running_condition.wait()

    def stop(self):
        self.running = False
        self.running_lock.acquire()

        self.end_time = datetime.now()
        self.last_off_temp = self.current_temp
        self.write_into_db(self.end_time, self.route)
        self.running_lock.release()

    def resume(self):
        with self.running_condition:
            self.running = True
            self.be_running = 1
            self.running_condition.notify()

    def is_changed(self):
        if self.change_flag:
            self.end_time = datetime.now()
            self.route = 'state change'
            self.write_into_db(self.end_time, self.route)
            # self.current_speed = self.target_speed
            self.start_time = datetime.now()
            self.on_temp = self.current_temp
            self.change_flag = 0

    def write_into_db(self, end_time, route):
        self.write_lock.acquire()
        duration = (end_time - self.start_time).total_seconds()
        if duration < 0.01:
            pass
        else:
            self.fee += self.current_fee
            self.last_fee = self.current_fee
            self.current_fee = 0

            add_to_detail(
                self.room_id,
                self.start_time,
                self.end_time,
                self.current_speed,
                self.last_fee,
                duration,
                self.target_temp,
                route
            )
        self.write_lock.release()
