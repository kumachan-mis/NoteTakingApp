#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSplitter, QScrollArea
from PyQt5.QtCore import Qt
import streaming
from components import *


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.__memo_boxes = []
        # 仮置き(ここから)
        self.__doc_area = QTextEdit()
        # 仮置き(ここまで)
        self.__stream_area = QTextEdit()
        self.__gen_memo_box = QPushButton()
        self.__th = streaming.StreamingThread()

        MemoBox.set_max_page(10)
        self.__init_ui()
        self.__run_streaming_thread()

    def __init_ui(self):
        self.setWindowTitle("Streaming Print")

        screen = QApplication.desktop()
        self.resize(9*screen.width()/10, 4*screen.height()/5)
        self.__center()

        self.__set_components()
        self.__set_window_layout()

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __set_components(self):
        # 仮置き(ここから)
        self.__doc_area.setReadOnly(True)
        self.__doc_area.append("ここに講義資料を表示")
        # 仮置き(ここまで)

        self.__gen_memo_box.setText("新規ボックスを作成")
        self.__gen_memo_box.clicked.connect(self.__generate_new_box)

        self.__stream_area.setReadOnly(False)
        self.__stream_area.append("[音声認識結果]")

    def __set_window_layout(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        v_box = QVBoxLayout(inner)
        self.__scroll_splitter = QSplitter(Qt.Vertical)
        v_box.addWidget(self.__scroll_splitter)
        inner.setLayout(v_box)
        scroll.setWidget(inner)

        memo_widget = QSplitter(Qt.Horizontal)
        memo_widget.addWidget(scroll)
        memo_widget.addWidget(self.__doc_area)
        memo_widget.setSizes([self.width() / 3, 2 * self.width() / 3])

        h_box = QHBoxLayout()
        h_box.addWidget(self.__gen_memo_box)
        h_box.addWidget(self.__stream_area)
        stream_widget = QWidget()
        stream_widget.setLayout(h_box)

        v_box = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(memo_widget)
        splitter.addWidget(stream_widget)
        splitter.setSizes([4 * self.height() / 5, self.height() / 5])
        v_box.addWidget(splitter)

        self.setLayout(v_box)

    def __run_streaming_thread(self):
        self.__th.streaming_result.connect(self.__stream_area.append)
        self.__th.start()

    def __generate_new_box(self):
        if not self.__memo_boxes:
            related_page = 1
        else:
            related_page = self.__memo_boxes[-1].current_related_page()

        box = MemoBox(related_page)
        box.deleted.connect(self.remove_from_list)
        self.__scroll_splitter.addWidget(box)
        self.__memo_boxes.append(box)

    def remove_from_list(self, deleted):
        self.__memo_boxes.remove(deleted)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())