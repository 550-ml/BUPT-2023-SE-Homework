
"""
程序名称: Central Air Conditioning Management System (CACMS) Backend Service
程序描述:
    - 利用 Flask 和 SQLAlchemy 构建，提供RESTful API接口以响应前端请求。
    - 包括用户验证、房间和设备状态管理、费用计算等核心功能。

主要模块及其功能:
    1. 数据模型定义: 使用 SQLAlchemy 定义数据库模型，包括用户、详单和账单等。
    2. 数据库操作: 提供增加详单和账单的函数，用于处理数据库交互。
    3. 数据库初始化: 定义初始化数据库的函数，用于设置初始状态和测试数据。
    4. (被注释掉的) 统计报表模型: 为酒店经理提供统计信息的数据模型。

接口说明: 无直接接口，但提供数据库交互的后端逻辑。

开发者信息:
    - 开发者: [陈悦-2021211882]
    - 开发日期: [2023-12]
"""

from app import *
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy(app)

# 用户表存储账号密码，用于登录验证
class User(db.Model):
    username = db.Column(db.String(80), unique=True, primary_key=True)
    password = db.Column(db.String(80), nullable=True)
    type = db.Column(db.Enum('receptionist', 'manager', 'administrator'))

# 详单表
class Detail(db.Model):
    room_id = db.Column(db.String(50), nullable=True, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.datetime.now(), primary_key=True)
    end_time = db.Column(db.DateTime, default=0, onupdate=datetime.datetime.now(), primary_key=True)
    speed = db.Column(db.Enum("HIGH", "MID", "LOW"), primary_key=True)
    fee = db.Column(db.Float, default=0.0, primary_key=True)
    times_used = db.Column(db.Float, nullable=True, primary_key=True)
    target_temp = db.Column(db.Integer, nullable=True, primary_key=True)
    route = db.Column(db.String(255), primary_key=True)

    def __str__(self) -> str:
        return 'room_id:{0},start_time:{1},end_time:{2},speed:{3},fee:{4},times_used:{5}'.format(
             self.room_id, self.start_time, self.end_time, self.speed, self.fee, self.times_used, self.target_temp, self.route)

    def __repr__(self) -> str:
        return self.__str__()

# 账单表
class Order(db.Model):
    room_id = db.Column(db.String(50), primary_key=True)
    checkin = db.Column(db.DateTime, default=datetime.datetime.now())
    checkout = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    total_cost = db.Column(db.Float, default=0.0)

    def __str__(self) -> str:
        return 'room_id:{0},checkin:{1},checkout:{2},total_cost:{3}'.format(
             self.room_id, self.checkin, self.checkout, self.total_cost)

    def __repr__(self) -> str:
        return self.__str__()

# 插入详单
def add_to_detail(room_id, start_time=datetime.datetime.now(), end_time=0, speed='mid', fee=0,
                  times_used=0, target_temp=25, route=''):
    with app.app_context():
        db.session.add(Detail(room_id=room_id,
                              start_time=start_time,
                              end_time=end_time,
                              speed=speed,
                              fee=fee,
                              times_used=times_used,
                              target_temp=target_temp,
                              route=route))
        db.session.commit()

# 插入账单
def add_to_order(room_id, checkin=datetime.datetime.now(), checkout=datetime.datetime.now(), total_cost=0):
    with app.app_context():
        db.session.add(Order(room_id=room_id,
                             checkin=checkin,
                             checkout=checkout,
                             total_cost=total_cost))
        db.session.commit()

# 酒店经理报表
# class Statistics(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     dateTime = db.Column(db.DateTime, default=datetime.datetime.now)
#     totalNum = db.Column(db.Integer)
#     satisfyNum = db.Column(db.Integer, nullable=True)
#     scheduledNum = db.Column(db.Integer, nullable=True)
#     RDRNum = db.Column(db.Integer, nullable=True)
#     totalFee = db.Column(db.Float, default=0.0)
#
#     def __str__(self) -> str:
#         return 'id:{0},dateTime:{1},totalNum:{2},satisfyNum:{3},scheduledNum:{4},RDRNum:{5},totalFee:{6}'.format(
#             self.id, self.dateTime, self.totalNum, self.satisfyNum, self.scheduledNum, self.RDRNum, self.totalFee)
#
#     def __repr__(self) -> str:
#         return self.__str__()

# 数据库初始化
def db_init():
    with app.app_context():
        db.drop_all()
        db.create_all()

        #账号密码
        db.session.add(User(username='receptionist_1', password='receptionist', type='receptionist'))
        db.session.add(User(username='manager_1', password='manager', type='manager'))
        db.session.add(User(username='administrator_1', password='administrator', type='administrator'))

        db.session.commit()
