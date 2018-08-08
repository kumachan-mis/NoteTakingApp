#!/usr/local/bin/python3
from PyQt5.QtGui import QTextCursor

end_flag = 'END\n'


def reader(file, text_edit):
    text_edit.clear()
    while True:
        line = file.readline()
        if line == end_flag:
            break
        text_edit.append(line[1:-1])


def writer(file, text_edit):
    cursor = text_edit.textCursor()
    cursor.movePosition(QTextCursor.Start)

    while True:
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        file.write('#' + cursor.selectedText() + '\n')

        if cursor.atEnd():
            file.write(end_flag)
            break

        cursor.movePosition(QTextCursor.Down)