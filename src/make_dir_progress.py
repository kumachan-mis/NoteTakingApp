#!/usr/local/bin/python3
from os import path, makedirs
from pdf2image import convert_from_path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.Qt import pyqtSignal
from main_window import UserInterface
from error_window import ErrorWindow


class MakeDirProgress(QDialog):
    def __init__(self, path_data):
        super().__init__()
        self.__path_data = path_data
        self.__set_pdf_path()

        self.__loading_filename = QLabel()
        self.__progress = QProgressBar()
        self.__th = ProgressThread(self.__path_data)
        self.__run_progress_thread()

        self.__init_ui()

    def __set_pdf_path(self):
        if self.__path_data.file_path == '':
            return

        with open(self.__path_data.file_path, 'r') as file:
            self.__path_data.set_pdf_image_dir_path(file.readline()[:-1])

    def __init_ui(self):
        screen = QApplication.desktop()
        self.resize(screen.width() / 4, screen.height() / 4)
        self.setWindowTitle('講義資料読み込み')
        self.__center()

        v_box = QVBoxLayout()
        load = QLabel('読み込み中... しばらくお待ちください.')
        v_box.addWidget(load)
        v_box.addWidget(self.__loading_filename)
        v_box.addWidget(self.__progress)
        self.setLayout(v_box)

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __init_progress(self, max):
        if max == -1:
            self.__th.quit()
            self.__gen_main_window()
        elif max == -2:
            self.__th.quit()
            self.__gen_error_window()
        else:
            self.__progress.setRange(0, max)

    def __update_progress(self, value, filename):
        self.__loading_filename.setText(filename)
        self.__progress.setValue(value)

        if value == self.__progress.maximum():
            self.__th.quit()
            self.__gen_main_window()

    def __run_progress_thread(self):
        self.__th.load_ready.connect(self.__init_progress)
        self.__th.a_image_loaded.connect(self.__update_progress)
        self.__th.start()

    def __gen_main_window(self):
        self.close()
        ui = UserInterface(self.__path_data)
        ui.exec_()

    def __gen_error_window(self):
        self.close()
        error = ErrorWindow(self.__path_data.pdf_path + 'は見つかりませんでした...')
        error.exec_()


class ProgressThread(QThread):
    load_ready = pyqtSignal(int)
    a_image_loaded = pyqtSignal(int, str)

    def __init__(self, path_data):
        super().__init__()
        self.__path_data = path_data

    def __make_image_dir(self):
        if path.isdir(self.__path_data.image_dir_path):
            self.load_ready.emit(-1)
            return

        if not path.isfile(self.__path_data.pdf_path):
            self.load_ready.emit(-2)
            return

        makedirs(self.__path_data.image_dir_path)
        images = convert_from_path(self.__path_data.pdf_path)
        self.load_ready.emit(len(images))

        page = 1
        for image in images:
            save_path = path.join(self.__path_data.image_dir_path, 'page{:0=3}.png')
            image.save(save_path.format(page), 'png')
            self.a_image_loaded.emit(page, save_path.format(page))
            page = page + 1

    def run(self):
        self.__make_image_dir()