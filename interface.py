import cv2
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
from usage import analysis

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

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False) 
        self.ok_button.setVisible(False) 

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.select_button)

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
        self.image_label.clear()
        self.image_label.setPixmap(scaledPixmap)
        self.image_label.setText("")
        self.image_label.adjustSize()

        self.resize(image.width(), image.height())

        # Convert QPixmap to numpy array
        image_array = cv2.imread(image_path)
        if image_array is not None:
            self.selected_image_array = image_array
            # Print the array shape and content
            self.ok_button.setEnabled(True) 
            self.ok_button.setVisible(True)
            print("Selected Image Array:")
            print(self.selected_image_array)

            binary_mask = analysis(self.selected_image_array)
            binary_mask.save('pred_mask.png')
            
        else:
            print("Failed to read the image file.")

        return image_array

    def confirm_selection(self): 
        if self.selected_image_array is not None: 
            self.clear_image()

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
    window.show()
    app.exec()
