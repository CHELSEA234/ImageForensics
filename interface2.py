from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.label.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_3.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_4.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_5.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_6.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_7.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_8.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.show()


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
