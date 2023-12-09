import heapq
from datetime import datetime
import time
import threading
import scheduler

from central_ac import CentralAc

centralAC = CentralAc()
# room_test = Room(1, 'INIT', centralAC.service, threading.Lock())
#
# room_test.initial_env_temp = 28
# room_test.current_temp = room_test.initial_env_temp
# room_test.target_speed = 'HIGH'
# room_test.current_speed = room_test.target_speed
# room_test.target_temp = 25
#
# room_test.start()
# time.sleep(9)
# room_test.stop()
# print(room_test.fee)
# room_test.join()

# room_threads = ["thread1", "thread2", "thread3", "thread4", "thread5"]
# ready_to_delete = [1, 3]
#
# # Sort indices in reverse order
# ready_to_delete.sort(reverse=True)
#
# # Remove elements from room_threads
# for index in ready_to_delete:
#     del room_threads[index]
#
# # room_threads now has the elements removed
# print(room_threads)
# room1 = Room(1, 1, centralAC.service, threading.Lock())
# room2 = Room(2, 1, centralAC.service, threading.Lock())
# room3 = Room(3, 1, centralAC.service, threading.Lock())
#
# room_thread = [room1, room2, room3]
# print(room_thread)
scheduler = scheduler.Scheduler(centralAC)
centralAC.fee_rate = 2.0
print(scheduler.central_ac.fee_rate)
