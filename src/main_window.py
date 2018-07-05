#!/usr/local/bin/python3
from sys import exit
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QSize
from memo_box import MemoBoxGroup
from doc_viewer import DocumentViewer
from stream_editor import StreamEditor

my_extension = '.soundnote'


class UserInterface(QDialog):
    def __init__(self, is_new, pdf_path = '', file_path = ''):
        super().__init__()

        self.__file_path = file_path

        screen = QApplication.desktop()
        self.resize(9 * screen.width() / 10, 9 * screen.height() / 10)
        self.__doc_area_size = QSize(3 * self.width() / 5, 4 * self.height() / 5)

        self.__gen_memo_box = QPushButton()
        self.__save_overwrite = QPushButton()
        self.__save_new = QPushButton()
        self.__stream_area = StreamEditor()
        self.__stream_area.run_streaming_thread()

        self.setWindowTitle("サウンドノート")
        self.__center()
        if is_new:
            self.__new_window(pdf_path)
        else:
            self.__open_saved_file()
        self.__set_components()
        self.__set_layout()

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __set_components(self):
        self.__gen_memo_box.setText("新規ボックスを作成")
        self.__gen_memo_box.setAutoDefault(False)
        self.__gen_memo_box.clicked.connect(self.__memo_box_group.add_new_box)

        self.__save_overwrite.setText('上書き保存(ctrl+S)')
        self.__save_overwrite.setAutoDefault(False)
        self.__save_overwrite.clicked.connect(self.__overwrite_save_file)

        save_action = QAction(self)
        save_action.setShortcut(QKeySequence('Ctrl+S'))
        save_action.triggered.connect(self.__overwrite_save_file)
        self.addAction(save_action)

        self.__save_new.setText("新しいノートとして保存")
        self.__save_new.setAutoDefault(False)
        self.__save_new.clicked.connect(self.__save_as_new_file)

    def __set_layout(self):
        memo_widget = QSplitter(Qt.Horizontal)
        memo_widget.addWidget(self.__memo_box_group)
        memo_widget.addWidget(self.__doc_area)
        memo_widget.setSizes([self.width() - self.__doc_area_size.width(), self.__doc_area_size.width()])

        v_box = QVBoxLayout()
        v_box.addWidget(self.__gen_memo_box)
        v_box.addWidget(self.__save_overwrite)
        v_box.addWidget(self.__save_new)
        button_widget = QWidget()
        button_widget.setLayout(v_box)

        grid = QGridLayout()
        grid.addWidget(button_widget,      0, 0, 1,  1)
        grid.addWidget(self.__stream_area, 0, 1, 1, 10)
        stream_widget = QWidget()
        stream_widget.setLayout(grid)

        v_box = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(memo_widget)
        splitter.addWidget(stream_widget)
        splitter.setSizes([self.__doc_area_size.height(), self.height() - self.__doc_area_size.height()])
        v_box.addWidget(splitter)

        self.setLayout(v_box)

    def __new_window(self, pdf_path):
        self.__doc_area = DocumentViewer(pdf_path, self.__doc_area_size.width())
        self.__memo_box_group = MemoBoxGroup(self.__doc_area.max_page, self.__doc_area.turn_page)
        self.__memo_box_group.set_default()

    def __open_saved_file(self):
        with open(self.__file_path, 'r') as file:
            self.__doc_area = DocumentViewer(file.readline()[:-1], self.__doc_area_size.width())
            self.__memo_box_group = MemoBoxGroup(self.__doc_area.max_page, self.__doc_area.turn_page)
            self.__memo_box_group.read_memo_box_group_info(file)
            self.__stream_area.read_final_result(file)

    def __save_as_new_file(self):
        file_path = QFileDialog.getSaveFileName(None, 'ノートを保存',
                                                path.expanduser('~') + '/Desktop', '*' + my_extension)[0]
        if file_path == '':
            return
        self.__file_path = file_path
        self.__write_file()

    def __overwrite_save_file(self):
        if self.__file_path == '':
            self.__save_as_new_file()
            return
        self.__write_file()

    def __write_file(self):
        with open(self.__file_path, 'w') as file:
            self.__doc_area.write_pdf_path(file)
            self.__memo_box_group.write_memo_box_group_info(file)
            self.__stream_area.write_final_result(file)

    def closeEvent(self, event):
        get_reply = QMessageBox.question(self, 'close', 'ウィンドウを閉じていいですか？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if get_reply == QMessageBox.Yes:
            event.accept()
            exit()
        else:
            event.ignore()