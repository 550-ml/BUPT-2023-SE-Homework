# import heapq
# import time
# import threading
# from scheduler import Scheduler

# from central_ac import CentralAc

# centralAC = CentralAc()
# scheduler = Scheduler(centralAC)

# scheduler.schedule

a = [1, 2, 3]

def delete(id):
    if id not in a:
        return None
    del a[id]