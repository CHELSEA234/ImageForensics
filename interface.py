# still in development
# change the color scheme (top priority) - psuedo code commented out at the end of program.
# add a sound when the interface starts (top priority)
# add functionality so that multiple image files can be taken in the interface isntead of just 1????
# add some sort of error handling?
import cv2
from PyQt5.QtCore import Qt, QMimeData, QPropertyAnimation, QPoint
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QScreen
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, \
    QMessageBox
from PyQt5 import uic
# from usage import img_analysis
from PIL import Image

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.center_window()

        self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label.setText('fake')
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))
        self.show()

        self.center_window()


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

        self.welcome_label = QLabel("Welcome, press the Space key to proceed", self)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 24, weight=QFont.Weight.Bold))
        self.welcome_label.setGeometry(0, 0, self.width(), self.height())

        self.animation = QPropertyAnimation(self.welcome_label, b"pos")
        self.animation.setDuration(1500)
        self.animation.setStartValue(QPoint(0, -self.height()))
        self.animation.setEndValue(QPoint(0, 0))

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)
        self.select_button.setVisible(False)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False)
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

        self.show_welcome_screen()

    def center_window(self):
        screen_geometry = QApplication.screens()[0].geometry()
        window_geometry = self.geometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.setGeometry(window_geometry)

    def show_welcome_screen(self):
        self.welcome_label.setVisible(True)
        self.image_label.setVisible(False)
        self.select_button.setVisible(False)
        self.ok_button.setVisible(False)

    def show_image_selection_screen(self):
        self.welcome_label.setVisible(False)
        self.image_label.setVisible(True)
        self.select_button.setVisible(True)
        self.ok_button.setVisible(True)

        self.image_label.setText("Drag and drop an image or click the button below to select")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.show_image_selection_screen()

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
            # print(self.selected_image_array)
            #binary_mask = analysis(self.selected_image_array)
            #binary_mask.save('pred_mask.png')
        else:
            print("Failed to read the image file.")
        return self.selected_image_array

    def confirm_selection(self):
        self.secondW = MyGUI()

    def clear_image(self):
        self.image_label.clear()
        self.image_label.setText(self.placeholder_text)
        self.ok_button.setEnabled(False)
        self.ok_button.setVisible(False)
        self.selected_image_array = None

if __name__ == "__main__":
    app = QApplication([])
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.ok_button.move(10, 50)
    window.show()
    app.exec()
"""

# Define your color scheme
primary_color = QColor(100, 149, 237)  # Dodger Blue
secondary_color = QColor(135, 206, 250)  # Sky Blue
text_color = QColor(46, 49, 49)  # Dark Gray

# Create a color palette
palette = QApplication.palette()

# Set colors for different roles
palette.setColor(QPalette.Window, secondary_color)
palette.setColor(QPalette.WindowText, text_color)
palette.setColor(QPalette.Base, secondary_color)
palette.setColor(QPalette.AlternateBase, primary_color)
palette.setColor(QPalette.Button, primary_color)
palette.setColor(QPalette.ButtonText, text_color)
palette.setColor(QPalette.Text, text_color)
palette.setColor(QPalette.Highlight, primary_color)
palette.setColor(QPalette.HighlightedText, text_color)

# Apply the color palette to the application
QApplication.setPalette(palette)

# Update the stylesheet to match the new colors
app.setStyleSheet("QWidget { background-color: %s; }" % secondary_color.name())

"""