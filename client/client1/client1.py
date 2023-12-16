import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTime
from os.path import isfile
import requests
import json
import hashlib
import rsa
import random
from datetime import datetime
import subprocess

from Ui_new_client1 import Ui_Form

class AirConditionerPanel(QWidget, Ui_Form):

    #def start_server(self):
    #    try:
    #        # 启动服务器的命令
    #        server_command = "python server.py"
    #        # 使用subprocess模块启动服务器
    #        subprocess.Popen(server_command, shell=True)
    #    except Exception as e:
    #        print(f"Error starting server: {e}")
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app=QApplication(sys.argv)
    w=AirConditionerPanel()
    w.show()
    app.exec_()
