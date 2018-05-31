# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class MessageBoxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.move(300, 300)
        self.resize(500, 400)
        self.setWindowTitle("messageBox")
        self.show()

    def closeEvent(self, event): # QWidgetクラスから継承. ウィンドウを閉じようとした時に呼ばれる
        getReply = QMessageBox.question(self, 'check', 'ウィンドウを閉じていいですか？', # ユーザの選択を促すメソッド
                               QMessageBox.Yes | QMessageBox.No, # 選択ボタンの一覧
                               QMessageBox.No) # デフォルトの選択

        if getReply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    messageBox = MessageBoxWindow()
    sys.exit(app.exec_())