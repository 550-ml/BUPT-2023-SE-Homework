import heapq
import threading
from datetime import datetime

from room1 import Room


class Queues:
    def __init__(self) -> None:
        self.wait_count = 0
        self.index = 0
        self.ready_queue = []
        self.wait_lock = threading.Lock()

        self.suspend_queue = {}

        self.running_queue = {}  # 设计成字典类型，通过room_id访问
        self.service_lock = threading.Lock()

    # 将服务对象加入等待/待调度队列
    def add_into_ready_queue(self, service_object: Room, priority):
        heapq.heappush(self.ready_queue, (priority, datetime.now(), service_object))
        return True

    # 从等待/待调度队列中取得优先级最高的服务对象
    def get_from_ready_queue(self):
        service_objects = heapq.nsmallest(1, self.ready_queue)
        if not service_objects:
            return None
        return service_objects[0][-1], service_objects[0][-2]

    def add_into_suspend_queue(self, room: Room):
        time_now = datetime.now()
        self.suspend_queue[room] = time_now

    def pop_suspend_queue(self):
        ready_to_pop = []
        time_now = datetime.now()
        for room, start_time in self.suspend_queue.items():
            if (time_now - start_time).total_seconds() >= 60:
                ready_to_pop.append(room)
        if len(ready_to_pop) == 0:
            return None
        else:
            for room in ready_to_pop:
                self.suspend_queue.pop(room)
            return ready_to_pop

    # 把等待/待调度队列中优先级最高的服务对象弹出
    def pop_ready_queue(self):
        # with self.wait_lock:
        #     if self.wait_count == 0:
        #         return None
        #     self.wait_count -= 1
        service_object = heapq.heappop(self.ready_queue)[-1]
        # service_object.wait_clock = 0  # 清空等待时长
        return service_object

    # 把服务对象加入到服务队列中
    def add_into_running_queue(self, service_object: Room):
        # with self.service_lock:
        #     service_object.current_speed = service_object.target_speed
        self.running_queue[service_object.room_id] = service_object
        # # 初始化时钟
        # service_object.wait_clock = 0
        # service_object.service_clock = 0
        # service_object.start_serve()
        return True

    # 把房间id为room_id的服务对象从服务队列中弹出
    def pop_service_by_room_id(self, room_id):
        self.running_queue.pop(room_id)

    # 得到服务队列中优先级最低且运行时间最长的一个服务对象
    def get_running_room_with_lowest_priority(self):
        priority = {'HIGH': 1, 'MID': 2, 'LOW': 3}
        room_with_lowest_priority_and_longest_time = None
        lowest_priority = None
        longest_running_time = 0
        time_now = datetime.now()

        for room_id, room in self.running_queue.items():
            room_priority = priority[room.current_speed]
            running_time = (time_now - room.start_time).total_seconds()

            if (lowest_priority is None or
                    room_priority > lowest_priority or
                    (room_priority == lowest_priority and running_time > longest_running_time)):

                room_with_lowest_priority_and_longest_time = room
                lowest_priority = room_priority
                longest_running_time = running_time
        return room_with_lowest_priority_and_longest_time
