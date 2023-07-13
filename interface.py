import os
import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
from pydub import AudioSegment
from pydub.playback import play

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

class AudioPlaybackThread(QThread):
    finished_playing = pyqtSignal()

    def __init__(self, sound_file_path):
        super().__init__()
        self.sound_file_path = sound_file_path

    def run(self):
        audio = AudioSegment.from_wav(self.sound_file_path)
        play(audio)
        self.finished_playing.emit()

    def finish(self):
        self.finished_playing.emit()

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setAcceptDrops(True)

        self.center_window()


        # Get the directory path of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the sound file relative to the script directory
        sound_file_path = os.path.join(script_directory, "/home/cvlab/Downloads/interfaceAudio.wav")

        self.sound_file_path = sound_file_path

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

        #self.animation.finished.connect(self.play_init_sound)
        self.start_audio_playback()
        self.animation.start()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.image_label.setVisible(False)
        self.select_button.setVisible(False)
        self.ok_button.setVisible(False)
        self.welcome_label.setVisible(True)
        self.timer.stop()
        self.animation.start()
        #self.play_init_sound()

    def start_audio_playback(self):
        self.welcome_label.setVisible(True)
        self.image_label.setVisible(True)
        self.select_button.setVisible(True)
        self.ok_button.setVisible(True)
        self.audio_thread = AudioPlaybackThread(self.sound_file_path)
        self.audio_thread.finished_playing.connect(self.show_image_selection_screen)
        self.audio_thread.start()

    def play_init_sound(self):
        audio = AudioSegment.from_wav(self.sound_file_path)
        play(audio)

    def timer_timeout(self):
        self.timer.stop()
        self.image_label.setVisible(True)
        self.select_button.setVisible(True)
        self.ok_button.setVisible(True)

    def center_window(self):
        screen_geometry = QApplication.screens()[0].geometry()
        window_geometry = QRect(screen_geometry.center().x() - 350, screen_geometry.center().y() - 250, 700, 500)
        self.setGeometry(window_geometry)

    def show_image_selection_screen(self):
        self.welcome_label.setVisible(False)
        self.image_label.setVisible(True)
        self.select_button.setVisible(True)
        self.ok_button.setVisible(True)
        self.image_label.setText("Drag and drop an image or click the button below to select")
        self.timer.start(2000)
        self.animation.start()
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
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.select_button.move(10, 10)
    window.ok_button.move(10, 50)
    window.show()
    sys.exit(app.exec_())
