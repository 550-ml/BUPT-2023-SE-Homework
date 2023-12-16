from flask import Flask, request, jsonify
import socket
import threading
import json

app = Flask(__name__)

# 客户端内部状态，用字典来保存
client_state = {
    "start":"0",
    "stop":"1",
    "temperature": 25,
    "wind_speed": "",
    "mode": "cold",
    #"sweep":"on",#送风 on,stop
    # 可以根据实际需要添加其他状态
}
connected_clients = set()
# 添加一个简单的路由，返回 "Hello"(测试用例)
#@app.route('/')
#def hello():
#    return 'Hello'
# 处理服务器更改客户端状态请求
@app.route('/api/control', methods=['POST'])
def control_device():
    request1 = request.json
    operation = request1["operation"]
    data = request1["data"]
    operations = [element.strip() for element in operation.split(',')]
    data1 = [data1.strip() for data1 in data.split(',')]
    operation_data = dict(zip(operations, data1))
    # 处理服务器更改客户端状态请求
    # 以下是一个简单的示例，你可以根据你的业务逻辑进行修改
    for key, value in operation_data.items():
        if key == "start":
          client_state["start"] = value  # is_on
        elif key == "stop":
            client_state["stop"] = value  # not is_on
        elif key == "temperature":
            client_state["temperature"] = value  # 26
        elif key == "wind_speed":
            client_state["wind_speed"] = value  # low, mid, high
        elif key == "mode":
            client_state["mode"] = value
    #   elif key == "sweep":
    #        client_state["sweep"] = value
    #if "sweep" in operation_data:
    #     client_state["sweep"] = operation_data["sweep"]#on,stop
    broadcast_state()
    # 返回一个表示成功的响应
    return jsonify({'message': 'State changed successfully'}), 200

def broadcast_state():
    # 遍历所有连接的客户端并发送更新的状态
    for client_socket in connected_clients:
        try:
            client_socket.sendall(json.dumps(client_state).encode())
        except Exception as e:
            print(f"向客户端广播状态时发生错误: {e}")
            # 根据需要处理异常（例如，从集合中删除客户端）

def start_flask_server():
    app.run(debug=True,host='0.0.0.0',port=5681, use_reloader=False)

def start_socket_server():
    # 创建Socket服务器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8892))
    server_socket.listen(5)# 允许同时最多5个连接
    print("Socket服务器正在监听端口8892")
    while True:  # 持续监听
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"与客户端 {client_address}建立连接")
        # 发送 "Hello" 给客户端(测试用例)
        #client_socket.sendall(b'Hello')
        # 发送更新的数据给客户端
        connected_clients.add(client_socket)

        # 发送更新的数据给客户端
        try:
            client_socket.sendall(json.dumps(client_state).encode())
        except Exception as e:
            print(f"向新客户端发送初始状态时发生错误: {e}")

        # 创建一个线程处理该客户端的消息
        threading.Thread(args=(client_socket,)).start()
    
if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask_server)
    socket_thread = threading.Thread(target=start_socket_server)

    flask_thread.start()
    socket_thread.start()

    flask_thread.join()
    #socket_thread.join()#不需要join监听服务器的线程，因为它应该是持续运行的