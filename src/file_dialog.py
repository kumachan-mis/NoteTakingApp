#!/usr/local/bin/python3
import os
from PyQt5.QtWidgets import QFileDialog
import data
import make_dir


class NewOrOpen:
    def __init__(self, is_close, widget=None):
        self.__is_close = is_close
        self.__widget = widget

    def gen_new_note(self):
        pdf_path = QFileDialog.getOpenFileName(None, '講義資料を開く',
                                               os.path.expanduser('~') + '/Desktop', '*.pdf')[0]
        if os.path.splitext(pdf_path)[1] != '.pdf':
            return
        self.__goto_make_dir(data.PathData(True, pdf_path=pdf_path))

    def choose_open_file(self):
        file_path = QFileDialog.getOpenFileName(None, 'ノートを開く',
                                                os.path.expanduser('~') + '/Desktop', '*' + data.my_extension)[0]
        if os.path.splitext(file_path)[1] != data.my_extension:
            return
        self.__goto_make_dir(data.PathData(False, file_path=file_path))

    def __goto_make_dir(self, path_data):
        if self.__is_close:
            self.__widget.close()
            self.__widget.deleteLater()

        mk_dir = make_dir.MakeDirProgress(path_data)
        mk_dir.exec_()