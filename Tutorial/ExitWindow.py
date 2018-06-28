# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication


class ExitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle("exitWindow")
        exit = QPushButton('exit', self)
        exit.resize(exit.sizeHint())
        exit.move(100, 200)
        exit.clicked.connect(QCoreApplication.instance().quit)
        exit.show()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exit = ExitWindow()
    sys.exit(app.exec_())