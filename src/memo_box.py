#!/usr/local/bin/python3
from PyQt5.QtWidgets import (QWidget, QDialog, QLineEdit, QTextEdit, QComboBox, QLabel, QPushButton,
                             QScrollArea, QSplitter, QVBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
import read_write


class MemoBox(QWidget):
    deleted = pyqtSignal(QDialog)
    jump = pyqtSignal(int)

    def __init__(self, max_page, related_page):
        super().__init__()
        self.__max_page = max_page
        self.__title_area = QLineEdit()
        self.__memo_area = QTextEdit()

        self.__related_page_area = QComboBox()
        self.__init_combo(related_page)
        self.__init_memo_box()

    def __init_combo(self, related_page):
        self.__related_page_area.setEditable(False)

        for page_num in range(1, self.__max_page + 1):
            self.__related_page_area.addItem(str(page_num))

        self.__related_page_area.setCurrentIndex(related_page)

    def __init_memo_box(self):
        grid = QGridLayout()
        label_about = QLabel("テーマ")
        label_page = QLabel("ページ")
        jump_button = QPushButton("ジャンプ")
        jump_button.setAutoDefault(False)
        jump_button.clicked.connect(self.__jump_pressed)
        delete_button = QPushButton("削除")
        delete_button.setAutoDefault(False)
        delete_button.clicked.connect(self.__delete)

        grid.addWidget(label_about,              0, 0, 1,  1)
        grid.addWidget(self.__title_area,        0, 1, 1,  5)
        grid.addWidget(label_page,               0, 6, 1,  1)
        grid.addWidget(self.__related_page_area, 0, 7, 1,  1)
        grid.addWidget(jump_button,              0, 8, 1,  1)
        grid.addWidget(delete_button,            0, 9, 1,  1)
        grid.addWidget(self.__memo_area,         1, 0, 7, 10)

        self.setLayout(grid)

    def __delete(self):
        self.deleted.emit(self)
        self.deleteLater()

    def __jump_pressed(self):
        self.jump.emit(self.__related_page_area.currentIndex())

    def current_related_page(self):
        return self.__related_page_area.currentIndex()

    def read_memo_box_info(self, file):
        self.__title_area.setText(file.readline()[:-1])
        self.__related_page_area.setCurrentIndex(int(file.readline()[:-1]))
        read_write.reader(file, self.__memo_area)

    def write_memo_box_info(self, file):
        file.write(self.__title_area.text() + '\n')
        file.write(str(self.__related_page_area.currentIndex()) + '\n')
        read_write.writer(file, self.__memo_area)


class MemoBoxGroup(QScrollArea):
    def __init__(self, max_page, jump_method):
        super().__init__()
        self.__max_page = max_page
        self.__jump_method = jump_method
        self.__memo_boxes = []
        self.__scroll_splitter = QSplitter(Qt.Vertical)

        self.__set_layout()

    def __set_layout(self):
        self.setWidgetResizable(True)
        inner = QWidget()
        v_box = QVBoxLayout(inner)
        v_box.addWidget(self.__scroll_splitter)
        inner.setLayout(v_box)
        self.setWidget(inner)

    def add_new_box(self):
        if not self.__memo_boxes:
            related_page = 0
        else:
            related_page = self.__memo_boxes[-1].current_related_page()

        box = MemoBox(self.__max_page, related_page)
        box.deleted.connect(self.__memo_boxes.remove)
        box.jump.connect(self.__jump_method)

        self.__scroll_splitter.addWidget(box)
        self.__memo_boxes.append(box)

    def set_default(self):
        for index in range(3):
            self.add_new_box()

    def read_memo_box_group_info(self, file):
        memo_box_num = int(str(file.readline()))
        for index in range(memo_box_num):
            self.add_new_box()
            self.__memo_boxes[index].read_memo_box_info(file)

    def write_memo_box_group_info(self, file):
        file.write(str(len(self.__memo_boxes)) + '\n')
        for memo_box in self.__memo_boxes:
            memo_box.write_memo_box_info(file)