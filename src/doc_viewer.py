#!/usr/local/bin/python3
import os
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import glob


class DocumentViewer(QWidget):
    current_page_response = pyqtSignal(int)

    def __init__(self, path_data, viewer_width):
        super().__init__()

        self.__path_data = path_data
        self.__doc_image_tuple = ()
        self.__current_page = 0
        self.max_page = 0
        self.__scroll = QScrollArea()
        self.__scroll.setWidgetResizable(True)
        self.__current_page_label = QLabel()

        self.__get_doc_image(viewer_width)
        self.__set_layout()

    def __get_doc_image(self, viewer_width):
        for image_path in sorted(glob.glob(os.path.join(self.__path_data.image_dir_path, '*.png'))):
            pix_map = QPixmap(image_path).scaledToWidth(viewer_width)
            self.__doc_image_tuple = self.__doc_image_tuple + (pix_map,)

        self.max_page = len(self.__doc_image_tuple)

    def __set_layout(self):
        previous_button = QPushButton('1ページ戻る')
        previous_button.setAutoDefault(False)
        previous_button.clicked.connect(self.__previous_page)
        next_button = QPushButton('1ページ進む')
        next_button.setAutoDefault(True)
        next_button.clicked.connect(self.__next_page)
        self.turn_page(0)
        self.__current_page_label.resize(self.__current_page_label.sizeHint())

        grid = QGridLayout()
        grid.addWidget(previous_button,            0, 0,  1, 10)
        grid.addWidget(self.__scroll,              1, 0, 10, 10)
        grid.addWidget(next_button,               11, 0,  1,  9)
        grid.addWidget(self.__current_page_label, 11, 9,  1,  1)

        self.setLayout(grid)

    def __previous_page(self):
        self.turn_page((self.__current_page + self.max_page - 1) % self.max_page)

    def __next_page(self):
        self.turn_page((self.__current_page + 1) % self.max_page)

    def turn_page(self, page):
        self.__current_page = page
        label = QLabel()
        label.setPixmap(self.__doc_image_tuple[self.__current_page])
        self.__scroll.setWidget(label)
        self.__current_page_label.setText('ページ' + str(self.__current_page + 1))

    def emit_current_page(self):
        self.current_page_response.emit(self.__current_page + 1)