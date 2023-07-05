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
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))
        self.show()


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
