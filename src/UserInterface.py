#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QSplitter, QTextEdit
from PyQt5.QtCore import Qt
import streaming


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__streamArea = QTextEdit()
        self.__editArea = QTextEdit()
        self.__splitter = QSplitter(Qt.Vertical)
        self.__vBox = QVBoxLayout()

        self.__th = streaming.StreamingThread()

        self.__init_ui()
        self.__run_streaming_thread()

    def __init_ui(self):
        self.setWindowTitle("Streaming Print")

        screen = QApplication.desktop()
        self.resize(4*screen.width()/5, 4*screen.height()/5)
        self.__center()

        self.__streamArea.setReadOnly(True)
        self.__streamArea.append("ここに音声認識結果を表示")

        self.__editArea.setReadOnly(False)
        self.__editArea.append("ここにメモ")

        self.__splitter.addWidget(self.__editArea)
        self.__splitter.addWidget(self.__streamArea)
        self.__vBox.addWidget(self.__splitter)
        self.__splitter.moveSplitter(self.height()/2 , 1)

        widget = QWidget()
        widget.setLayout(self.__vBox)
        self.setCentralWidget(widget)

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __run_streaming_thread(self):
        self.__th.streaming_result.connect(self.__show_streaming_result)
        self.__th.start()

    def __show_streaming_result(self, result):
        self.__streamArea.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())