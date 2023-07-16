import cv2
from PyQt5.QtCore import Qt, QMimeData, QPropertyAnimation, QPoint, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, \
    QMessageBox
from PyQt5 import uic
# from usage import img_analysis
from PIL import Image


class MyGUI(QMainWindow):
    def __init__(self, detection, prob):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        # self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label.setText(detection + "  " + str(100*prob) + '%')
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))

        self.label_9 = QLabel(self)
        self.label_9.setText("detection result")
        self.label_9.move(100, 10)

        self.label_10 = QLabel(self)
        self.label_10.setText("second plot")
        self.label_10.move(500, 10)

        self.label_11 = QLabel(self)
        self.label_11.setText("localization plot")
        self.label_11.move(100, 200)

        self.label_12 = QLabel(self)
        self.label_12.setText("tSNE plot")
        self.label_12.move(500, 200)

        self.label_13 = QLabel(self)
        self.label_13.setText("feature map 32")
        self.label_13.move(100, 405)

        self.label_14 = QLabel(self)
        self.label_14.setText("feature map 64")
        self.label_14.move(280, 405)

        self.label_15 = QLabel(self)
        self.label_15.setText("feature map 128")
        self.label_15.move(460, 405)

        self.label_16 = QLabel(self)
        self.label_16.setText("feature map 256")
        self.label_16.move(640, 405)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI("Fake", 0.9)
    window.show()
    app.exec()
