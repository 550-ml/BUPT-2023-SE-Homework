import heapq
from datetime import datetime
import time

# ready_queue = [(3, 1, '1')]
# heapq.heappush(ready_queue, (1, 2, '2'))
# print(ready_queue)

start_time = datetime.now()
time.sleep(5)
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()
print(duration)
