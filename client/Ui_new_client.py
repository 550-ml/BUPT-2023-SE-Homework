from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import BodyLabel, ComboBox, CompactDoubleSpinBox, RadioButton, SwitchButton, TitleLabel
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 700)
        self.SwitchButton = SwitchButton(Form)
        self.SwitchButton.setGeometry(QtCore.QRect(450, 140, 91, 22))
        self.SwitchButton.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.SwitchButton.setObjectName("SwitchButton")
        self.SwitchButton.setChecked(False)  # 设置初始状态为False

        self.CompactDoubleSpinBox = CompactDoubleSpinBox(Form)
        self.CompactDoubleSpinBox.setGeometry(QtCore.QRect(450, 220, 79, 33))
        self.CompactDoubleSpinBox.setMinimumSize(QtCore.QSize(79, 33))
        self.CompactDoubleSpinBox.setMaximumSize(QtCore.QSize(1000, 1000))
        self.CompactDoubleSpinBox.setMouseTracking(False)
        self.CompactDoubleSpinBox.setMinimum(16.0)
        self.CompactDoubleSpinBox.setMaximum(34.0)
        self.CompactDoubleSpinBox.setProperty("value", 25.0)
        self.CompactDoubleSpinBox.setObjectName("CompactDoubleSpinBox")
        self.TitleLabel = TitleLabel(Form)
        self.TitleLabel.setGeometry(QtCore.QRect(530, 50, 123, 37))
        self.TitleLabel.setObjectName("TitleLabel")
        self.BodyLabel = BodyLabel(Form)
        self.BodyLabel.setGeometry(QtCore.QRect(460, 110, 61, 21))
        self.BodyLabel.setObjectName("BodyLabel")
        self.BodyLabel_2 = BodyLabel(Form)
        self.BodyLabel_2.setGeometry(QtCore.QRect(460, 190, 63, 19))
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.BodyLabel_3 = BodyLabel(Form)
        self.BodyLabel_3.setGeometry(QtCore.QRect(650, 190, 63, 19))
        self.BodyLabel_3.setObjectName("BodyLabel_3")

        self.RadioButton = RadioButton(Form)
        self.RadioButton.setGeometry(QtCore.QRect(670, 230, 51, 24))
        self.RadioButton.setObjectName("RadioButton")
        self.RadioButton_2 = RadioButton(Form)
        self.RadioButton_2.setGeometry(QtCore.QRect(730, 230, 51, 24))
        self.RadioButton_2.setObjectName("RadioButton_2")
        self.RadioButton_3 = RadioButton(Form)
        self.RadioButton_3.setGeometry(QtCore.QRect(600, 230, 51, 24))
        self.RadioButton_3.setObjectName("RadioButton_3")
        self.RadioButton_3.setChecked(True)

        self.BodyLabel_4 = BodyLabel(Form)
        self.BodyLabel_4.setGeometry(QtCore.QRect(660, 110, 63, 19))
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.BodyLabel_5 = BodyLabel(Form)
        self.BodyLabel_5.setGeometry(QtCore.QRect(660, 140, 63, 19))
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.BodyLabel_6 = BodyLabel(Form)
        self.BodyLabel_6.setGeometry(QtCore.QRect(460, 280, 63, 19))
        self.BodyLabel_6.setObjectName("BodyLabel_6")

        self.ComboBox = ComboBox(Form)
        self.ComboBox.setGeometry(QtCore.QRect(450, 310, 76, 32))
        self.ComboBox.setObjectName("ComboBox")
        self.ComboBox.addItem("制冷")
        self.ComboBox.addItem("制热")

        self.DateTimeLabel = QLabel(Form)
        self.DateTimeLabel.setGeometry(QtCore.QRect(10, 680, 200, 20))
        self.DateTimeLabel.setObjectName("DateTimeLabel")

        self.timer = QTimer(Form)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        self.SwitchButton.checkedChanged.connect(self.on_button_state_changed)
        self.CompactDoubleSpinBox.valueChanged.connect(self.on_spinbox_value_changed)
        self.RadioButton.clicked.connect(self.on_radio_button_clicked)
        self.RadioButton_2.clicked.connect(self.on_radio_button_clicked)
        self.RadioButton_3.clicked.connect(self.on_radio_button_clicked)
        self.ComboBox.currentIndexChanged.connect(self.on_combobox_index_changed)

        self.countdown = 3  # 初始化计数器
        self.timer = QTimer()
        self.timer.timeout.connect(self.finalize_changes)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel.setText(_translate("Form", "空调面板"))
        self.BodyLabel.setText(_translate("Form", "空调开关"))
        self.BodyLabel_2.setText(_translate("Form", "设定温度"))
        self.BodyLabel_3.setText(_translate("Form", "设定风速"))
        self.RadioButton_2.setText(_translate("Form", "高"))
        self.RadioButton.setText(_translate("Form", "中"))
        self.RadioButton_3.setText(_translate("Form", "低"))
        self.BodyLabel_4.setText(_translate("Form", "房间号"))
        self.BodyLabel_5.setText(_translate("Form", "2-233"))
        self.BodyLabel_6.setText(_translate("Form", "设定模式"))
        self.ComboBox.setText(_translate("Form", "制热"))
        self.ComboBox.setText(_translate("Form", "制冷"))

    def updateDateTime(self):
        # 更新 QLabel 显示当前日期和时间
        current_time = QTime.currentTime()
        current_date_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.DateTimeLabel.setText(current_date_time)

    def on_button_state_changed(self,checked):
        if checked:
            self.start_timer()
        else:
            self.start_timer()
        
        #data = self.get_panel_data()
        #self.save_data_to_file(data)

    def on_spinbox_value_changed(self):
        self.start_timer()
        #data = self.get_panel_data()
        #self.save_data_to_file(data)

    def on_radio_button_clicked(self):
        self.start_timer()
        #data = self.get_panel_data()
        #self.save_data_to_file(data)

    def on_combobox_index_changed(self):
        self.start_timer()
        #data = self.get_panel_data()
        #self.save_data_to_file(data)

    def start_timer(self):
        self.countdown = 3  # 重置计数器
        self.timer.start(1000)

    def finalize_changes(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.stop_timer()
            data = self.get_panel_data()
            self.save_data_to_file(data)
    
    def stop_timer(self):
        self.timer.stop()

    def get_panel_data(self):
        import datetime
        selected_radio_text = ""
        if self.RadioButton.isChecked():
            selected_radio_text = "中"
        elif self.RadioButton_2.isChecked():
            selected_radio_text = "高"
        elif self.RadioButton_3.isChecked():
            selected_radio_text = "低"
        # 从面板上所有相关的小部件中收集数据
        panel_data = {
            "空调开关": "On" if self.SwitchButton.isChecked() else "Off",
            "设定温度": self.CompactDoubleSpinBox.value(),
            "风速": selected_radio_text,
            "设定模式": self.ComboBox.currentText(),
            # 根据需要添加更多小部件
        }
        panel_data["更改时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return panel_data
    
    def save_data_to_file(self, data):
        import os
        # 获取当前脚本所在的目录
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # 构建保存文件的完整路径
        file_path = os.path.join(current_directory, "client_operation_data.txt")
        with open(file_path, "a") as file:
            file.write(str(data) + "\n")