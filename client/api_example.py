import requests
import json
import hashlib
import rsa
import random
from datetime import datetime

# 生成唯一标识符
unique_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))

# 请求数据
room_id = '2-233'
port = '11451'
data = '26'
operation = 'start'
time = datetime.now().isoformat()

# 生成签名文本
sign_text = room_id + unique_id + port
signature = hashlib.sha256(sign_text.encode()).hexdigest()

# 配置服务器的URL
base_url = 'http://localhost:11451/api'

# /device/client 端点的请求数据
client_data = {
    "room_id": room_id,
    "port": port,
    "unique_id": unique_id,
    "signature": signature
}

# /device/client/{room_id} 端点的请求数据
client_operation_data = {
    "operation": operation,
    "data": data,
    "time": time,
    "unique_id": unique_id,
    "signature": signature
}

# /control 端点的请求数据
server_operation_data = {
    "operation": operation,
    "data": data
}

# 发送到 /device/client 的 POST 请求
response = requests.post(f'{base_url}/device/client', json=client_data)
print(response.status_code)
print(response.json())

# 发送到 /device/client/{room_id} 的 POST 请求
response = requests.post(f'{base_url}/device/client/{room_id}', json=client_operation_data)
print(response.status_code)
print(response.json())

# 发送到 /control 的 POST 请求
response = requests.post(f'{base_url}/control', json=server_operation_data)
print(response.status_code)
print(response.json())


import requests
import time

# 服务器的基本 URL
base_url = 'http://localhost:11451/api'

# 客户端的房间号
room_id = '2-233'

# 每秒向服务器索取空调状态的函数
def get_ac_status():
    while True:
        try:
            # 发送到 /room/updateRoomState 的 POST 请求
            response = requests.post(f'{base_url}/room/updateRoomState', json={'roomId': room_id})
            if response.status_code == 200:
                room_state = response.json().get('roomState')
                if room_state:
                    speed = room_state.get('speed')
                    curr_temp = room_state.get('currTemp')
                    target_temp = room_state.get('targetTemp')
                    fee = room_state.get('fee')
                    ac_state = room_state.get('acState')
                    print(f'空调状态：风速-{speed}，当前温度-{curr_temp}，目标温度-{target_temp}，费用-{fee}，空调状态-{ac_state}')
                else:
                    print('未获取到空调状态')
            else:
                print(f'获取空调状态失败，状态码：{response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'请求异常：{e}')
        
        time.sleep(1)

# 调用函数开始每秒索取空调状态
get_ac_status()
