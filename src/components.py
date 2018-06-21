#!/usr/local/bin/python3
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import pyqtSignal


class MemoBox(QWidget):
    max_page = 1
    deleted = pyqtSignal(QWidget)

    @staticmethod
    def set_max_page(max_page):
        MemoBox.max_page = max_page

    def __init__(self, related_page):
        super().__init__()
        self.__combo_box = QComboBox()
        self.__init_combo(related_page)
        self.__init_memo_box()

    def __init_combo(self, related_page):
        self.__combo_box.setEditable(False)

        for page_num in range(1, MemoBox.max_page + 1):
            self.__combo_box.addItem(str(page_num))

        self.__combo_box.setCurrentIndex(related_page - 1)

    def __init_memo_box(self):
        grid = QGridLayout()
        label_about = QLabel("テーマ")
        title_area = QLineEdit()
        label_page = QLabel("ページ")
        delete_button = QPushButton("削除")
        memo_area = QTextEdit()

        delete_button.clicked.connect(self.__delete)

        grid.addWidget(label_about,      0, 0, 1, 1)
        grid.addWidget(title_area,       0, 1, 1, 5)
        grid.addWidget(label_page,       0, 6, 1, 1)
        grid.addWidget(self.__combo_box, 0, 7, 1, 1)
        grid.addWidget(delete_button,    0, 8, 1, 1)
        grid.addWidget(memo_area,        1, 0, 7, 9)

        self.setLayout(grid)

    def __delete(self):
        self.deleted.emit(self)
        self.deleteLater()

    def current_related_page(self):
        return self.__combo_box.currentIndex() + 1