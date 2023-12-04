from app import *

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(80), unique=True, primary_key=True)
    password = db.Column(db.String(80), nullable=True)
    type = db.Column(db.Enum('receptionist', 'manager', 'administrator'))


class Detail(db.Model):
    room_id = db.Column(db.String, nullable=True, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    speed = db.Column(db.Enum("HIGH", "MID", "LOW"))
    fee = db.Column(db.Float, default=0.0)
    times_used = db.Column(db.Integer, nullable=True)

    def __str__(self) -> str:
        return 'room_id:{0},start_time:{1},end_time:{2},speed:{3},fee:{4},times_used:{5}'.format(
             self.room_id, self.start_time, self.end_time, self.speed, self.fee, self.times_used)

    def __repr__(self) -> str:
        return self.__str__()


class Order(db.Model):
    room_id = db.Column(db.String, primary_key=True)
    checkin = db.Column(db.DateTime, default=datetime.datetime.now)
    checkout = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    total_cost = db.Column(db.Float, default=0.0)

    def __str__(self) -> str:
        return 'room_id:{0},checkin:{1},checkout:{2},total_cost:{3}'.format(
             self.room_id, self.checkin, self.checkout, self.total_cost)

    def __repr__(self) -> str:
        return self.__str__()


def add_to_detail(room_id, star_time=datetime.datetime.now, end_time=datetime.datetime.now, speed='mid', fee=0,
                  time_used=0):
    with app.app_context():
        db.session.add(Detail(room_id=room_id,
                              star_time=star_time,
                              end_time=end_time,
                              speed=speed,
                              fee=fee,
                              time_used=time_used))
        db.session.commit()


def add_to_order(room_id, checkin=datetime.datetime.now, checkout=datetime.datetime.now, total_cost=0):
    with app.app_context():
        db.session.add(Order(room_id=room_id,
                             checkin=checkin,
                             checkout=checkout,
                             total_cost=total_cost))
        db.session.commit()

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


def db_init():
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.commit()
