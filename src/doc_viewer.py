#!/usr/local/bin/python3
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton
from PyQt5.QtGui import QPixmap
from pdf2image import convert_from_path
from glob import glob


class DocumentViewer(QWidget):
    dir_path_header = '/Users/suwayuya/Desktop/Lectures/'

    def __init__(self, filename, image_size):
        super().__init__()
        self.__image_dir_path = os.path.join('../images', filename)
        self.__doc_image_list = []
        self.__current_page = 0
        self.max_page = 0
        self.__scroll = QScrollArea()
        self.__scroll.setWidgetResizable(True)

        self.__make_image_dir(filename)
        self.__get_doc_image(image_size)

    def __make_image_dir(self, filename):
        if os.path.isdir(self.__image_dir_path):
            return

        print(self.__image_dir_path + '　を新規作成します')
        os.makedirs(self.__image_dir_path)
        pdf_path = os.path.join(DocumentViewer.dir_path_header, filename + '.pdf')
        print('読み込み中：' + pdf_path)
        images = convert_from_path(pdf_path)

        page = 1
        for image in images:
            save_path = os.path.join(self.__image_dir_path, 'page{:0=3}.png')
            print('出力：' + save_path.format(page))
            image.save(save_path.format(page), 'png')
            page = page + 1

        print('読み込みが完了しました.')

    def __get_doc_image(self, viewer_width):
        for image_path in sorted(glob(os.path.join(self.__image_dir_path, '*.png'))):
            pix_map = QPixmap(image_path).scaledToWidth(viewer_width)
            self.__doc_image_list.append(pix_map)

        self.max_page = len(self.__doc_image_list)

        previous_button = QPushButton("1ページ戻る")
        previous_button.clicked.connect(self.__previous_page)
        next_button = QPushButton('1ページ進む')
        next_button.clicked.connect(self.__next_page)
        self.turn_page(0)

        v_box = QVBoxLayout()
        v_box.addWidget(previous_button)
        v_box.addWidget(self.__scroll)
        v_box.addWidget(next_button)
        self.setLayout(v_box)

    def __previous_page(self):
        self.turn_page((self.__current_page + self.max_page - 1) % self.max_page)

    def __next_page(self):
        self.turn_page((self.__current_page + 1) % self.max_page)

    def turn_page(self, page):
        self.__current_page = page
        label = QLabel()
        label.setPixmap(self.__doc_image_list[self.__current_page])
        self.__scroll.setWidget(label)