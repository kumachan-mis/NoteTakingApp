#!/usr/local/bin/python3
import sys
import os
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QDialog,
                             QPushButton, QSplitter, QVBoxLayout, QGridLayout, QMessageBox,
                             QMenuBar, QFileDialog, QAction)
from PyQt5.Qt import QSize, Qt
import memo_box
import doc_viewer
import stream_editor
import file_dialog
from data import my_extension


class UserInterface(QWidget):
    __num_of_instance = 0

    def exec_(self):
        self.__dialog.exec_()

    def __init__(self, path_data):
        super().__init__()
        UserInterface.__num_of_instance += 1
        self.path_data = path_data
        self.__dialog = QDialog()

        screen = QApplication.desktop()
        self.resize(screen.width(), 9*screen.height()/10)
        self.__doc_area_size = QSize(3*self.width()/5, 7*self.height()/10)

        self.__gen_memo_box = QPushButton()
        self.__stream_area = stream_editor.StreamingEditor()
        self.__stream_area.run_streaming_thread()

        self.set_title()
        self.__center()
        if self.path_data.is_new:
            self.__new_window()
        else:
            self.__open_saved_file()
        self.__set_components()
        self.__set_layout()
        self.show()

    def set_title(self):
        if self.path_data.file_name == '':
            self.setWindowTitle('サウンドノート - [新規ノート]')
        else:
            self.setWindowTitle('サウンドノート - ' + self.path_data.file_name)

    def __center(self):
        flame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        flame.moveCenter(center_point)
        self.move(flame.topLeft())

    def __set_components(self):
        menu_bar = UIMenuBar(self)
        menu_bar.set_file_menu()

        self.__gen_memo_box.setText('新規ボックスを作成')
        self.__gen_memo_box.setAutoDefault(False)
        self.__gen_memo_box.clicked.connect(self.__memo_box_group.add_new_box)

        self.__stream_area.current_page_request.connect(
            self.__doc_area.emit_current_page
        )
        self.__doc_area.current_page_response.connect(
            self.__stream_area.print_final_result
        )

    def __set_layout(self):
        memo_widget = QSplitter(Qt.Horizontal)
        memo_widget.addWidget(self.__memo_box_group)
        memo_widget.addWidget(self.__doc_area)
        memo_widget.setSizes([self.width() - self.__doc_area_size.width(), self.__doc_area_size.width()])

        grid = QGridLayout()
        grid.addWidget(self.__gen_memo_box, 0, 0, 1,  1)
        grid.addWidget(self.__stream_area,  0, 1, 1, 10)
        stream_widget = QWidget()
        stream_widget.setLayout(grid)

        v_box = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(memo_widget)
        splitter.addWidget(stream_widget)
        splitter.setSizes([self.__doc_area_size.height(), self.height() - self.__doc_area_size.height()])
        v_box.addWidget(splitter)

        self.__dialog.setLayout(v_box)
        v_box = QVBoxLayout()
        v_box.addWidget(self.__dialog)
        self.setLayout(v_box)

    def __new_window(self):
        self.__doc_area = doc_viewer.DocumentViewer(self.path_data, self.__doc_area_size.width())
        self.__memo_box_group = memo_box.MemoBoxGroup(self.__doc_area.max_page, self.__doc_area.turn_page)
        self.__memo_box_group.set_default()

    def __open_saved_file(self):
        with open(self.path_data.file_path, 'r') as file:
            self.path_data.set_pdf_image_dir_path(file.readline()[:-1])
            self.__doc_area = doc_viewer.DocumentViewer(self.path_data, self.__doc_area_size.width())
            self.__memo_box_group = memo_box.MemoBoxGroup(self.__doc_area.max_page, self.__doc_area.turn_page)
            self.__memo_box_group.read_memo_box_group_info(file)
            self.__stream_area.read_final_result(file)

    def write_file(self):
        with open(self.path_data.file_path, 'w') as file:
            file.write(self.path_data.pdf_path + '\n')
            self.__memo_box_group.write_memo_box_group_info(file)
            self.__stream_area.write_final_result(file)

    def closeEvent(self, event):
        get_reply = QMessageBox.question(self, 'close', 'ウィンドウを閉じていいですか？',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if get_reply == QMessageBox.Yes:
            event.accept()
            UserInterface.__num_of_instance -= 1
            self.close()
            if UserInterface.__num_of_instance == 0:
                sys.exit()
        else:
            event.ignore()


class UIMenuBar(QMenuBar):
    def __init__(self, ui):
        super().__init__(ui)
        self.__ui = ui
        self.__new_or_open = file_dialog.NewOrOpen(False)

    def set_file_menu(self):
        file_menu = self.addMenu(' &ファイル')

        action = QAction(' &名前をつけて保存', self.__ui)
        action.setShortcut('Ctrl+Shift+S')
        action.triggered.connect(self.__save_as_new_file)
        file_menu.addAction(action)

        action = QAction(' &上書き保存', self.__ui)
        action.setShortcut('Ctrl+S')
        action.triggered.connect(self.__overwrite_save_file)
        file_menu.addAction(action)

        action = QAction(' &ノートを新規作成', self.__ui)
        action.setShortcut('Ctrl+N')
        action.triggered.connect(self.__new_or_open.gen_new_note)
        file_menu.addAction(action)

        action = QAction(' &ノートを開く', self.__ui)
        action.setShortcut('Ctrl+O')
        action.triggered.connect(self.__new_or_open.choose_open_file)
        file_menu.addAction(action)

        file_menu.addSeparator()
        action = QAction(' &終了', self.__ui)
        action.triggered.connect(self.__ui.close)
        file_menu.addAction(action)

    def __save_as_new_file(self):
        file_path = QFileDialog.getSaveFileName(self, 'ノートを保存',
                                                os.path.expanduser('~') + '/Desktop', '*' + my_extension)[0]
        if file_path == '':
            return
        self.__ui.path_data.set_file_path_name(file_path)
        self.__ui.write_file()
        self.__ui.set_title()

    def __overwrite_save_file(self):
        if self.__ui.path_data.file_path == '':
            self.__save_as_new_file()
            return
        self.__ui.write_file()