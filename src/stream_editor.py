#!/usr/local/bin/python3
from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit, QSplitter, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
import streaming_controller
import read_write


class StreamingEditor(QWidget):
    current_page_request = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__final_result = None
        self.__th = streaming_controller.StreamingThread()
        self.__final_result_viewer = QTextEdit()
        self.__all_result_viewer = QLineEdit()

        self.__set_layout()

    def __set_layout(self):
        v_box = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        self.__final_result_viewer.setReadOnly(False)
        self.__final_result_viewer.append("[音声認識結果の最終文]")
        self.__all_result_viewer.setReadOnly(False)

        splitter.addWidget(self.__final_result_viewer)
        splitter.addWidget(self.__all_result_viewer)

        v_box.addWidget(splitter)
        self.setLayout(v_box)

    def run_streaming_thread(self):
        self.__th.final_result.connect(self.__set_final_result)
        self.__th.streaming_result.connect(self.__all_result_viewer.setText)
        self.__th.start()

    def __set_final_result(self, final_result):
        self.__final_result = final_result
        self.current_page_request.emit()

    def print_final_result(self, current_page):
        self.__final_result_viewer.append(self.__final_result + '(' + str(current_page) + ')')

    def read_final_result(self, file):
        read_write.reader(file, self.__final_result_viewer)

    def write_final_result(self, file):
        read_write.writer(file, self.__final_result_viewer)