import re
from threading import Thread
from app import *
from flask import request, jsonify
from database import *
from sqlalchemy import func
import utils
from scheduler import Scheduler
import datetime


scheduler = Scheduler()
t = Thread(target=scheduler.schedule)

# 登录
@app.route('/login', methods=['POST'])
def login_admin():
    """
    username
    password
    :return: {error:bool.
                role:str}  # room/administrator/manager/receptionist

    不用加
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

    向后端发送信号，往账单表里添加元组
    """




    return jsonify(ret), 200

# 管理员删房
@app.route('/admin/device', methods=['delete'])
def delete_room():
    """
    room:
        type: string


    :return: 200 room:
                    type: string
            401

    将账单里的删除
    """

# 管理员给出所有可利用的设备
@app.route('admin/devices', methods=['get'])
def get_room_list():
    """
    room:
        type: string

    :return: 200 room 数组:
                    type: string array
            401

    调数据库
    """


# 管理员控制某一设备
@app.route('admin/devices/{room_id}', methods=['post'])
def control_device():
    """
    room:
        type: string

    operation:
          type: string
          example:  'start, stop, temperature, wind_speed, mode, sweep'
    data:
          type: string
          example: 26   # different for operations

    :return: 200 items:
                    type: string
            401


    """


# 对某一房间进行状态查询
@app.route('/status/{room_id}', methods=['get'])
def get_one_status():
    """
    room:
        type: string
    public_key:
        type: string # RSA 4096

    :return: 200 room, temperature, wind_speed, mode, sweep, is_on, last_update
            401

    """


# 获取所有房间状态信息
@app.route('/status', methods=['get'])
def get_all_status():
    """
    room:
        type: string
    public_key:
        type: string # RSA 4096

    :return: 200 room, is_on(开关机状态)

            401

    """


# 开房
@app.route('/room/check_in', methods=['POST'])
def check_in():
    """前台开房
    roomId
    :return: 200 room,

            401
    """


    return


# 退房 FINISH
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
                    temperature
                    wind_speed
                    mode
                    sweep       ??
                    duration
                    cost

    调数据库
    """



# 客户端