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
