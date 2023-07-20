import sys
from PyQt5.QtCore import Qt, QMimeData, QPoint, QTimer, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5 import uic

class MyGUI(QMainWindow):
    def __init__(self, detection, prob, layer_string, original_image):
        super().__init__()
        uic.loadUi("form.ui", self)
        
        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)
        
        self.label.setStyleSheet("background-color: #f7c994; color: black;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText("  " + detection + "  " + str(100 * prob) + '%')
        
        tmp = ""
        for i in layer_string:
            tmp += str(i) + "\n"
        
        tmp = tmp[:-2]
        
        self.label_2.setStyleSheet("background-color: #f7c994; color: black;")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setText(tmp)
        
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))
        self.label_9.setPixmap(QPixmap(original_image))
        
        self.label_10 = QLabel(self)
        self.label_10.setText("Detection Result")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_10.move(150, -5)
        
        self.label_11 = QLabel(self)
        self.label_11.setText("Model Parsing")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_11.setStyleSheet("color: black; font-weight: bold;")
        self.label_11.move(530, -5)
        
        self.label_12 = QLabel(self)
        self.label_12.setText("Localization Result")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_12.setStyleSheet("color: black; font-weight: bold; font-size:8pt;")
        self.label_12.move(150, 200)
        
        self.label_13 = QLabel(self)
        self.label_13.setText("tSNE Plot")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_13.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_13.move(530, 200)
    
        self.label_14 = QLabel(self)
        self.label_14.setText("Feature Map 32")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_14.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_14.move(90, 405)

        self.label_15 = QLabel(self)
        self.label_15.setText("Feature Map 64")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_15.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_15.move(270, 405)
        
        self.label_16 = QLabel(self)
        self.label_16.setText("Feature Map 128")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_16.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_16.move(450, 405)
        
        self.label_17 = QLabel(self)
        self.label_17.setText("Feature Map 256")
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_17.setStyleSheet("color: black; font-weight: bold; font-size:9pt;")
        self.label_17.move(620, 405)
        
        self.label_18 = QLabel(self)
        self.label_18.setText(" Original Picture ")
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_18.setStyleSheet("color: black; font-weight: bold; font-size:9pt")
        self.label_18.move(1000, -5)
        self.show()
        
if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI("Fake", 0.9, ['MSE', 'ReLU', 'Sig', 'ReLU', 'SiLU', 'Down_sampling'], 'asset/sample_1.jpg')
    window.show()
    sys.exit(app.exec())