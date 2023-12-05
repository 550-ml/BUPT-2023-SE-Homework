from flask import Flask, request, jsonify

app = Flask(__name__)

# 客户端内部状态，用字典来保存
client_state = {
    "temperature": 0,
    "wind_speed": 0,
    "mode": "off",
    # 可以根据实际需要添加其他状态
}

# 服务器更改客户端状态请求
@app.route('/control', methods=['POST'])
def control_device():
    data = request.json
    
    # 处理服务器更改客户端状态请求
    # 以下是一个简单的示例，你可以根据你的业务逻辑进行修改
    if "temperature" in data:
        client_state["temperature"] = data["temperature"]
    if "wind_speed" in data:
        client_state["wind_speed"] = data["wind_speed"]
    if "mode" in data:
        client_state["mode"] = data["mode"]
    
    # 返回一个表示成功的响应
    return jsonify({'message': 'State changed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5677)#http://localhost:5677
