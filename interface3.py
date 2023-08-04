import sys
from PyQt5.QtCore import Qt, QMimeData, QPoint, QTimer, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PyQt5 import uic


class MyGUI(QMainWindow):
    def __init__(self, detection, prob, layer_string, image_path):
        super().__init__()
        uic.loadUi("form2.ui", self)

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        widthScreen = 1300
        heightScreen = 600

        if detection == "Fake":
            self.label.setStyleSheet("background-color: #f7c994; color: Red; font-size:16pt;")
        else:
            self.label.setStyleSheet(
                "background-color: #f7c994; color: Green; font-size:16pt;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText("  " + detection + "  " + str(100 * prob) + '%')
        self.labelx = self.label.x()/widthScreen
        self.labely = self.label.y()/heightScreen
        self.labelw = self.label.width()/widthScreen
        self.labelh = self.label.height()/heightScreen
        self.textLabel = QLabel(self)
        self.textLabel.setText("Detection Result")
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setStyleSheet("color: black; font-weight: bold; font-size:8pt")
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


        self.label_9.setPixmap(QPixmap(image_path))
        self.label_9x = self.label_9.x()/widthScreen
        self.label_9y = self.label_9.y()/heightScreen
        self.label_9w = self.label_9.width()/widthScreen
        self.label_9h = self.label_9.height()/heightScreen
        self.textLabel9 = QLabel(self)
        self.textLabel9.setText("Original Image")
        self.textLabel9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel9.setStyleSheet("color: black; font-weight: bold; font-size:8pt;")
        self.textLabel9.move(self.label_9.x(),  self.label_9.y() - 25)

        self.label_11.setStyleSheet("background-color: #f7c994; color: black;")
        self.label_11x = self.label_11.x()/widthScreen
        self.label_11y = self.label_11.y()/heightScreen
        self.label_11w = self.label_11.width()/widthScreen
        self.label_11h = self.label_11.height()/heightScreen
        self.textLabel11 = QLabel(self)
        self.textLabel11.setText("New Plot")
        self.textLabel11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel11.setStyleSheet("color: black; font-weight: bold;")
        self.textLabel11.move(self.label_11.x(), self.label_11.y() - 25)

        self.nodeW, self.nodeH = 15, 15
        self.nodeWw = self.nodeW/widthScreen
        self.nodeHh = self.nodeH/heightScreen

        self.level1 = QLabel(self)
        self.level1.setGeometry(418, 170, self.nodeW, self.nodeH)
        self.level1x = 418/widthScreen
        self.level1y = 170/heightScreen
        #self.level1.setStyleSheet("background-color: #00ccff;")
        self.level1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        y = 195
        x = 320
        x_diff = 205
        self.level2 = [QLabel(self) for i in range(2)]
        self.level2x = [0 for i in range(2)]
        self.level2y = [0 for i in range(2)]
        for i in range(2):
            self.level2[i].setGeometry(x, y,  self.nodeW, self.nodeH)
            self.level2x[i] = x/widthScreen
            self.level2y[i] = y/heightScreen
            #self.level2[i].setStyleSheet("background-color: #00ccff;")
            x = x + x_diff
        
        x = 255
        y = 215
        x_diff = 130
        self.level3 = [QLabel(self) for i in range(4)]
        self.level3x = [0 for i in range(4)]
        self.level3y = [0 for i in range(4)]
        for i in range(4):
            self.level3[i].setGeometry(x, y, self.nodeW, self.nodeH)
            self.level3x[i] = x/widthScreen
            self.level3y[i] = y/heightScreen
            #self.level3[i].setStyleSheet("background-color: #00ccff;")
            if i == 1:
                x_diff = 94
            x = x + x_diff
        
        x = 220
        y = 245
        x_diff = 65
        self.level4 = [QLabel(self) for i in range(4)]
        self.level4x = [0 for i in range(4)]
        self.level4y = [0 for i in range(4)]
        for i in range(4):
            self.level4[i].setGeometry(x, y, self.nodeW, self.nodeH)
            self.level4x[i] = x/widthScreen
            self.level4y[i] = y/heightScreen
            #self.level4[i].setStyleSheet("background-color: #00ccff;")
            x = x + x_diff

        x = 205
        y = 280
        x_diff = 33
        self.level5 = [QLabel(self) for i in range(13)]
        self.level5x = [0 for i in range(13)]
        self.level5y = [0 for i in range(13)]
        for i in range(13):
            self.level5[i].setGeometry(x, y, self.nodeW, self.nodeH)
            self.level5x[i] = x/widthScreen
            self.level5y[i] = y/heightScreen
            #self.level5[i].setStyleSheet("background-color: #00ccff;")
            x = x + x_diff

        self.label_10.setStyleSheet("background-color: #00ccff; color: black;")
        self.label_10x = self.label_10.x()/widthScreen
        self.label_10y = self.label_10.y()/heightScreen
        self.label_10w = self.label_10.width()/widthScreen
        self.label_10h = self.label_10.height()/heightScreen
        self.label_10.setPixmap(QPixmap('Tree.png'))

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

        self.label_11.setGeometry(size.width()*self.label_11x, size.height() *
                                  self.label_11y, size.width()*self.label_11w, size.height()*self.label_11h)
        self.textLabel11.move(self.label_11.x(),  self.label_11.y() - 25)

        self.level1.setGeometry(size.width()*self.level1x, size.height()*self.level1y, size.width()*self.nodeWw, size.height()*self.nodeHh)
        for i in range(2):
            self.level2[i].setGeometry(size.width()*self.level2x[i], size.height()*self.level2y[i], size.width()*self.nodeWw, size.height()*self.nodeHh)
        
        for i in range(4):
            self.level3[i].setGeometry(size.width()*self.level3x[i], size.height()*self.level3y[i], size.width()*self.nodeWw, size.height()*self.nodeHh)

        for i in range(4):
            self.level4[i].setGeometry(size.width()*self.level4x[i], size.height()*self.level4y[i], size.width()*self.nodeWw, size.height()*self.nodeHh)
        
        for i in range(13):
            self.level5[i].setGeometry(size.width()*self.level5x[i], size.height()*self.level5y[i], size.width()*self.nodeWw, size.height()*self.nodeHh)


    def mousePressEvent(self, event):
        cursor_pos = event.pos()
        #print(cursor_pos, self.level1.geometry())

        ck = False
        if self.level1.geometry().contains(cursor_pos):
            ck = True
        for i in range(2):
            if self.level2[i].geometry().contains(cursor_pos):
                ck = True
        for i in range(4):
            if self.level3[i].geometry().contains(cursor_pos):
                ck = True
        for i in range(4):
            if self.level4[i].geometry().contains(cursor_pos):
                ck = True
        for i in range(13):
            if self.level5[i].geometry().contains(cursor_pos):
                ck = True

        if ck:
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
                   'Sig', 'ReLU', 'SiLU', 'Down_sampling'], 'asset/sample_1.jpg')
    window.show()
    sys.exit(app.exec())
