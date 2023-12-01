import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime
from os.path import isfile

class AirConditionerPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.power_on = False
        self.temperature = 25  # 初始温度
        self.fan_speeds = ['低', '中', '高']
        self.current_fan_speed = 0  # 初始风速为低
        self.modes = ['制冷', '制热']
        self.current_mode = 0  # 初始模式为制冷

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.record_event)
        self.countdown = 0

        self.log_file = self.get_log_file()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.temperature_label = QLabel(f"温度: {self.temperature}°", self)
        layout.addWidget(self.temperature_label)

        self.fan_speed_label = QLabel(f"风速: {self.fan_speeds[self.current_fan_speed]}", self)
        layout.addWidget(self.fan_speed_label)

        self.mode_label = QLabel(f"模式: {self.modes[self.current_mode]}", self)
        layout.addWidget(self.mode_label)

        power_button = QPushButton('开关', self)
        power_button.clicked.connect(self.toggle_power)
        layout.addWidget(power_button)

        increase_temp_button = QPushButton('▲', self)
        increase_temp_button.clicked.connect(lambda: self.adjust_temperature(0.5))
        layout.addWidget(increase_temp_button)

        decrease_temp_button = QPushButton('▼', self)
        decrease_temp_button.clicked.connect(lambda: self.adjust_temperature(-0.5))
        layout.addWidget(decrease_temp_button)

        fan_speed_button = QPushButton('风速调节', self)
        fan_speed_button.clicked.connect(self.adjust_fan_speed)
        layout.addWidget(fan_speed_button)

        mode_button = QPushButton('模式调节', self)
        mode_button.clicked.connect(self.toggle_mode)
        layout.addWidget(mode_button)

        #shutdown_button = QPushButton('关闭', self)
        #shutdown_button.clicked.connect(self.shutdown)
        #layout.addWidget(shutdown_button)

        self.log_display = QTextEdit(self)
        layout.addWidget(self.log_display)

        self.setLayout(layout)
        self.setWindowTitle('空调面板')
        self.setGeometry(300, 300, 500, 700)
        self.show()

    def toggle_power(self):
        if not self.power_on:
            self.power_on = True
            self.start_timer()
            self.log_event("空调开机")
        else:
            self.stop_timer()
            self.power_on = False
            self.log_event(f"空调关闭 - 最后记录 - "
                           f"温度: {self.temperature}°, 风速: {self.fan_speeds[self.current_fan_speed]}, "
                           f"模式: {self.modes[self.current_mode]}")

    def adjust_temperature(self, change):
        if self.power_on:
            if 16 <= self.temperature + change <= 30:
                self.temperature += change
                self.temperature_label.setText(f"温度: {self.temperature}°")
                self.start_timer()

    def adjust_fan_speed(self):
        if self.power_on:
            self.current_fan_speed = (self.current_fan_speed + 1) % len(self.fan_speeds)
            self.fan_speed_label.setText(f"风速: {self.fan_speeds[self.current_fan_speed]}")
            self.start_timer()

    def toggle_mode(self):
        if self.power_on:
            self.current_mode = (self.current_mode + 1) % len(self.modes)
            self.mode_label.setText(f"模式: {self.modes[self.current_mode]}")
            self.start_timer()

    def shutdown(self):
        if self.power_on:
            self.stop_timer()
            self.power_on = False
            self.log_event(f"空调关闭 - 最后记录 - "
                           f"温度: {self.temperature}°, 风速: {self.fan_speeds[self.current_fan_speed]}, "
                           f"模式: {self.modes[self.current_mode]}")

    def start_timer(self):
        self.countdown = 3
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def record_event(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.stop_timer()
            self.log_event(f"正在记录 - "
                           f"温度: {self.temperature}°, 风速: {self.fan_speeds[self.current_fan_speed]}, "
                           f"模式: {self.modes[self.current_mode]}")

    def log_event(self, event):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        log_entry = f"{timestamp} - {event}\n"
        self.log_display.append(log_entry)
        with open(self.log_file, 'a') as file:
            file.write(log_entry)

    def get_log_file(self):
        timestamp = QDateTime.currentDateTime().toString("yyyyMMddhhmmss")
        log_file = "time_log.txt"
        return log_file


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AirConditionerPanel()
    sys.exit(app.exec_())
