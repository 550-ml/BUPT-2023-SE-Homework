import heapq
import time
import threading
from scheduler import Scheduler

from central_ac import CentralAc

centralAC = CentralAc()
scheduler = Scheduler(centralAC)

scheduler.schedule
