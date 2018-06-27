#!/usr/local/bin/python3
from sys import argv
from PyQt5.QtWidgets import QApplication
from new_or_open import NewOrOpen

if __name__ == '__main__':
    app = QApplication(argv)
    new_or_open = NewOrOpen()
    new_or_open.exec_()