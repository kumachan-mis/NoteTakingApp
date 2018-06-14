import sys
from PyQt5.QtWidgets import *

# entry point
if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    widget = QScrollArea()
    widget.setWidgetResizable(True)

    inner = QWidget()
    layout = QVBoxLayout(inner)
    inner.setLayout(layout)
    widget.setWidget(inner)

    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))
    layout.addWidget(QPushButton('OK!'))

    widget.show()
    sys.exit(myapp.exec_())
