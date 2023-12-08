from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# 客户端内部状态，用字典来保存
client_state = {
    "start":"",
    "stop":"",
    "temperature": 0,
    "wind_speed": "",
    "mode": "cold",
    "sweep":"on",#送风 on,stop
    # 可以根据实际需要添加其他状态
}
# 添加一个简单的路由，返回 "Hello"(测试用例)
#@app.route('/')
#def hello():
#    return 'Hello'
# 处理服务器更改客户端状态请求
@app.route('/control', methods=['POST'])
def control_device(data):
    data = request.json
    # 处理服务器更改客户端状态请求
    # 以下是一个简单的示例，你可以根据你的业务逻辑进行修改
    if "start" in data:
        client_state["start"] = data["start"]#is_on
    if "stop" in data:
        client_state["stop"] = data["stop"]#not is_on
    if "temperature" in data:
        client_state["temperature"] = data["temperature"]#26
    if "wind_speed" in data:
        client_state["wind_speed"] = data["wind_speed"]#low,mid,high
    if "mode" in data:
        client_state["mode"] = data["mode"]#cold,hot
    if "sweep" in data:
         client_state["sweep"] = data["sweep"]#on,stop
    # 返回一个表示成功的响应
    return jsonify({'message': 'State changed successfully'}), 200
def start_flask_server():
    app.run(debug=True, port=5677, use_reloader=False)
def start_socket_server():
    # 创建Socket服务器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)# 允许同时最多5个连接
    print("Socket server is listening on port 8888")
    while True:  # 持续监听
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        # 发送 "Hello" 给客户端(测试用例)
        #client_socket.sendall(b'Hello')
        # 发送更新的数据给客户端
        client_socket.sendall(str(client_state).encode())
    
if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask_server)
    socket_thread = threading.Thread(target=start_socket_server)

    flask_thread.start()
    socket_thread.start()

    flask_thread.join()
    #socket_thread.join()#不需要join监听服务器的线程，因为它应该是持续运行的