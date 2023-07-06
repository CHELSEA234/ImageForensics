from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt
import os

class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # Create the left-hand side layout
        left_layout = QVBoxLayout()

        # Create the top-left image label
        top_left_label = QLabel()
        top_left_label.setAlignment(Qt.AlignCenter)  # Align the image to the center
        top_left_pixmap = QPixmap("asset/image1.jpg")
        top_left_label.setPixmap(top_left_pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(top_left_label)

        # Create the bottom-left image label
        bottom_left_label = QLabel()
        bottom_left_pixmap = QPixmap("asset/image5.jpg")
        bottom_left_label.setPixmap(bottom_left_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(bottom_left_label)

        main_layout.addLayout(left_layout)

        # Create the right-hand side layout
        right_layout = QGridLayout()

        image_folder = "asset"
        image_files = sorted(os.listdir(image_folder))[:8]

        # Iterate over the image files and create labels
        for i, image_file in enumerate(image_files):
            if i == 0:
                continue  # Skip the top-left image, as it has already been added
            label = QLabel()
            pixmap = QPixmap(os.path.join(image_folder, image_file))
            label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            row = (i - 1) // 3  # Calculate the row index (skip the first row)
            col = (i - 1) % 3  # Calculate the column index
            right_layout.addWidget(label, row, col)

        main_layout.addLayout(right_layout)

        self.show()

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
