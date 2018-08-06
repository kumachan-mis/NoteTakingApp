#!/usr/local/bin/python3
from os import path
from PyQt5.QtWidgets import *
from make_dir_progress import MakeDirProgress
from main_window import my_extension


class NewOrOpen(QDialog):
    def __init__(self):
        super().__init__()
        self.__new_note = QPushButton()
        self.__open_file = QPushButton()

        self.__init_ui()

    def __init_ui(self):
        welcome_label = QLabel('サウンドノートへようこそ.')

        self.__new_note.setText('ノートを新規作成')
        self.__new_note.setToolTip('講義資料のPDFファイルを選択します.')
        self.__new_note.clicked.connect(self.__gen_new_note)
        self.__new_note.setAutoDefault(False)

        self.__open_file.setText('作ったノートを開く')
        self.__open_file.setToolTip('保存されているノートを選択します.')
        self.__open_file.setAutoDefault(False)
        self.__open_file.clicked.connect(self.__choose_open_file)

        v_box = QVBoxLayout()
        v_box.addWidget(welcome_label)
        v_box.addWidget(self.__new_note)
        v_box.addWidget(self.__open_file)

        self.setLayout(v_box)
        self.show()

    def __gen_new_note(self):
        pdf_path = QFileDialog.getOpenFileName(None, '講義資料を開く',
                                               path.expanduser('~') + '/Desktop', '*.pdf')[0]
        if path.splitext(pdf_path)[1] != '.pdf':
            exit()

        self.close()
        make_dir = MakeDirProgress(True, pdf_path=pdf_path)
        make_dir.exec_()

    def __choose_open_file(self):
        file_path = QFileDialog.getOpenFileName(None, 'ノートを開く',
                                                path.expanduser('~') + '/Desktop', '*' + my_extension)[0]
        if path.splitext(file_path)[1] != my_extension:
            exit()

        self.close()
        make_dir = MakeDirProgress(False, file_path=file_path)
        make_dir.exec_()