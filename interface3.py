import sys
from PyQt5.QtCore import Qt, QMimeData, QPoint, QTimer, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PyQt5 import uic


class MyGUI(QMainWindow):
    def __init__(self, detection, prob, layer_string):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        widthScreen = 1300
        heightScreen = 600

        if detection == "Fake":
            self.label.setStyleSheet("background-color: #f7c994; color: Red;")
        else:
            self.label.setStyleSheet(
                "background-color: #f7c994; color: Green;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText("  " + detection + "  " + str(100 * prob) + '%')
        self.labelx = self.label.x()/widthScreen
        self.labely = self.label.y()/heightScreen
        self.labelw = self.label.width()/widthScreen
        self.labelh = self.label.height()/heightScreen
        self.textLabel = QLabel(self)
        self.textLabel.setText("Detection Result")
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel.move(self.label.x(),  self.label.y() - 25)

        tmp = ""
        for i in layer_string:
            tmp += str(i) + "\n"

        tmp = tmp[:-2]

        self.label_2.setStyleSheet("background-color: #f7c994; color: black;")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setText(tmp)
        self.label_2x = self.label_2.x()/widthScreen
        self.label_2y = self.label_2.y()/heightScreen
        self.label_2w = self.label_2.width()/widthScreen
        self.label_2h = self.label_2.height()/heightScreen
        self.textLabel2 = QLabel(self)
        self.textLabel2.setText("Parsed Model")
        self.textLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel2.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel2.move(self.label_2.x(),  self.label_2.y() - 25)

        # self.label_3.setPixmap(QPixmap('pred_mask.png'))
        # self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('pred_mask.png'))
        self.label_5x = self.label_5.x()/widthScreen
        self.label_5y = self.label_5.y()/heightScreen
        self.label_5w = self.label_5.width()/widthScreen
        self.label_5h = self.label_5.height()/heightScreen
        self.textLabel5 = QLabel(self)
        self.textLabel5.setText("Binary Mask")
        self.textLabel5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel5.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel5.move(self.label_5.x(),  self.label_5.y() - 25)
        # self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        # self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_7.setStyleSheet("background-color: #f7c994; color: black;")
        self.label_7x = self.label_7.x()/widthScreen
        self.label_7y = self.label_7.y()/heightScreen
        self.label_7w = self.label_7.width()/widthScreen
        self.label_7h = self.label_7.height()/heightScreen
        self.textLabel7 = QLabel(self)
        self.textLabel7.setText("Feature Map")
        self.textLabel7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel7.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel7.move(self.label_7.x(),  self.label_7.y() - 25)

        self.label_8.setPixmap(QPixmap('result_tsne.png'))
        self.label_8x = self.label_8.x()/widthScreen
        self.label_8y = self.label_8.y()/heightScreen
        self.label_8w = self.label_8.width()/widthScreen
        self.label_8h = self.label_8.height()/heightScreen
        self.textLabel8 = QLabel(self)
        self.textLabel8.setText("tSNE plot")
        self.textLabel8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel8.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel8.move(self.label_8.x(),  self.label_8.y() - 25)

        self.label_9.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_9x = self.label_9.x()/widthScreen
        self.label_9y = self.label_9.y()/heightScreen
        self.label_9w = self.label_9.width()/widthScreen
        self.label_9h = self.label_9.height()/heightScreen
        self.textLabel9 = QLabel(self)
        self.textLabel9.setText("Original Image")
        self.textLabel9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel9.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel9.move(self.label_9.x(),  self.label_9.y() - 25)

        # self.label_10 = QLabel(self)
        # self.label_10.setText("Detection Result")
        # self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_10.setStyleSheet("color: black; font-weight: bold;")
        # self.label_10.move(150, -5)

        # self.label_11 = QLabel(self)
        # self.label_11.setText("Model Parsing")
        # self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_11.setStyleSheet("color: black; font-weight: bold;")
        # self.label_11.move(530, -5)

        self.label_11.setStyleSheet("background-color: #82eefd; color: black;")
        self.label_11x = self.label_11.x()/widthScreen
        self.label_11y = self.label_11.y()/heightScreen
        self.label_11w = self.label_11.width()/widthScreen
        self.label_11h = self.label_11.height()/heightScreen
        self.textLabel11 = QLabel(self)
        self.textLabel11.setText("New Plot")
        self.textLabel11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel11.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel11.move(self.label_11.x(), self.label_11.y() - 25)

        self.test = QLabel(self)
        self.test.setGeometry(418, 170, 15, 15)
        self.test.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.test.setStyleSheet("background-color: #82eefd; color: black;")

        self.label_10.setStyleSheet("background-color: #00ccff; color: black;")
        self.label_10x = self.label_10.x()/widthScreen
        self.label_10y = self.label_10.y()/heightScreen
        self.label_10w = self.label_10.width()/widthScreen
        self.label_10h = self.label_10.height()/heightScreen
        self.label_10.setPixmap(QPixmap('asset/Hierarchical_Tree.png'))
        self.textLabel10 = QLabel(self)
        self.textLabel10.setText("Tree Structure")
        self.textLabel10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel10.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel10.move(self.label_10.x(),  self.label_10.y() - 25)

        self.show()

    def resizeEvent(self, event):
        # Override resizeEvent to handle resizing
        # This method is called whenever the window is resized
        size = event.size()
        # self.label.setText(f"Window size: {size.width()}x{size.height()}")
        self.resize(size)

        old_size = event.oldSize()
        if old_size.width() == -1 and old_size.height() == -1:
            old_size = size

        diff = size - old_size

        self.label.setGeometry(size.width()*self.labelx, size.height() *
                               self.labely, size.width()*self.labelw, size.height()*self.labelh)
        self.textLabel.move(self.label.x(),  self.label.y() - 25)

        self.label_2.setGeometry(size.width()*self.label_2x, size.height() *
                                 self.label_2y, size.width()*self.label_2w, size.height()*self.label_2h)
        self.textLabel2.move(self.label_2.x(),  self.label_2.y() - 25)

        # self.label_2.setText(
        #     f"Window size: {diff.width()}x{diff.height()}")

        self.label_5.setGeometry(size.width()*self.label_5x, size.height() *
                                 self.label_5y, size.width()*self.label_5w, size.height()*self.label_5h)
        self.textLabel5.move(self.label_5.x(),  self.label_5.y() - 25)

        self.label_7.setGeometry(size.width()*self.label_7x, size.height() *
                                 self.label_7y, size.width()*self.label_7w, size.height()*self.label_7h)
        self.textLabel7.move(self.label_7.x(),  self.label_7.y() - 25)

        self.label_8.setGeometry(size.width()*self.label_8x, size.height() *
                                 self.label_8y, size.width()*self.label_8w, size.height()*self.label_8h)
        self.textLabel8.move(self.label_8.x(),  self.label_8.y() - 25)

        self.label_9.setGeometry(size.width()*self.label_9x, size.height() *
                                 self.label_9y, size.width()*self.label_9w, size.height()*self.label_9h)
        self.textLabel9.move(self.label_9.x(),  self.label_9.y() - 25)

        self.label_10.setGeometry(size.width()*self.label_10x, size.height() *
                                  self.label_10y, size.width()*self.label_10w, size.height()*self.label_10h)
        self.textLabel10.move(self.label_10.x(),  self.label_10.y() - 25)

        self.label_11.setGeometry(size.width()*self.label_11x, size.height() *
                                  self.label_11y, size.width()*self.label_11w, size.height()*self.label_11h)
        self.textLabel11.move(self.label_11.x(),  self.label_11.y() - 25)

    # def enterEvent(self, event):
    #     # print(self.test.geometry())
    #     # print(event.pos())
    #     if self.test.geometry().contains(event.pos()):
    #         self.test.setStyleSheet("background-color: #00ccff; color: black;")

    # def leaveEvent(self, event):
    #     self.test.setStyleSheet("background-color: #82eefd; color: black;")

    def mousePressEvent(self, event):
        cursor_pos = event.pos()
        print(cursor_pos, self.test.geometry())

        if self.test.geometry().contains(cursor_pos):
            # self.test.setStyleSheet("background-color: #00ccff; color: black;")
            dlg = QDialog(self)
            dlg.setWindowTitle("Dialog")
            dlg.exec()

        else:
            pass
            # self.test.setStyleSheet("background-color: #82eefd; color: black;")


if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI("Fake", 0.9, ['MSE', 'ReLU',
                   'Sig', 'ReLU', 'SiLU', 'Down_sampling'])
    window.show()
    sys.exit(app.exec())
