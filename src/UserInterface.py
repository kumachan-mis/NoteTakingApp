#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import *
import streaming


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.run_streaming_thread()

    def init_ui(self):
        self.setWindowTitle("Streaming Print")
        self.resize(800, 600)
        self.center()

        self.streamArea = QTextEdit(self)
        self.streamArea.setReadOnly(True)
        self.streamArea.append("音声認識結果を画面に表示します")

        self.editArea = QTextEdit(self)
        self.editArea.setReadOnly(False)
        self.editArea.append("ここにメモ")

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.streamArea)
        self.hBox.addWidget(self.editArea)

        self.vBox = QVBoxLayout()
        self.vBox.addLayout(self.hBox)

        self.widget = QWidget()
        self.widget.setLayout(self.vBox)
        self.setCentralWidget(self.widget)

    def center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def run_streaming_thread(self):
        self.th = streaming.StreamingThread()
        self.th.streaming_result.connect(self.show_streaming_result)
        self.th.start()

    def show_streaming_result(self, result):
        self.streamArea.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())