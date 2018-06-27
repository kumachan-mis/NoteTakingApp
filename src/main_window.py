#!/usr/local/bin/python3
from sys import exit
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from streaming import StreamingThread
from memo_box import MemoBox
from doc_viewer import DocumentViewer

my_extension = '.soundnote'


class UserInterface(QDialog):
    def __init__(self, is_new, pdf_path = '', file_path = ''):
        super().__init__()
        screen = QApplication.desktop()
        self.resize(9 * screen.width() / 10, 4 * screen.height() / 5)
        self.__doc_area_size = QSize(3 * self.width() / 5, 4 * self.height() / 5)

        self.__gen_memo_box = QPushButton()
        self.__filename_area = QLineEdit()
        self.__save = QPushButton()
        self.__memo_boxes = []
        self.__scroll_splitter = QSplitter(Qt.Vertical)

        self.__stream_area = QTextEdit()
        self.__th = StreamingThread()
        self.__run_streaming_thread()

        self.setWindowTitle("サウンドノート")
        self.__center()
        self.__set_components()
        if is_new:
            self.__new_note(pdf_path)
        else:
            self.__open_saved_file(file_path)
        self.__set_window_layout()

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __set_components(self):
        self.__gen_memo_box.setText("新規ボックスを作成")
        self.__gen_memo_box.clicked.connect(self.__generate_new_box)
        self.__save.setText("保存")
        self.__save.clicked.connect(self.__save_as_file)
        self.__stream_area.setReadOnly(False)
        self.__stream_area.append("[音声認識結果]")

    def __set_window_layout(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        v_box = QVBoxLayout(inner)
        v_box.addWidget(self.__scroll_splitter)
        inner.setLayout(v_box)
        scroll.setWidget(inner)

        memo_widget = QSplitter(Qt.Horizontal)
        memo_widget.addWidget(scroll)
        memo_widget.addWidget(self.__doc_area)
        memo_widget.setSizes([self.width() - self.__doc_area_size.width(), self.__doc_area_size.width()])

        h_box = QHBoxLayout()
        h_box.addWidget(self.__gen_memo_box)
        h_box.addWidget(self.__save)
        h_box.addWidget(self.__stream_area)
        stream_widget = QWidget()
        stream_widget.setLayout(h_box)

        v_box = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(memo_widget)
        splitter.addWidget(stream_widget)
        splitter.setSizes([self.__doc_area_size.height(), self.height() - self.__doc_area_size.height()])
        v_box.addWidget(splitter)

        self.setLayout(v_box)

    def __run_streaming_thread(self):
        self.__th.streaming_result.connect(self.__stream_area.append)
        self.__th.start()

    def __generate_new_box(self):
        if not self.__memo_boxes:
            related_page = 0
        else:
            related_page = self.__memo_boxes[-1].current_related_page()

        box = MemoBox(related_page)
        box.deleted.connect(self.__remove_from_list)
        box.jump.connect(self.__doc_area.turn_page)

        self.__scroll_splitter.addWidget(box)
        self.__memo_boxes.append(box)

    def __remove_from_list(self, deleted):
        self.__memo_boxes.remove(deleted)

    def __new_note(self, pdf_path):
        self.__doc_area = DocumentViewer(pdf_path, self.__doc_area_size.width())
        MemoBox.set_max_page(self.__doc_area.max_page)
        for index in range(3):
            self.__generate_new_box()

    def __open_saved_file(self, file_path):

        with open(file_path, 'r') as file:
            self.__doc_area = DocumentViewer(file.readline()[:-1], self.__doc_area_size.width())
            MemoBox.set_max_page(self.__doc_area.max_page)

            memo_box_num = int(str(file.readline()))
            for index in range(memo_box_num):
                self.__generate_new_box()
                self.__memo_boxes[index].read_memo_box_info(file)

    def __save_as_file(self):
        file_path = QFileDialog.getSaveFileName(None, 'Save File',
                                                path.expanduser('~') + '/Desktop', '*' + my_extension)[0]
        if file_path == '':
            return

        with open(file_path, 'w') as file:
            self.__doc_area.write_pdf_path(file)

            file.write(str(len(self.__memo_boxes)) + '\n')
            for memo_box in self.__memo_boxes:
                memo_box.write_memo_box_info(file)

    def closeEvent(self, event):
        get_reply = QMessageBox.question(self, 'close', 'ウィンドウを閉じていいですか？',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

        if get_reply == QMessageBox.Yes:
            event.accept()
            exit()
        else:
            event.ignore()