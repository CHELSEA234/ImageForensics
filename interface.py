import cv2
import sys
import os
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QRect
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, \
    QMessageBox
from PyQt5 import uic
# from usage import img_analysis
from PIL import Image



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

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.setGeometry(window_geometry)

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.center_window()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_path = None
        self.setCentralWidget(self.image_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_timeout)
        stylesheet = """
            QMainWindow {
                background-color: black;
            }

            QLabel {
                color: white;
            }
        """

        self.setStyleSheet(stylesheet)

        self.welcome_label = QLabel("Welcome!", self)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 24, weight=QFont.Weight.Bold))
        self.welcome_label.setGeometry(0, 0, self.width(), self.height())

        self.animation = QPropertyAnimation(self.welcome_label, b"pos")
        self.animation.setDuration(1500)
        self.animation.setStartValue(QPoint(0, -self.height()))
        self.animation.setEndValue(QPoint(0, 0))

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)
        # self.select_button.setVisible(False)
        self.select_button.setStyleSheet(
            """
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #0D47A1;
            }
            """
        )

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False)
        self.ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: #B71C1C;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #8B0000;
            }
            """
        )

        # self.ok_button.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.select_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.selected_image_array = None

        self.animation.start()

        self.show_welcome_screen()

    def center_window(self):
        screen_geometry = QApplication.screens()[0].geometry()
        window_geometry = QRect(screen_geometry.center().x() - 350, screen_geometry.center().y() - 250, 700, 500)
        self.setGeometry(window_geometry)

    def show_welcome_screen(self):
        # self.welcome_label.setVisible(True)
        self.image_label.setVisible(False)
        self.select_button.setVisible(False)
        self.ok_button.setVisible(False)
        self.timer.start(2500)
        self.animation.start()

    def timer_timeout(self):
        self.timer.stop()
        self.show_image_selection_screen()


    def show_image_selection_screen(self):
        self.welcome_label.setVisible(False)
        self.image_label.setVisible(True)
        self.select_button.setVisible(True)
        self.ok_button.setVisible(True)
        self.image_label.setText("Drag and drop an image or click the button below to select")


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            image_path = url.toLocalFile()
            self.display_image(image_path)

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                self.display_image(image_path)

    def display_image(self, image_path: str):
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)

        maxWidth = 700
        maxHeight = 500

        scaledPixmap = pixmap.scaled(maxWidth, maxHeight, Qt.AspectRatioMode.KeepAspectRatio)

        self.image_label.clear()
        self.image_label.setPixmap(scaledPixmap)
        self.image_label.setText("")
        self.image_label.adjustSize()

        self.resize(image.width(), image.height())

        image_array = cv2.imread(image_path)
        if image_array is not None:
            self.selected_image_array = image_array
            self.ok_button.setEnabled(True)
            self.ok_button.setVisible(True)
            print("Selected Image Array:")
            self.image_path = image_path
            # print(self.selected_image_array)
            # binary_mask = analysis(self.selected_image_array)
            # binary_mask.save('pred_mask.png')
        else:
            print("Failed to read the image file.")
        return self.selected_image_array

    def confirm_selection(self):
        # Assuming you have the following attributes in the ImageWindow class:
        detection = "Some Detection Result"
        prob = 0.9
        layer_string = ["layer1", "layer2", "layer3"]

        self.secondW = MyGUI(detection, prob, layer_string)
        self.secondW.label_2.setPixmap(QPixmap(self.image_path))
        self.secondW.label_2.move(64, 19)  # Move the image label to the desired position under "detection results"
        self.secondW.show()

        self.hide()

    def clear_image(self):
        self.image_label.clear()
        self.image_label.setText(self.placeholder_text)
        self.ok_button.setEnabled(False)
        self.ok_button.setVisible(False)
        self.selected_image_array = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.ok_button.move(10, 50)
    window.show()
    sys.exit(app.exec())
