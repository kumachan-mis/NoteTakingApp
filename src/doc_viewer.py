#!/usr/local/bin/python3
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from pdf2image import convert_from_path
from glob import glob


class DocumentViewer(QWidget):
    dir_path_header = '/Users/suwayuya/Desktop/Lectures/'

    def __init__(self, filename, image_size):
        super().__init__()
        self.__image_dir_path = os.path.join('../images', filename)
        self.viewer_width = 0
        self.__doc_label_list = []
        self.__current_page = 0
        self.max_page = 0
        self.__v_box = QVBoxLayout()

        self.__make_image_dir(filename)
        self.__get_doc_image(image_size)

    def __make_image_dir(self, filename):
        if os.path.isdir(self.__image_dir_path):
            print(self.__image_dir_path + '　が見つかりました')
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

    def __get_doc_image(self, viewer_height):
        for image_path in sorted(glob(os.path.join(self.__image_dir_path, '*.png'))):
            pix_map = QPixmap(image_path).scaledToHeight(viewer_height)

            if self.viewer_width == 0:
                self.viewer_width = pix_map.width()

            label = QLabel()
            label.setPixmap(pix_map)
            self.__doc_label_list.append(label)

        print(self.__doc_label_list)
        self.max_page = len(self.__doc_label_list)

        previous_button = QPushButton("1ページ戻る")
        previous_button.clicked.connect(self.__previous_page)
        next_button = QPushButton('1ページ進む')
        next_button.clicked.connect(self.__next_page)

        self.__v_box.addWidget(previous_button)
        self.__v_box.addWidget(self.__doc_label_list[self.__current_page])
        self.__v_box.addWidget(next_button)
        self.setLayout(self.__v_box)

    def __previous_page(self):
        previous_page = (self.__current_page + self.max_page - 1) % self.max_page
        self.__v_box.replaceWidget(
            self.__doc_label_list[self.__current_page],
            self.__doc_label_list[previous_page])
        print(self.__doc_label_list)
        self.__current_page = previous_page

    def __next_page(self):
        next_page = (self.__current_page + 1) % self.max_page
        self.__v_box.replaceWidget(
            self.__doc_label_list[self.__current_page],
            self.__doc_label_list[next_page])
        print(self.__doc_label_list)
        self.__current_page = next_page
