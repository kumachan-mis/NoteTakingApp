# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class StatusBarWindow(QMainWindow):
    # QMainWindowは各操作バーの配置がすでにレイアウトされている
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('ready')
        self.setWindowTitle('statusBarWindow')
        self.setGeometry(100, 100, 400, 300)
        self.show()

if __name__  == '__main__':
    app = QApplication(sys.argv)
    status = StatusBarWindow()
    sys.exit(app.exec_())