# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class IconWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('./tutorialmedia/sampleicon1.png'))
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    iconwin = IconWindow()
    sys.exit(app.exec_())