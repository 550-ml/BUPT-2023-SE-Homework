import heapq
from datetime import datetime
import time
import threading

from room import Room
from central_ac import CentralAc

centralAC = CentralAc()
room_test = Room(1, 'INIT', 28, centralAC.service, threading.Lock())

room_test.target_speed = 'HIGH'
room_test.current_speed = room_test.target_speed
room_test.target_temp = 25

room_test.start()
time.sleep(9)
room_test.stop()
print(room_test.fee)
room_test.join()
