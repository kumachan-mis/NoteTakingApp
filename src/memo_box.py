#!/usr/local/bin/python3
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import pyqtSignal


class MemoBox(QDialog):
    __max_page = 1
    deleted = pyqtSignal(QDialog)
    jump = pyqtSignal(int)

    @staticmethod
    def set_max_page(max_page):
        MemoBox.__max_page = max_page

    def __init__(self, related_page):
        super().__init__()
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
        title_area = QLineEdit()
        label_page = QLabel("ページ")
        delete_button = QPushButton("削除")
        jump_button = QPushButton("ジャンプ")
        memo_area = QTextEdit()

        delete_button.clicked.connect(self.__delete)
        jump_button.clicked.connect(self.__jump_pressed)

        grid.addWidget(label_about,              0, 0, 1,  1)
        grid.addWidget(title_area,               0, 1, 1,  5)
        grid.addWidget(label_page,               0, 6, 1,  1)
        grid.addWidget(self.__related_page_area, 0, 7, 1,  1)
        grid.addWidget(jump_button,              0, 8, 1,  1)
        grid.addWidget(delete_button,            0, 9, 1,  1)
        grid.addWidget(memo_area,                1, 0, 7, 10)

        self.setLayout(grid)

    def __delete(self):
        self.deleted.emit(self)
        self.deleteLater()

    def __jump_pressed(self):
        self.jump.emit(self.__related_page_area.currentIndex())

    def current_related_page(self):
        return self.__related_page_area.currentIndex()