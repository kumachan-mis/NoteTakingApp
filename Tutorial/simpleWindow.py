# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget


def simpleWindow():
    app = QApplication(sys.argv)
    # 新しいアプリケーションの土台を作る
    w = QWidget()
    # ウインドウを作る
    w.resize(400, 300);
    # ウィンドウサイズを設定
    w.move(300, 300)
    # ウィンドウの左上端の位置を指定
    w.setWindowTitle("First PyQt5")
    # ウィンドウタイトルを設定
    w.show()
    # 描画

    sys.exit(app.exec_())
    # 正常終了のための処理

if __name__ == '__main__':
    # モジュールとしての使用ではなく、直接スクリプトがmainとして実行されたら
    simpleWindow()
