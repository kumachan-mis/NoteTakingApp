# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class CheckMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        menuBar = self.menuBar()
        viewMenu = menuBar.addMenu('View')

        viewStartAct = QAction('View StatusBar', self, checkable=True)
        viewStartAct.setStatusTip('View StatusBar')
        viewStartAct.setChecked(True)
        viewStartAct.triggered.connect(self.toggleMenu)

        viewMenu.addAction(viewStartAct)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Checkmenu Window')
        self.show()

    def toggleMenu(self, showOrHide):
        if showOrHide:
            self.statusber.show()
        else:
            self.statusbar.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    checkMenu = CheckMenu()
    sys.exit(app.exec_())