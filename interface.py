import os
import cv2
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, QPropertyAnimation, QPoint, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont, QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, \
    QListView, QAbstractItemView

class ThumbnailView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(100, 100))  # Default thumbnail size

    def updateThumbnailSize(self, size):
        self.setIconSize(QSize(size, size))

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.center_window()

        self.label_2 = QLabel(self)
        self.label_2.setPixmap(QPixmap('asset/sample_1.jpg'))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setScaledContents(True)
        self.label_2.setMinimumSize(400, 300)  # Adjust the size as needed
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
        self.play_init_sound()

    def play_init_sound(self):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile("/Users/noel/Desktop/1103 N Oak Terr.wav"))
        sound.play()

    def center_window(self):
        screen_geometry = QApplication.screens()[0].geometry()
        window_geometry = QRect(screen_geometry.center().x() - 350, screen_geometry.center().y() - 250, 700, 500)
        self.setGeometry(window_geometry)

    def show_welcome_screen(self):
        self.image_label.setVisible(False)
        self.select_button.setVisible(False)
        self.ok_button.setVisible(False)
        self.timer.start(2500)

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

        thumbnail_view = ThumbnailView(file_dialog)
        thumbnail_view.setViewMode(QListView.IconMode)  # Set the custom view mode
        thumbnail_view.updateThumbnailSize(100)  # Set the thumbnail size (adjust as needed)
        file_dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)  # Hide the filter details

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

        # Retrieve the filename for tooltip display
        filename = os.path.basename(image_path)

        # Set the tooltip with a larger image preview
        self.image_label.setToolTip(f'<html><img src="{image_path}" width="500" height="500"></html>')

        image_array = cv2.imread(image_path)
        if image_array is not None:
            self.selected_image_array = image_array
            self.ok_button.setEnabled(True)
            self.ok_button.setVisible(True)
            print("Selected Image Array:")
            self.image_path = image_path
        else:
            print("Failed to read the image file.")
        return self.selected_image_array

    def confirm_selection(self):
        self.secondW = MyGUI()
        self.secondW.show()
        self.secondW.label_2.setPixmap(QPixmap(self.image_path))
        self.hide()

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
