from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class ErrorWindow(QDialog):
    def __init__(self, error_message):
        super().__init__()
        self.__init_ui(error_message)

    def __init_ui(self, error_message):
        self.setWindowTitle('エラー')
        error_message = QLabel(error_message)
        ok = QPushButton('OK')
        ok.setAutoDefault(False)
        ok.clicked.connect(self.__quit)

        v_box = QVBoxLayout()
        v_box.addWidget(error_message)
        v_box.addWidget(ok)

        self.setLayout(v_box)
        self.show()

    def __quit(self):
        self.close()
        self.deleteLater()