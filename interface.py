import cv2
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5 import uic
from PIL import Image

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.label.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label.setText('fake')
        self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))

    def update_images(self, image_path):
        binary_mask = generate_binary_mask(image_path)
        feature_map_1 = generate_feature_map_1(image_path)
        feature_map_2 = generate_feature_map_2(image_path)
        feature_map_3 = generate_feature_map_3(image_path)
        feature_map_4 = generate_feature_map_4(image_path)
        tsne_result = generate_tsne_result(image_path)

        self.label_3.setPixmap(QPixmap.fromImage(binary_mask))
        self.label_4.setPixmap(QPixmap.fromImage(tsne_result))
        self.label_5.setPixmap(QPixmap.fromImage(feature_map_1))
        self.label_6.setPixmap(QPixmap.fromImage(feature_map_2))
        self.label_7.setPixmap(QPixmap.fromImage(feature_map_3))
        self.label_8.setPixmap(QPixmap.fromImage(feature_map_4))


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_path = None
        self.setCentralWidget(self.image_label)

        self.placeholder_text = "Drag and drop an image or click the button below to select"
        self.image_label.setText(self.placeholder_text)
        self.image_label.setFont(QFont("Arial", 12, weight=QFont.Weight.Light))

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False)
        self.ok_button.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.select_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.selected_image_array = None

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

        maxWidth = 800
        maxHeight = 600

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
        else:
            print("Failed to read the image file.")
        return self.selected_image_array

    def confirm_selection(self):
        self.secondW = MyGUI()
        self.secondW.show()
        self.secondW.update_images(self.image_path)

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
    app.exec_()
