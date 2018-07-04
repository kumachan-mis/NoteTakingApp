#!/usr/local/bin/python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from text_edit_read_write import reader, writer


class MemoBox(QWidget):
    __max_page = 1
    deleted = pyqtSignal(QDialog)
    jump = pyqtSignal(int)

    @staticmethod
    def set_max_page(max_page):
        MemoBox.__max_page = max_page

    def __init__(self, related_page):
        super().__init__()
        self.__title_area = QLineEdit()
        self.__memo_area = QTextEdit()

        self.__related_page_area = QComboBox()
        self.__init_combo(related_page)
        self.__init_memo_box()

    def __init_combo(self, related_page):
        self.__related_page_area.setEditable(False)

        for page_num in range(1, MemoBox.__max_page + 1):
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
        reader(file, self.__memo_area)

    def write_memo_box_info(self, file):
        file.write(self.__title_area.text() + '\n')
        file.write(str(self.__related_page_area.currentIndex()) + '\n')
        writer(file, self.__memo_area)