# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QFont

class TooltipWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('Times', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        button = QPushButton('Buton', self)
        button.setToolTip('This is a <b>QWidget</b> widget')
        # ボタン名と表示するウィンドウを引数に取る
        button.resize(button.sizeHint())
        # sizeHintは理想的なボタンサイズを与える
        button.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Tooltip")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tipwin = TooltipWindow()
    sys.exit(app.exec_())
