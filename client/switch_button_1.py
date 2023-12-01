import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication

class SwitchButton(QWidget):
    switch_toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._switch_on = False
        self._switch_color = QColor(0, 255, 0)
        self._switch_rect = QRect(0, 0, 30, 30)
        self._switch_animation = QPropertyAnimation(self, b"switchRect", self)
        self._switch_animation.setDuration(300)
        self._switch_animation.setStartValue(QRect(0, 0, 30, 30))
        self._switch_animation.setEndValue(QRect(30, 0, 30, 30))
        self._switch_animation.finished.connect(self._on_animation_finished)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRoundedRect(self.rect(), 15, 15)

        painter.setBrush(QBrush(self._switch_color))
        painter.drawRoundedRect(self._switch_rect, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._switch_animation.setDirection(QPropertyAnimation.Forward if not self._switch_on else QPropertyAnimation.Backward)
            self._switch_animation.start()

    def _on_animation_finished(self):
        self._switch_on = not self._switch_on
        if self._switch_on:
            self._switch_color = QColor(0, 255, 0)  # 红色
        else:
            self._switch_color = QColor(255, 0, 0)  # 绿色
        self.switch_toggled.emit(self._switch_on)

    @pyqtProperty(QRect)
    def switchRect(self):
        return self._switch_rect

    @switchRect.setter
    def switchRect(self, rect):
        self._switch_rect = rect
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    switch_button = SwitchButton()
    switch_button.show()
    sys.exit(app.exec_())
