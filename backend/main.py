import os

from app import *
from threading import Thread
from flask import request, jsonify, Blueprint
from database import *
from scheduler import Scheduler
import requests
from central_ac import *
import datetime
import hashlib
from sqlalchemy import func
import utils
import re

central_ac = CentralAc()
scheduler = Scheduler(central_ac)

t = Thread(target=scheduler.schedule)

rooms_ip = [{
    "room": "test",
    "port": "",
    "ip": ""
}]



# 登录
@app.route('/api/login', methods=['POST'])
def login_admin():
    """
    username
    password
    :return: {error:bool.
                role:str}  # room/administrator/manager/receptionist

curl.exe -v -X post -d '{"username":"administrator_1", "password":"administrator"}' http://localhost:11451/api/login?no-csrf
    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    username = params['username']
    password = params['password']

    ans = User.query.filter(User.username == username).filter(User.password == password).first()

    if ans.type == "administrator":
        role = "AC admin"
    elif ans.type == "receptionist":
        role = "checkout"
    elif ans.type == "manager":
        role = "manager"

    if ans is None:
        print('登录失败')
        return jsonify({'error_code': 100}), 401
    else:
        print('登录成功')
        ret = {'username': username, 'role': role}

        return jsonify(ret), 200
        # make_response(jsonify(response_data))


# 登出
@app.route('/api/logout', methods=['POST'])
def logout_admin():
    """
    当前账号退出
    :return: 204 成功
            401 error

curl.exe -v -X post http://localhost:11451/api/logout?no-csrf
    """

    return 204


weiruzhu = ['test', 'test2']


# 管理员加房
# 理解是增加一个未入住房间
@app.route('/api/admin/device', methods=['put'])
def add_room():
    """
    room:
        type: string
    public_key:
        type: string # RSA 4096

    :return: 200 room:
                    type: string
            401

curl.exe -v -X put -d '{"room":"test", "public_key":"RSA 4096"}' http://localhost:11451/api/admin/device?no-csrf
    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']
    public_key = params['public_key']

    try:
        weiruzhu.append(room)
        rooms_ip.append({
            "room": room,
            "port": "",
            "ip": ""
        })
        print(weiruzhu)
        return jsonify({'room': room}), 200
    except:
        return jsonify({'error_code': 100}), 401


# 管理员删房
@app.route('/api/admin/device', methods=['delete'])
def delete_room():
    """
    room:
        type: string


    :return: 200 room:
                    type: string
            401
curl.exe -v -X delete -d '{"room":"test"}' http://localhost:11451/api/admin/device?no-csrf
    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']

    # try:
    if room in weiruzhu:
        weiruzhu.remove(room)
        print(f"未入住'{room}' 已删除")
        rooms_ip = [room_info for room_info in rooms_ip if room_info["room"] != room]
        print(weiruzhu)
        return jsonify({'room': room}), 200
    elif room in scheduler.room_threads:
        del scheduler.room_threads[room]  # 此处等于scheduler函数中的删房函数
        print(f"已入住'{room}' 已删除")
        rooms_ip = [room_info for room_info in rooms_ip if room_info["room"] != room]
        return jsonify({'room': room}), 200
    else:
        print(f"Room '{room}' not found 未入住或已入住.")
        return jsonify({'error_code': 100}), 401

    # except:
    #     # raise ValueError(f"Room '{room}' not found 未入住或已入住.")
    #     print(f"except")
    #     return jsonify({'error_code': 100}), 401


# 管理员给出所有可利用的设备
@app.route('/api/admin/devices', methods=['get'])
def get_room_list():
    """

    :return: 200 room :
                    type: string array
            401

    调数据库

curl.exe -v -X get http://localhost:11451/api/admin/devices?no-csrf
    """
    try:
        available = scheduler.get_available_room()
        # for room in weiruzhu:
        #     available.append(room)
        return jsonify(available), 200
    except:
        return jsonify({'error_code': 100}), 401


# 管理员控制某一设备
@app.route('/api/admin/devices/<string:room_id>', methods=['post'])
def control_device(room_id):
    """
    room:
        type: string

    operation:
          type: string
          example:  'start, stop, temperature, wind_speed, mode,'
    data:
          type: string
          example: 26   # different for operations

    :return: 200 返回房间列表？？   ？？？？
            401

curl.exe -v -X post -d '{"operation":"start, stop, temperature, wind_speed", "data":"1, 0, 23, 3"}' http://localhost:11451/api/admin/devices/test?no-csrf
    """
    if room_id not in scheduler.room_threads.keys():
        print("该房间不存在")
        return jsonify({'error_code': 100}), 401
    params = request.get_json(force=True)
    print(request.path, " : ", params)

    operation = params['operation']
    data = params['data']

    operations = [element.strip() for element in operation.split(',')]
    datas = [datas.strip() for datas in data.split(',')]
    operation_data = dict(zip(operations, datas))

    start = operation_data.get('start')
    target_temp = operation_data.get('temperature')
    wind_speed = operation_data.get('wind_speed')

    if wind_speed == '3':
        wind_speed = 'HIGH'
    elif wind_speed == '2':
        wind_speed = 'MID'
    elif wind_speed == '1':
        wind_speed = 'LOW'

    power = True
    for room in scheduler.room_threads.values():
        if room.room_id == room_id:
            power = room.power

    # try:
    print("请求的开关机", bool(int(start)))
    print("房间当前的开关机", power)
    if bool(int(start)) == bool(power) and bool(start):
        print("更改风速温度")
        scheduler.deal_with_speed_temp_change(room_id, int(target_temp), wind_speed)

        #control_client(room_id, True, target_temp, wind_speed)
    else:
        if start == '1':
            start = 'ON'
            print(room_id, "开机")
        else:
            print(room_id, "关机")
        scheduler.deal_with_on_and_off(room_id, int(target_temp), wind_speed, start)

        #control_client(room_id, False, target_temp, wind_speed)

    return jsonify({'room': room_id}), 200
    # except:
    #     return jsonify({'error_code': 100}), 401

room_temp = {
    "test": 30
}
# 对某一房间进行状态查询
@app.route('/api/status/<string:room_id>', methods=['GET'])
def get_one_status(room_id):
    """
    room:
        type: string


    :return: 200 room, temperature, wind_speed, mode, sweep, is_on, last_update
            401
curl.exe -v -X get http://localhost:11451/api/status/test?no-csrf
    """

    # try:
        # if room_id in weiruzhu:
        #     json = jsonify({
        #         'room': room_id,
        #         'temperature': 25,
        #         'wind_speed': 2,
        #         'mode': 'cold',
        #         # 'sweep': sweep,
        #         'is_on': False,
        #         'is_ruzhu': False
        #     })
        #     print(json)
        #     return json, 200
    speed_to_num = {'HIGH': 3, 'MID': 2, 'LOW': 1}
    print(room_id)
    print(scheduler.room_threads.keys())
    room_message = scheduler.get_room_message(room_id)
    if room_message["wind_speed"] == None:
        init_temp = room_temp[room_id]
        room_message = {
            'room': room_id,
            'temperature': init_temp,
            'wind_speed': 2,
            'mode': 'cold',
            # 'sweep': sweep,
            'is_on': False,
            'is_ruzhu': False
        }
    else:
        room_message['wind_speed'] = speed_to_num[room_message['wind_speed']]
    json = jsonify(room_message)
    print(json)
    return json, 200
    # except:
    #     return jsonify({'error_code': 100}), 401


# 获取所有房间开关信息
@app.route('/api/status', methods=['get'])
def get_all_status():
    """

    :return: 200 room, is_on(开关机状态)

            401

curl.exe -v -X get http://localhost:11451/api/status?no-csrf
    """
    try:
        json = []
        # for room in weiruzhu:
        #     status[room] = False
        for room in scheduler.room_threads.values():
            status = {}
            status['room'] = room.room_id
            status['is_on'] = room.power
            json.append(status)

        return jsonify(json), 200
    except:
        return jsonify({'error_code': 100}), 401


# 开房
@app.route('/api/room/check_in', methods=['POST'])
def check_in():
    """前台开房
    roomId
    :return: 200 room,

            401

curl.exe -v -X POST -d '{"room": "test"}' http://localhost:11451/api/room/check_in?no-csrf
    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']
    temp = params['temperature']
    print(temp)
    temp = int(temp)

    if room not in room_temp.keys():
        room_temp[room] = temp

    if room not in weiruzhu:
        print(weiruzhu)
        print('这房间您的管理员没加呢，不存在这房间号。')
        return jsonify({'error_code': 100}), 401
    else:
        # try:
        rooms = []
        rooms.append(room)
        #print(rooms)
        temps = []
        temps.append(temp)
        scheduler.add_room(rooms)
        scheduler.set_room_initial_env_temp(rooms, temps)
        json = jsonify('room', room)
        weiruzhu.remove(room)
        print("已入住")
        print(weiruzhu)
        return json, 200
        # except:
        #     return jsonify({'error_code': 100}), 401


# 退房
@app.route('/api/room/check_out', methods=['POST'])
def check_out():
    """前台退房
    roomId:int

    :return: room,
            report_data:
                total_cost
                total_time
                details:
                    start_time
                    end_time
                    temperature 不用
                    wind_speed
                    mode

                    duration
                    cost

    调数据库
curl.exe -v -X POST -d '{"room": "test"}' http://localhost:11451/api/room/check_out?no-csrf
    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']

    order = Order.query.filter_by(room_id=room).order_by(Order.checkin.desc()).first()
    if order is None:
        print("数据库中没有找到与之匹配的房间号")
        return jsonify({'error_code': 100}), 401

    checkin = order.checkin
    checkout = order.checkout
    total_time = checkout - checkin
    total_cost = order.total_cost

    details = Detail.query.filter_by(room_id=room).order_by(Detail.start_time.desc()).all()

    de = {}

    # 遍历查询结果并提取所需信息
    for detail in details:
        de.update({
            'start_time': detail.start_time.isoformat(),
            'end_time': detail.end_time.isoformat(),
            'wind_speed': detail.wind_speed,
            'mode': detail.mode,
            'duration': detail.times_used,
            'cost': detail.fee
        })

    report_data = {
        'total_cost': total_cost,
        'total_time': total_time,
        'details': de
    }

    delete = []
    delete.append(room)
    scheduler.delete_room(delete)
    weiruzhu.append(room)

    return jsonify(report_data), 200


# 客户端连接

@app.route('/api/device/client', methods=['POST'])
def client_connect():
    """
    room_id
    port    #Port for WebHook
    unique_id   #random Unique ID, 16 characters
    signature   #SHA256withRSA, RSA 4096, sign text = room_id + unique_id + port

    :return:204 succes
            401

curl.exe -v -X POST -d '{"room_id": "test"}' http://localhost:11451/api/device/client?no-csrf
    """
    data = request.json
    print(data)
    room_id = data.get('room_id')
    port = data.get('port')
    client_ip = request.remote_addr

    # unique_id = data.get('unique_id')
    # signature = data.get('signature')

    # sign_text = room_id + unique_id + str(port)
    # if sign_text == signature:
    #     return 204
    # else:
    #     return jsonify({'error_code': 100}), 401

    for room_ip in rooms_ip:
        if room_ip["room"] == room_id:
            room_ip["port"] = port
            room_ip["ip"] = client_ip

    return jsonify({"message": "succeed"}), 200


# 服务器更改客户端状态
#@app.route('/api/control', methods=['POST'])
def control_client(room_id, is_on: bool, target_temp, wind):
    """
    send:
    operation   # start, stop, temperature, wind_speed, mode
    data        # example: 26  operations

    :return: 204 401
    """
    port = ''
    client_ip = ''
    for room_ip in rooms_ip:
        if room_ip["room"] == room_id:
            port = room_ip["port"]
            client_ip = room_ip["ip"]

    webhook_url = 'http://' + client_ip + ':' + port + '/api/control'  # 前端提供的Webhook URL
    operation = "start, stop, temperature, wind_speed, mode"
    data = str(is_on) + ',' + str(not is_on) + ',' + str(target_temp) + ',' + str(wind) + ',' + 'cold'
    json = {
        "operation": operation,
        "data": data
    }
    try:
        response = requests.post(webhook_url, json=json)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")

    return jsonify({"message": "Online successfully"}), 200


# 客户端主动更改状态
@app.route('/api/device/client/<string:room_id>', methods=['POST'])
def client_change(room_id):
    """
    room_id
    operation   # start, stop, temperature, wind_speed, mode, sweep
    data        # example: 26  operations
    time        # 更改日期
    unique_id？？   # random Unique ID, 16 characters
    signature？？   # SHA256withRSA, RSA 4096, sign text = operation + unique_id + data + time
    :return: 204
            401

curl.exe -v -X POST -d '{"room_id": "test", "operation": "start, stop, temperature, wind_speed, mode", "data": "1, 0, 16, 3, cold", "time": "2023-09-18T11:45:14+08:0", "unique_id": "1145141919810abc", "signature": "SHA256withRSA"}' http://localhost:11451/api/device/client/test?no-csrf
    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    operation = params['operation']
    data = params['data']
    time = params['time']

    unique_id = params['unique_id']
    signature = params['signature']

    operations = [element.strip() for element in operation.split(',')]
    datas = [datas.strip() for datas in data.split(',')]
    operation_data = dict(zip(operations, datas))

    start = operation_data.get('start')
    target_temp = operation_data.get('temperature')
    wind_speed = operation_data.get('wind_speed')

    if wind_speed == str(3):
        wind_speed = 'HIGH'
    elif wind_speed == str(2):
        wind_speed = 'MID'
    elif wind_speed == str(1):
        wind_speed = 'LOW'

    if room_id not in scheduler.room_threads:
        print("该房间未入住")
        return jsonify({'error_code': 100}), 401

    power = True
    for room in scheduler.room_threads.values():
        if room.room_id == room_id:
            power = room.power

    print("请求的开关机",start)
    print("房间当前的开关机",power)
    if bool(int(start)) == bool(power) and bool(power):
        print("更改风速")
        if start == '1':
            start = 'ON'
        #print(room_id, target_temp, wind_speed, start)
        scheduler.deal_with_speed_temp_change(room_id, int(target_temp), wind_speed)
    else:
        if start == '1':
            start = 'ON'
            print(room_id, "开机")
        else:
            print(room_id, "关机")
        #print(room_id, target_temp, wind_speed, start)
        return_state = scheduler.deal_with_on_and_off(room_id, int(target_temp), wind_speed, start)
        print(return_state)

    return jsonify({"message": "Online successfully"}), 204


# 管理员给出所有未入住房间信息
@app.route('/api/admin/uncheck_in', methods=['get'])
def get_uncheckin_room_list():
    """

    :return: 200 room :
                    type: string array
            401

    调数据库

curl.exe -v -X get http://localhost:11451/api/admin/uncheck_in?no-csrf
    """
    try:
        # available = scheduler.get_available_room()
        available = []
        for room in weiruzhu:
            available.append(room)
        return jsonify(available), 200
    except:
        return jsonify({'error_code': 100}), 401


if __name__ == '__main__':
    db_init()
    t.start()
    # api = Blueprint('api', __name__, url_prefix='/api')
    # app.register_blueprint(api)
    with app.app_context():
        app.run(port=11451, debug=True, host='0.0.0.0')

    # scheduler.schedule()
"""
调试：
http://localhost:11451/__debugger__/683-942-319
开房test
curl.exe -v -X POST -d '{"room": "test", "temperature": 30}' http://localhost:11451/api/room/check_in?no-csrf
客户端更改状态：开机
curl.exe -v -X POST -d '{"room_id": "test", "operation": "start, stop, temperature, wind_speed, mode", "data": "1, 0, 16, 3, cold", "time": "2023-09-18T11:45:14+08:0", "unique_id": "1145141919810abc", "signature": "SHA256withRSA"}' http://localhost:11451/api/device/client/test?no-csrf
关机
curl.exe -v -X POST -d '{"room_id": "test", "operation": "start, stop, temperature, wind_speed, mode", "data": "0, 1, 16, 3, cold", "time": "2023-09-18T11:45:14+08:0", "unique_id": "1145141919810abc", "signature": "SHA256withRSA"}' http://localhost:11451/api/device/client/test?no-csrf

管理员开机
curl.exe -v -X post -d '{"operation":"start, stop, temperature, wind_speed", "data":"1, 0, 18, 3"}' http://localhost:11451/api/admin/devices/test?no-csrf
管理员关机
curl.exe -v -X post -d '{"operation":"start, stop, temperature, wind_speed", "data":"0, 1, 18, 3"}' http://localhost:11451/api/admin/devices/test?no-csrf

"""
