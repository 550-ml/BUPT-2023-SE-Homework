import heapq
from datetime import datetime
import time
import threading

from room import Room
from central_ac import CentralAc

centralAC = CentralAc()
room_test = Room(1, 'INIT', centralAC.service, threading.Lock())

room_test.initial_env_temp = 28
room_test.current_temp = room_test.initial_env_temp
room_test.target_speed = 'HIGH'
room_test.current_speed = room_test.target_speed
room_test.target_temp = 25

room_test.start()
time.sleep(9)
room_test.stop()
print(room_test.fee)
room_test.join()
