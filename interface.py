import cv2
import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QRect
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget,\
    QMessageBox, QDialog
from PyQt5 import uic
import numpy as np

class MyGUI(QMainWindow):
    def __init__(self, detection, prob, layer_string):
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
        self.label_2.move(1000, 1000)
        self.label_2.setFixedWidth(325)
        self.label_2.setFixedHeight(250)

        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))
        self.label_9.setPixmap(QPixmap('sample_1.jpg'))

        self.label_10 = QLabel(self)
        self.label_10.setText("Detection Result")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setStyleSheet("color: black; font-weight: bold;")
        self.label_10.move(150, -5)
        self.label_10.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_11 = QLabel(self)
        self.label_11.setText("Model Parsing")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_11.setStyleSheet("color: black; font-weight: bold;")
        self.label_11.move(530, -5)
        self.label_11.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_12 = QLabel(self)
        self.label_12.setText("Localization Plot")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_12.setStyleSheet("color: black; font-weight: bold;")
        self.label_12.move(150, 200)
        self.label_12.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_13 = QLabel(self)
        self.label_13.setText("tSNE Plot")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_13.setStyleSheet("color: black; font-weight: bold;")
        self.label_13.move(530, 200)
        self.label_13.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_14 = QLabel(self)
        self.label_14.setText("Feature Map 32")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_14.setStyleSheet("color: black; font-weight: bold;")
        self.label_14.move(90, 405)
        self.label_14.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_15 = QLabel(self)
        self.label_15.setText("Feature Map 64")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_15.setStyleSheet("color: black; font-weight: bold;")
        self.label_15.move(270, 405)
        self.label_15.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_16 = QLabel(self)
        self.label_16.setText("Feature Map 128")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_16.setStyleSheet("color: black; font-weight: bold;")
        self.label_16.move(450, 405)
        self.label_16.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_17 = QLabel(self)
        self.label_17.setText("Feature Map 256")
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_17.setStyleSheet("color: black; font-weight: bold;")
        self.label_17.move(620, 405)
        self.label_17.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.

        self.label_18 = QLabel(self)
        self.label_18.setText("Original Picture")
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_18.setStyleSheet("color: black; font-weight: bold;")
        self.label_18.move(1000, -5)
        self.label_18.setFixedWidth(120)  # Set a fixed width for the label to accommodate the text.
        self.show()

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.setGeometry(window_geometry)

    def show_selected_image(self, image_path):
        # Load the selected image and set it as the pixmap for label_2 in MyGUI
        selected_image_pixmap = QPixmap(image_path)

        # Define the desired maximum width and height for the image in the MyGUI window
        max_width = 800
        max_height = 800

        # Scale the pixmap to fit within the desired dimensions while maintaining the aspect ratio
        scaled_pixmap = selected_image_pixmap.scaled(max_width, max_height, Qt.AspectRatioMode.KeepAspectRatio)

        # Set the scaled pixmap to label_2
        self.label_2.setPixmap(scaled_pixmap)


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False)

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

        self.ok_button.setVisible(False)

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
        self.animation.finished.connect(self.enable_ok_button)
        self.error_dialog = None  # Store the error dialog as an attribute of the main window

        self.show_welcome_screen()

        self.show()

    def enable_ok_button(self):
        self.ok_button.setEnabled(True)


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

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                self.display_image(image_path)
            else:
                self.clear_image()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            image_path = url.toLocalFile()
            self.display_image(image_path)

    def confirm_selection(self):
        #print("Confirm selection called.")
        if not self.image_path or self.selected_image_array is None or not np.any(self.selected_image_array):
            # Create a custom error dialog with the main window as its parent
            self.error_dialog = QDialog(self)
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            self.error_dialog.setParent(self)  # Set the main window as the parent of the error dialog

            # Calculate the position to center the error_dialog on the screen
            screen_geometry = QApplication.desktop().availableGeometry(self)
            error_dialog_width = 400  # Adjust the width of the error_dialog
            error_dialog_height = 200  # Adjust the height of the error_dialog
            error_dialog_x = screen_geometry.center().x() - (error_dialog_width // 2) + 11
            error_dialog_y = screen_geometry.center().y() - (error_dialog_height // 2) + 10

            # Set the style sheet for the error_dialog
            self.error_dialog.setStyleSheet(
            """
            QDialog {
                background-color: black;
                
            }
            QLabel {
                color: white;
                font-size: 18px;
            }
            """
            )

            # Move the error_dialog to the calculated position
            self.error_dialog.move(error_dialog_x, error_dialog_y)
            layout = QVBoxLayout(self.error_dialog)

            # Set the text color to black and override the color for the QLabel showing the text
            error_label = QLabel(" Sorry, " + " you must select an image.")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the text in the center

            error_label.setStyleSheet("color: white; font-size: 18px;")  # Set the font size to 18px (adjust as needed)
            # Set the minimum width and height of the error label to make it larger
            error_label.setMinimumWidth(365)  # Adjust the width to make the error message larger
            error_label.setMinimumHeight(50)  # Adjust the height to make the error message larger
            layout.addWidget(error_label)

            # Add your critical icon here, or you can use a QLabel with a pixmap of the critical icon.

            # Show the custom error dialog
            self.error_dialog.show()
            # Add this line to process events and ensure the error_dialog is displayed properly
            QApplication.processEvents()
            # Start the timer to close the error dialog after 2500 milliseconds (2.5 seconds)
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(self.error_dialog.close)
            timer.start(3000)

            return

        detection = "Some Detection Result"
        prob = 0.9
        layer_string = ["layer1", "layer2", "layer3"]

        self.secondW = MyGUI(detection, prob, layer_string)

        self.secondW.label_2.move(925, 250)
        # Load the selected image and set it as the pixmap for label_2 in MyGUI
        selected_image_pixmap = QPixmap(self.image_path)
        max_width = 800  # Adjust the desired width for the image
        max_height = 800  # Adjust the desired height for the image
        scaled_pixmap = selected_image_pixmap.scaled(max_width, max_height, Qt.AspectRatioMode.KeepAspectRatio)

        self.secondW.show_selected_image(self.image_path)

        # Set the scaled pixmap to label_2
        self.secondW.label_2.setPixmap(scaled_pixmap)

        # Show the MyGUI window and hide the ImageWindow
        self.secondW.show()

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

            print("Selected Image Array:")
            self.image_path = image_path
            # print(self.selected_image_array)
            # binary_mask = analysis(self.selected_image_array)
            # binary_mask.save('pred_mask.png')
        else:
            print("Failed to read the image file.")
            self.ok_button.setEnabled(False)

        self.ok_button.setVisible(True)
        return self.selected_image_array

    def clear_image(self):
        self.image_label.clear()
        self.image_label.setText("Drag and drop an image or click the button below to select")
        self.ok_button.setEnabled(False)
        self.ok_button.setVisible(False)
        self.selected_image_array = None
        self.image_path = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.ok_button.move(10, 50)

    window.show()
    sys.exit(app.exec())

