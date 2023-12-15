# import heapq
# import time
# import threading
# from scheduler import Scheduler

# from central_ac import CentralAc

# centralAC = CentralAc()
# scheduler = Scheduler(centralAC)

# scheduler.schedule

a = [1, 2, 3]

def get():
    if not a:
        return False
    return [item for item in a]

b = get()