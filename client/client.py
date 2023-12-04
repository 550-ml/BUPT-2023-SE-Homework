import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime
from os.path import isfile
import requests
import json
import hashlib
import rsa
import random
from datetime import datetime

from Ui_new_client import Ui_Form

class AirConditionerPanel(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app=QApplication(sys.argv)
    w=AirConditionerPanel()
    w.show()
    app.exec_()