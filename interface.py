import cv2
from PyQt5.QtCore import Qt, QMimeData, QPropertyAnimation, QPoint
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PIL import Image

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.center_window()

        self.label_2 = QLabel(self)
        self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label = QLabel('fake', self)
        self.label_3 = QLabel(self)
        self.label_3.setPixmap(QPixmap('pred_mask.png'))
        self.label_4 = QLabel(self)
        self.label_4.setPixmap(QPixmap('result_tsne.png'))
        self.label_5 = QLabel(self)
        self.label_5.setPixmap(QPixmap('result_feat_32.png'))
        self.label_6 = QLabel(self)
        self.label_6.setPixmap(QPixmap('result_feat_64.png'))
        self.label_7 = QLabel(self)
        self.label_7.setPixmap(QPixmap('result_feat_128.png'))
        self.label_8 = QLabel(self)
        self.label_8.setPixmap(QPixmap('result_feat_256.png'))

        layout = QVBoxLayout()
        layout.addWidget(self.label_2)
        layout.addWidget(self.label)
        layout.addWidget(self.label_3)
        layout.addWidget(self.label_4)
        layout.addWidget(self.label_5)
        layout.addWidget(self.label_6)
        layout.addWidget(self.label_7)
        layout.addWidget(self.label_8)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)
        self.select_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            """
        )
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_selection)
        self.ok_button.setEnabled(False)
        self.ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.select_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.selected_image_array = None

        self.show_welcome_screen()

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.setGeometry(window_geometry)

    def show_welcome_screen(self):
        self.image_label.setVisible(False)
        self.select_button.setVisible(False)
        self.ok_button.setVisible(False)

    def show_image_selection_screen(self):
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

        self.ok_button.setEnabled(True)
        self.ok_button.setVisible(True)

    def confirm_selection(self):
        self.secondW = MyGUI()

if __name__ == "__main__":
    app = QApplication([])
    
    # stylesheet of the app
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #F5F5F5;
        }
        
        QLabel {
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 5px;
            padding: 10px;
        }
        """
    )
    
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.ok_button.move(10, 50)
    window.show()
    app.exec()
