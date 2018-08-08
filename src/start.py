#!/usr/local/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QVBoxLayout
import file_dialog


class StartMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.__new_note = QPushButton()
        self.__open_file = QPushButton()
        self.__new_or_open = file_dialog.NewOrOpen(True, self)

        self.__init_ui()

    def __init_ui(self):
        welcome_label = QLabel('サウンドノートへようこそ.')

        self.__new_note.setText('ノートを新規作成')
        self.__new_note.setToolTip('講義資料のPDFファイルを選択します.')
        self.__new_note.clicked.connect(self.__new_or_open.gen_new_note)
        self.__new_note.setAutoDefault(False)

        self.__open_file.setText('作ったノートを開く')
        self.__open_file.setToolTip('保存されているノートを選択します.')
        self.__open_file.setAutoDefault(False)
        self.__open_file.clicked.connect(self.__new_or_open.choose_open_file)

        v_box = QVBoxLayout()
        v_box.addWidget(welcome_label)
        v_box.addWidget(self.__new_note)
        v_box.addWidget(self.__open_file)

        self.setLayout(v_box)
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sm = StartMenu()
    sm.exec_()
    sys.exit(app.exec_())