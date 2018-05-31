# !/usr/local/bin/python3
# -*- coding utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu


class SubmenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')

        impMenu = QMenu('Import", self', self)
        impMail = QAction('Import Mail', self)
        impMenu.addAction(impMail)

        newAct = QAction('New', self)

        fileMenu.addMenu(impMenu)
        fileMenu.addAction(newAct)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    submenu = SubmenuWindow()
    sys.exit(app.exec_())