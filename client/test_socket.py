import socket

def start_socket_client():
    try:
        # 创建Socket客户端
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8888))

        # 接收数据
        data = client_socket.recv(1024)  # 1024 是接收缓冲区大小，可以根据需要调整
        print(f"Received from server: {data.decode('utf-8')}")

        # 关闭连接
        client_socket.close()

    except Exception as e:
        print(f"Error in client: {e}")

if __name__ == '__main__':
    start_socket_client()
