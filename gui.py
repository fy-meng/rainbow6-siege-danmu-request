from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QPushButton, QWidget
import sys


class CombinedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 180, 310)
        self.setWindowTitle('Display')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._text_attackers = '    --\n' \
                               '    --\n' \
                               '    --'
        self._text_defenders = '    --\n' \
                               '    --\n' \
                               '    --'

        grid = QGridLayout()
        self.setLayout(grid)

        self._buttons_attacker = QPushButton('ATTACKERS:', self)
        self._buttons_attacker.clicked.connect(self.handle_button_attacker)
        self._buttons_attacker.setFont((QFont('bebas neue', 24, QFont.Bold)))
        self._buttons_attacker.setStyleSheet('QPushButton {background-color: rgba(255, 255, 255, 10); color: white;}')

        self._labels_attacker = QLabel(self._text_attackers, self)
        self._labels_attacker.setFont(QFont('bebas neue', 24, QFont.Bold))
        self._labels_attacker.setStyleSheet('color: white')

        self._buttons_defender = QPushButton('DEFENDERS:', self)
        self._buttons_defender.clicked.connect(self.handle_button_defender)
        self._buttons_defender.setFont((QFont('bebas neue', 24, QFont.Bold)))
        self._buttons_defender.setStyleSheet('QPushButton {background-color: rgba(255, 255, 255, 10); color: white;}')

        self._labels_defender = QLabel(self._text_defenders, self)
        self._labels_defender.setFont(QFont('bebas neue', 24, QFont.Bold))
        self._labels_defender.setStyleSheet('color: white')

        grid.addWidget(self._buttons_attacker, 0, 0)
        grid.addWidget(self._labels_attacker, 1, 0)
        grid.addWidget(self._buttons_defender, 2, 0)
        grid.addWidget(self._labels_defender, 3, 0)

        self._offset = None

        self.show()

    def handle_button_attacker(self):
        pass  # overridden in run.py

    def handle_button_defender(self):
        pass  # overridden in run.py

    def update_text(self, text):
        self._labels_attacker.setText(text[0])
        self._labels_defender.setText(text[1])

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
        # TODO： implement button handler
        CombinedWindow.button_attacker = button_attacker_fn
        CombinedWindow.button_defender = button_defender_fn
        self.combined_window = CombinedWindow()
