#!/usr/local/bin/python3
from os import path, makedirs
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout
from PyQt5.QtCore import QThread
from PyQt5.Qt import pyqtSignal


class MakeDirProgress(QWidget):
    def __init__(self, pdf_path):
        super().__init__()
        self.__loading_filename = QLabel()
        self.__progress = QProgressBar()
        self.__th = ProgressThread(pdf_path)
        self.__run_progress_thread()

        self.__init_ui()
        self.show()

    def __init_ui(self):
        self.setWindowTitle('講義資料読み込み')
        load = QLabel('読み込み中... しばらくお待ちください.')

        v_box = QVBoxLayout()
        v_box.addWidget(load)
        v_box.addWidget(self.__loading_filename)
        v_box.addWidget(self.__progress)
        self.setLayout(v_box)

    def __init_progress(self, max):
        self.__progress.setRange(0, max)

    def __update_progress(self, value, finename):
        self.__loading_filename.setText(finename)
        self.__progress.setValue(value)

    def __run_progress_thread(self):
        self.__th.load_ready.connect(self.__init_progress)
        self.__th.a_image_loaded.connect(self.__update_progress)
        self.__th.run()


class ProgressThread(QThread):
    load_ready = pyqtSignal(int)
    a_image_loaded = pyqtSignal(int, str)

    def __init__(self, pdf_path):
        super().__init__()
        self.__pdf_path = pdf_path

    def __make_image_dir(self, pdf_path):
        filename = path.splitext(path.split(pdf_path)[1])[0]
        image_dir_path = path.join('../images', filename)

        if path.isdir(image_dir_path):
            return

        makedirs(image_dir_path)
        images = convert_from_path(pdf_path)
        self.load_ready.emit(len(images))

        page = 1
        for image in images:
            save_path = path.join(image_dir_path, 'page{:0=3}.png')
            self.a_image_loaded.emit(page, save_path.format(page))
            image.save(save_path.format(page), 'png')
            page = page + 1

    def run(self):
        self.__make_image_dir(self.__pdf_path)