import re
from threading import Thread
from app import *
from flask import request, jsonify
from database import *
from sqlalchemy import func
import utils
from scheduler import Scheduler
import datetime
import hashlib

import requests
import central_ac


scheduler = Scheduler()
ac = CentralAc()
t = Thread(target=scheduler.schedule)

# 登录
@app.route('/login', methods=['POST'])
def login_admin():
    """
    username
    password
    :return: {error:bool.
                role:str}  # room/administrator/manager/receptionist
    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    username = params['username']
    password = params['password']

    ans = User.query.filter(User.username == username).filter(User.password == password).first()

    if ans is None:
        print('登录失败')
        return jsonify({'error_code': 100}), 401
    else:
        print('登录成功')
        ret = {'username': username}

        return jsonify(ret), 200
        # make_response(jsonify(response_data))

# 登出
@app.route('/logout', methods=['POST'])
def logout_admin():
    """
    当前账号退出
    :return: 204 成功
            401 error
    """

    return 204

# 管理员加房
@app.route('/admin/device', methods=['put'])
def add_room():
    """
    room:
        type: string
    public_key:
        type: string # RSA 4096

    :return: 200 room:
                    type: string
            401

    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']
    public_key = params['public_key']

    try:
        rooms = []
        rooms.append(room)
        scheduler.add_room(rooms)
        return jsonify({'room': room}), 200
    except:
        return jsonify({'error_code': 100}), 401

# 管理员删房
@app.route('/admin/device', methods=['delete'])
def delete_room():
    """
    room:
        type: string


    :return: 200 room:
                    type: string
            401

    """

    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']

    # 删除队列中的房间对象



# 管理员给出所有可利用的设备
@app.route('admin/devices', methods=['get'])
def get_room_list():
    """

    :return: 200 room :
                    type: string array
            401

    调数据库
    """

    # 给出等待与服务队列的所有房间号

def control_device(is_on:bool, target_temp, wind)

# 管理员控制某一设备
@app.route('admin/devices/<string:room_id>', methods=['post'])
def control_device(room_id):
    """
    room:
        type: string

    operation:
          type: string
          example:  'start, stop, temperature, wind_speed, mode, sweep不要了'
    data:
          type: string
          example: 26   # different for operations

    :return: 200 返回房间列表？？   ？？？？
            401


    """
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

    for room in scheduler.room_threads:
        if room.room_id == room_id:
            power = room.power

    if bool(start) == bool(power) == True:
        scheduler.deal_with_speed_temp_change(room_id, target_temp, wind_speed)

        control_device(True, target_temp, wind_speed)
    else:
        scheduler.deal_with_on_and_off(room_id, target_temp, wind_speed, start)

        control_device(False, target_temp, wind_speed)

    return jsonify({'room': room_id}), 200


# 对某一房间进行状态查询
@app.route('/status/<string:room_id>', methods=['GET'])
def get_one_status(room_id):
    """
    room:
        type: string
    public_key:
        type: string # RSA 4096

    :return: 200 room, temperature, wind_speed, mode, sweep, is_on, last_update
            401

    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    public_key = params['public_key']

    #detail = Detail.query.filter_by(room_id=room_id).order_by(Detail.start_time.desc()).first()
    for room in scheduler.room_threads:
        if room.room_id == room_id:
            is_on = room.power
            temperature = room.current_temp
            wind_speed = room.current_speed
            mode = 'cold'
            sweep = room.running
            #last_update =

    return jsonify({
        'room': room_id,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'mode': mode,
        #'sweep': sweep,
        'is_on': is_on,
        #'last_update': last_update
    }), 200




# 获取所有房间状态信息
@app.route('/status', methods=['get'])
def get_all_status():
    """

    :return: 200 room, is_on(开关机状态)

            401

    """

    #对目前可利用的状态队列，查询详单


# 开房
@app.route('/room/check_in', methods=['POST'])
def check_in():
    """前台开房
    roomId
    :return: 200 room,

            401
    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']

    try:
        rooms = []
        rooms.append(room)
        scheduler.add_room(rooms)
        json = jsonify('room',room)
        return json, 200
    except:
        return 401




# 退房
@app.route('/room/check_out', methods=['POST'])
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
    """
    params = request.get_json(force=True)
    print(request.path, " : ", params)
    room = params['room']

    order = Order.query.filter_by(room_id=room).order_by(Order.checkin.desc()).first()
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

    return jsonify(report_data), 200

# 客户端连接
port = ''
client_ip = ''
@app.route('/device/client', methods=['POST'])
def client_connect():
    """
    room_id
    port    #Port for WebHook
    unique_id   #random Unique ID, 16 characters
    signature   #SHA256withRSA, RSA 4096, sign text = room_id + unique_id + port

    :return:204 succes
            401
    """
    data = request.json
    room_id = data.get('room_id')
    port = data.get('port')
    client_ip = request.remote_addr

    #unique_id = data.get('unique_id')
    #signature = data.get('signature')

    # sign_text = room_id + unique_id + str(port)
    # if sign_text == signature:
    #     return 204
    # else:
    #     return jsonify({'error_code': 100}), 401

    return 204

# 服务器更改客户端状态
@app.route('/control', methods=['POST'])
def control_device(is_on:bool, target_temp, wind):
    """
    send:
    operation   # start, stop, temperature, wind_speed, mode
    data        # example: 26  operations

    :return: 204 401
    """


    webhook_url = 'http://' + client_ip + ':' + port + '/api'  # 前端提供的Webhook URL
    data = {
        'start': is_on,
        'stop': not is_on,
        'temperature': target_temp,
        'wind_speed': wind,
        'mode': 'cold'
    }
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")

    return

# 客户端主动更改状态
@app.route('/device/client/<string:room_id>', methods=['POST'])
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

    for room in scheduler.room_threads:
        if room.room_id == room_id:
            power = room.power

    if bool(start) == bool(power) == True:
        scheduler.deal_with_speed_temp_change(room_id, target_temp, wind_speed)
    else:
        scheduler.deal_with_on_and_off(room_id, target_temp, wind_speed, start)

    return 204



