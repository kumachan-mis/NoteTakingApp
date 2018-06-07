#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit
import streaming


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.textArea = QTextEdit(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Streaming Print")
        self.setGeometry(200, 100, 400, 300)

        self.widget = QWidget()

        # self.textArea.setReadOnly(True)
        self.textArea.append("音声認識結果を画面に表示します。")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textArea)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()

    streaming.do_streaming(ui.textArea)
    sys.exit(app.exec_())