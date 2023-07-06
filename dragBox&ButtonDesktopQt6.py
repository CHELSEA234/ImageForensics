import cv2
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QWidget, QFrame, QVBoxLayout


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        # Enable drop functionality
        self.setAcceptDrops(True)

        self.image_label = QLabel(self)
        # Center-align the label
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_label)

        self.placeholder_text = "Drag and drop an image or click the button below to select"
        self.image_label.setText(self.placeholder_text)
        # Set font
        self.image_label.setFont(QFont("Arial", 12, weight=QFont.Weight.Light))

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)

        placeholder_layout = QHBoxLayout()

        self.placeholder_frames = []
        for _ in range(3):
            frame = QFrame(self)
            frame.setFixedSize(100, 100)
            frame.setStyleSheet("background-color: lightgray;")
            frame.setLayout(QVBoxLayout())  # Set a layout for the frame
            self.placeholder_frames.append(frame)
            placeholder_layout.addWidget(frame)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.select_button)
        layout.addLayout(placeholder_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.selected_image_array = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            # Accept drag event if it contains URLs
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            # Get local file path from the dropped URL
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
                # Call the display_image method to display the selected image
                self.display_image(image_path)

    def display_image(self, image_path: str):
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)

        maxWidth = 800
        maxHeight = 600

        scaledPixmap = pixmap.scaled(maxWidth, maxHeight, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaledPixmap)
        self.image_label.setText("")
        self.image_label.adjustSize()

        self.resize(image.width(), image.height())

        # Clear previous placeholder images
        for frame in self.placeholder_frames:
            frame.setStyleSheet("background-color: lightgray;")
            frame.layout().takeAt(0)  # Remove any existing widgets from the layout

        # Scale and display the image in each placeholder frame
        for frame in self.placeholder_frames:
            scaledPixmap = pixmap.scaled(frame.width(), frame.height(), Qt.AspectRatioMode.KeepAspectRatio)
            label = QLabel(frame)
            label.setPixmap(scaledPixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setScaledContents(True)
            frame.layout().addWidget(label)

        temp_file_path = "temp_image.png"
        image.save(temp_file_path)

        image_array = cv2.imread(temp_file_path)

        self.selected_image_array = image_array

        return image_array


if __name__ == "__main__":
    app = QApplication([])
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.show()

    app.exec()
