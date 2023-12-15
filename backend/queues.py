import heapq
from datetime import datetime

from room import Room
from utils import current_temp


class Queues:
    def __init__(self) -> None:
        self.ready_queue = []
        self.suspend_queue = {}
        self.running_queue = {}  # 设计成字典类型，通过room_id访问
        self.off_queue = []

    def add_into_off_queue(self, room_id):
        self.off_queue.append[room_id]


    def get_all_rooms_from_off_queue(self):
        if not self.off_queue:
            return False
        return self.off_queue
    

    def pop_off_queue(self, room_id):
        if room_id not in self.off_queue:
            return None
        del self.off_queue[room_id]


    # 将服务对象加入等待/待调度队列
    def add_into_ready_queue(self, room_id, priority):
        heapq.heappush(self.ready_queue, (priority, datetime.now(), room_id))
        return True

    # 从等待/待调度队列中取得优先级最高的服务对象
    def get_from_ready_queue(self):
        service_objects = heapq.nsmallest(1, self.ready_queue)
        if not service_objects:
            return None, None
        return service_objects[0][-1], service_objects[0][-2]  # room_id, start_waiting_time

    def get_all_rooms_from_ready_queue(self):
        if not self.ready_queue:
            return False
        return [item[2] for item in self.ready_queue]
    
    # 关机时，对象在等待队列中
    def remove_from_ready_queue(self, room_id):
        # 查找与room_id匹配的元素
        for i, (_, _, ready_room_id) in enumerate(self.ready_queue):
            if ready_room_id == room_id:
                # 移除匹配的元素
                self.ready_queue.pop(i)
                # 重新构建堆
                heapq.heapify(self.ready_queue)
                return True
        return False  # 如果没有找到匹配的元素

    # 把等待/待调度队列中优先级最高的服务对象弹出
    def pop_ready_queue(self):
        room_id = heapq.heappop(self.ready_queue)[-1]
        return room_id

    # deep_copy
    def add_into_suspend_queue(self, room: Room):
        time_now = datetime.now()
        self.suspend_queue[room] = time_now

    def get_all_rooms_from_suspend_queue(self):
        if not self.suspend_queue:
            return False
        return list(self.suspend_queue.keys().room_id)

    def pop_suspend_queue(self):
        ready_to_pop = []
        time_now = datetime.now()
        for room, start_time in self.suspend_queue.items():
            duration = (time_now - start_time).total_seconds()
            temp_now = current_temp(room, time_now)
            if duration >= 60 and temp_now >= room.target_temp:
                ready_to_pop.append(room)
        if len(ready_to_pop) == 0:
            return None
        else:
            for room in ready_to_pop:
                self.suspend_queue.pop(room)
            return ready_to_pop

    # 关机时，对象在挂起队列中
    def remove_from_suspend_queue(self, room_id):
        for room in self.suspend_queue.keys():
            if room.room_id == room_id:
                self.suspend_queue.pop(room)
                return True
        return False

    # 把服务对象加入到服务队列中
    def add_into_running_queue(self, room_id):
        self.running_queue[room_id] = room_id
        return True

    # 把房间id为room_id的服务对象从服务队列中弹出
    def pop_service_by_room_id(self, room_id):
        self.running_queue.pop(room_id)

    @ staticmethod
    # 得到服务队列中优先级最低且运行时间最长的一个服务对象
    def get_running_room_with_lowest_priority(room_threads):
        priority = {'HIGH': 1, 'MID': 2, 'LOW': 3}
        room_with_lowest_priority_and_longest_time = None
        lowest_priority = None
        longest_running_time = 0
        time_now = datetime.now()

        for room_id, room in room_threads.items():
            room_priority = priority[room.current_speed]
            running_time = (time_now - room.start_time).total_seconds()

            if (lowest_priority is None or
                    room_priority > lowest_priority or
                    (room_priority == lowest_priority and running_time > longest_running_time)):

                room_with_lowest_priority_and_longest_time = room_id
                lowest_priority = room_priority
                longest_running_time = running_time
        return room_with_lowest_priority_and_longest_time
