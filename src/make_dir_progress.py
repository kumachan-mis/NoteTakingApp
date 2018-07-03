#!/usr/local/bin/python3
from os import path, makedirs
from pdf2image import convert_from_path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.Qt import pyqtSignal
from main_window import UserInterface
from error_window import ErrorWindow


class MakeDirProgress(QDialog):
    def __init__(self, is_new, pdf_path = '', file_path = ''):
        super().__init__()
        self.__is_new = is_new
        self.__pdf_path = pdf_path
        self.__file_path = file_path
        self.__set_pdf_path()

        self.__loading_filename = QLabel()
        self.__progress = QProgressBar()
        self.__th = ProgressThread(self.__pdf_path)
        self.__run_progress_thread()

        self.__init_ui()

    def __set_pdf_path(self):
        if self.__file_path == '':
            return

        with open(self.__file_path, 'r') as file:
            self.__pdf_path = file.readline()[:-1]

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
            self.close()
            self.__gen_main_window()
        elif max == -2:
            self.__th.quit()
            self.close()
            self.__gen_error_window()
        else:
            self.__progress.setRange(0, max)

    def __update_progress(self, value, filename):
        self.__loading_filename.setText(filename)
        self.__progress.setValue(value)

        if value == self.__progress.maximum():
            self.__th.quit()
            self.close()
            self.__gen_main_window()

    def __run_progress_thread(self):
        self.__th.load_ready.connect(self.__init_progress)
        self.__th.a_image_loaded.connect(self.__update_progress)
        self.__th.start()

    def __gen_main_window(self):
        if self.__is_new:
            ui = UserInterface(True, pdf_path=self.__pdf_path)
        else:
            ui = UserInterface(False, file_path=self.__file_path)
        ui.exec_()

    def __gen_error_window(self):
        self.close()
        error = ErrorWindow(self.__pdf_path + 'は見つかりませんでした...')
        error.exec_()


class ProgressThread(QThread):
    load_ready = pyqtSignal(int)
    a_image_loaded = pyqtSignal(int, str)

    def __init__(self, pdf_path):
        super().__init__()
        self.__pdf_path = pdf_path

    def __make_image_dir(self):
        filename = path.splitext(path.split(self.__pdf_path)[1])[0]
        image_dir_path = path.join('../images', filename)

        if path.isdir(image_dir_path):
            self.load_ready.emit(-1)
            return

        if not path.isfile(self.__pdf_path):
            self.load_ready.emit(-2)
            return

        makedirs(image_dir_path)
        images = convert_from_path(self.__pdf_path)
        self.load_ready.emit(len(images))

        page = 1
        for image in images:
            save_path = path.join(image_dir_path, 'page{:0=3}.png')
            image.save(save_path.format(page), 'png')
            self.a_image_loaded.emit(page, save_path.format(page))
            page = page + 1

    def run(self):
        self.__make_image_dir()