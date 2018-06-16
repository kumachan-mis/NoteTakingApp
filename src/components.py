#!/usr/local/bin/python3
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import pyqtSignal


class MemoBox(QWidget):
    maxPage = 1
    deleted = pyqtSignal('QWidget')

    @staticmethod
    def set_max_page(max_page):
        MemoBox.maxPage = max_page

    def __init__(self, relatedPage):
        super().__init__()

        self.__comboBox = QComboBox()

        self.__init_combo(relatedPage)
        self.__init_memo_box()

    def __init_combo(self, relatedPage):
        self.__comboBox.setEditable(False)

        for page_num in range(1, MemoBox.maxPage + 1):
            self.__comboBox.addItem(str(page_num))

        self.__comboBox.setCurrentIndex(relatedPage - 1)

    def __init_memo_box(self):
        grid = QGridLayout()
        labelAbout = QLabel("テーマ名")
        titleArea = QLineEdit()
        deleteButton = QPushButton("削除")
        memoArea = QTextEdit()

        deleteButton.clicked.connect(self.__delete)

        grid.addWidget(labelAbout,      0, 0, 1, 1)
        grid.addWidget(titleArea,       0, 1, 1, 5)
        grid.addWidget(self.__comboBox, 0, 6, 1, 1)
        grid.addWidget(deleteButton,    0, 7, 1, 1)
        grid.addWidget(memoArea,        1, 0, 6, 8)

        self.setLayout(grid)

    def __delete(self):
        self.deleted.emit(self)
        self.deleteLater()

    def current_related_page(self) -> int:
        return self.__comboBox.currentIndex() + 1