import cv2
from PyQt5.QtCore import Qt, QMimeData, QPropertyAnimation, QPoint, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5 import uic

class MyGUI(QMainWindow):
    def __init__(self, detection, prob, layer_string):
        super().__init__()
        uic.loadUi("form.ui", self)
        
        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)
        
        self.label.setStyleSheet("background-color: #f7c994; color: black;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("  " + detection + "  " + str(100 * prob) + '%')
        
        tmp = ""
        for i in layer_string:
            tmp += str(i) + "\n"
        
        tmp = tmp[:-2]
        
        self.label_2.setStyleSheet("background-color: #f7c994; color: black;")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setText(tmp)
        
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))
        
        self.label_9 = QLabel(self)
        self.label_9.setText("detection result")
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setStyleSheet("color: black; font-weight: bold;")
        self.label_9.move(150, -5)
        
        self.label_10 = QLabel(self)
        self.label_10.setText("model parsing")
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setStyleSheet("color: black; font-weight: bold;")
        self.label_10.move(530, -5)
        
        self.label_11 = QLabel(self)
        self.label_11.setText("localization plot")
        self.label_11.setAlignment(Qt.AlignCenter)
        self.label_11.setStyleSheet("color: black; font-weight: bold;")
        self.label_11.move(150, 200)
        
        self.label_12 = QLabel(self)
        self.label_12.setText("tSNE plot")
        self.label_12.setAlignment(Qt.AlignCenter)
        self.label_12.setStyleSheet("color: black; font-weight: bold;")
        self.label_12.move(530, 200)
        
        self.label_13 = QLabel(self)
        self.label_13.setText("feature map 32")
        self.label_13.setAlignment(Qt.AlignCenter)
        self.label_13.setStyleSheet("color: black; font-weight: bold;")
        self.label_13.move(90, 405)
        
        self.label_14 = QLabel(self)
        self.label_14.setText("feature map 64")
        self.label_14.setAlignment(Qt.AlignCenter)
        self.label_14.setStyleSheet("color: black; font-weight: bold;")
        self.label_14.move(270, 405)
        
        self.label_15 = QLabel(self)
        self.label_15.setText("feature map 128")
        self.label_15.setAlignment(Qt.AlignCenter)
        self.label_15.setStyleSheet("color: black; font-weight: bold;")
        self.label_15.move(450, 405)
        
        self.label_16 = QLabel(self)
        self.label_16.setText("feature map 256")
        self.label_16.setAlignment(Qt.AlignCenter)
        self.label_16.setStyleSheet("color: black; font-weight: bold;")
        self.label_16.move(620, 405)
        self.show()
        
if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI("Fake", 0.9, ['MSE', 'ReLU', 'Sig', 'ReLU', 'SiLU', 'Down_sampling'])
    window.show()
    app.exec()
