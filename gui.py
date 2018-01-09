from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QPushButton, QWidget
import sys


class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 180, 310)
        self.setWindowTitle('Display')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        text = 'ATTACKERS:\n' \
               '    --\n' \
               '    --\n' \
               '    --\n' \
               'DEFENDERS:\n' \
               '    --\n' \
               '    --\n' \
               '    --'
        self._label = QLabel(text, self)
        self._label.setFont(QFont('bebas neue', 24, QFont.Bold))
        self._label.setStyleSheet('color: white')

        self._offset = None

        self.show()

    def update_text(self, text):
        self._label.setText(text)

    def mousePressEvent(self, event):
        self._offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            x = event.globalX()
            y = event.globalY()
            x_w = self._offset.x()
            y_w = self._offset.y()
            self.move(x - x_w, y - y_w)


class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(550, 350, 100, 100)
        self.setWindowTitle('Control')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        grid = QGridLayout()
        self.setLayout(grid)

        self.button_attacker = QPushButton('Next Attacker', self)
        self.button_attacker.clicked.connect(self.handle_button_attacker)
        self.button_attacker.setFont((QFont('bebas neue', 24, QFont.Bold)))
        self.button_attacker.setStyleSheet('QPushButton {background-color: rgba(255, 255, 255, 10); color: white;}')

        self.button_defender = QPushButton('Next Defender', self)
        self.button_defender.clicked.connect(self.handle_button_defender)
        self.button_defender.setFont((QFont('bebas neue', 24, QFont.Bold)))
        self.button_defender.setStyleSheet('QPushButton {background-color: rgba(255, 255, 255, 10); color: white;}')

        grid.addWidget(self.button_attacker, 0, 0)
        grid.addWidget(self.button_defender, 1, 0)

        self._offset = None

        self.show()

    def handle_button_attacker(self):
        pass  # overridden in run.py

    def handle_button_defender(self):
        pass  # overridden in run.py

    def mousePressEvent(self, event):
        self._offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            x = event.globalX()
            y = event.globalY()
            x_w = self._offset.x()
            y_w = self._offset.y()
            self.move(x - x_w, y - y_w)


class GUI:
    def __init__(self, button_attacker_fn, button_defender_fn):
        self.app = QApplication(sys.argv)
        ControlWindow.button_attacker = button_attacker_fn
        ControlWindow.button_defender = button_defender_fn
        self.display_window = DisplayWindow()
        self.control_window = ControlWindow()
