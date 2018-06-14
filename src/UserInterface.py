#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSplitter, QScrollArea, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
import streaming


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__memoArea = QTextEdit()
        self.__streamArea = QTextEdit()
        self.__genTextBox = QPushButton()
        self.__th = streaming.StreamingThread()

        self.__init_ui()
        self.__run_streaming_thread()

    def __init_ui(self):
        self.setWindowTitle("Streaming Print")

        screen = QApplication.desktop()
        self.resize(4*screen.width()/5, 4*screen.height()/5)
        self.__center()

        self.__set_components()
        self.__set_window_layout()

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __set_components(self):
        self.__memoArea.setReadOnly(False)
        self.__memoArea.append("ここにメモ")

        self.__genTextBox.setText("新規ボックスを作成")
        self.__genTextBox.clicked.connect(self.__generate_new_box)

        self.__streamArea.setReadOnly(False)
        self.__streamArea.append("ここに音声認識結果を表示")

    def __set_window_layout(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        vBox = QVBoxLayout(inner)
        self.__scroll_splitter = QSplitter(Qt.Vertical)
        vBox.addWidget(self.__scroll_splitter)
        inner.setLayout(vBox)
        scroll.setWidget(inner)

        hBox = QHBoxLayout()
        hBox.addWidget(scroll)
        hBox.addWidget(self.__memoArea)
        memo_widget = QWidget()
        memo_widget.setLayout(hBox)

        hBox = QHBoxLayout()
        hBox.addWidget(self.__genTextBox)
        hBox.addWidget(self.__streamArea)
        stream_widget = QWidget()
        stream_widget.setLayout(hBox)

        vBox = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(memo_widget)
        splitter.addWidget(stream_widget)
        splitter.moveSplitter(self.height() / 2, 1)
        vBox.addWidget(splitter)

        widget = QWidget()
        widget.setLayout(vBox)
        self.setCentralWidget(widget)

    def __run_streaming_thread(self):
        self.__th.streaming_result.connect(self.__streamArea.setText)
        self.__th.start()

    def __generate_new_box(self):
        self.__scroll_splitter.addWidget(QTextEdit())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())