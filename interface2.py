from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.label.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.show()


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()