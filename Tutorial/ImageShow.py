import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QPixmap


class ImageShow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        h_box = QHBoxLayout(self)
        # QPixmapオブジェクト作成
        pix_map = QPixmap("test.png")

        # ラベルを作ってその中に画像を置く
        lbl = QLabel(self)
        lbl.setPixmap(pix_map)

        h_box.addWidget(lbl)
        self.setLayout(h_box)

        self.move(300, 200)
        self.setWindowTitle('ImageShow')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ImageShow()
    sys.exit(app.exec_())