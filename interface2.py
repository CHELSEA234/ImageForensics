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
        top_left_label.setPixmap(top_left_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(top_left_label)

        # Create the bottom-left image label
        bottom_left_label = QLabel()
        bottom_left_pixmap = QPixmap("asset/image5.jpg")
        bottom_left_label.setPixmap(bottom_left_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(bottom_left_label)

        main_layout.addLayout(left_layout)

        # Create the right-hand side layout
        right_layout = QGridLayout()  # Use QGridLayout for horizontal stacking

        image_folder = "asset"
        image_files = sorted(os.listdir(image_folder))[:8]

        # List of labels for the images
        labels = ["Drop Box", "Feature Map 1", "Feature Map 2", "Feature Map 3",
                  "Feature Map 4", "Binary Mask", "TSNE Result"]

        # Iterate over the image files and create labels
        for i, image_file in enumerate(image_files):
            if i == 0:
                continue  # Skip the top-left image, as it has already been added

            # Create a vertical layout for each image and label
            image_layout = QVBoxLayout()

            # Create the image label
            label = QLabel()
            pixmap = QPixmap(os.path.join(image_folder, image_file))
            label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)  # Align the image to the center
            image_layout.addWidget(label)

            # Create the label below the image
            text_label = QLabel(labels[i - 1])  # Use i-1 to access the corresponding label text
            text_label.setAlignment(Qt.AlignCenter)  # Align the label text to the center
            image_layout.addWidget(text_label)

            row = i // 3  # Calculate the row index
            col = i % 3  # Calculate the column index
            right_layout.addLayout(image_layout, row, col)  # Add the image and label layout to the grid layout

        main_layout.addLayout(right_layout)

        self.show()

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()




"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os


class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # Create the left-hand side layout
        left_layout = QVBoxLayout()

        # Create the gallery box image label
        gallery_box_label = QLabel()
        gallery_box_label.setAlignment(Qt.AlignCenter)  # Align the image to the center
        gallery_box_pixmap = QPixmap("asset/image1.jpg")
        gallery_box_label.setPixmap(gallery_box_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        left_layout.addWidget(gallery_box_label)

        # Create the gallery box label
        gallery_box_label_text = QLabel("Gallery Box")
        gallery_box_label_text.setAlignment(Qt.AlignCenter)  # Align the label text to the center
        left_layout.addWidget(gallery_box_label_text)

        main_layout.addLayout(left_layout)

        # Create the right-hand side layout
        right_layout = QVBoxLayout()

        # Create the upper-right layout for binary mask and TSNE result
        upper_right_layout = QHBoxLayout()

        # Create the binary mask image label
        binary_mask_label = QLabel()
        binary_mask_pixmap = QPixmap("asset/image6.jpg")
        binary_mask_label.setPixmap(binary_mask_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        upper_right_layout.addWidget(binary_mask_label)

        # Create the binary mask label
        binary_mask_label_text = QLabel("Binary Mask")
        binary_mask_label_text.setAlignment(Qt.AlignCenter)  # Align the label text to the center
        upper_right_layout.addWidget(binary_mask_label_text)

        # Create the TSNE result image label
        tsne_result_label = QLabel()
        tsne_result_pixmap = QPixmap("asset/image7.jpg")
        tsne_result_label.setPixmap(tsne_result_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        upper_right_layout.addWidget(tsne_result_label)

        # Create the TSNE result label
        tsne_result_label_text = QLabel("TSNE Result")
        tsne_result_label_text.setAlignment(Qt.AlignCenter)  # Align the label text to the center
        upper_right_layout.addWidget(tsne_result_label_text)

        right_layout.addLayout(upper_right_layout)

        # Create the layout for feature map images and labels
        feature_map_layout = QHBoxLayout()

        image_folder = "asset"
        image_files = sorted(os.listdir(image_folder))[2:6]  # Exclude the gallery box, binary mask, and TSNE result images

        # List of labels for the feature map images
        labels = ["Feature Map 1", "Feature Map 2", "Feature Map 3", "Feature Map 4"]

        # Iterate over the image files and create labels
        for image_file, label in zip(image_files, labels):
            # Create a vertical layout for each image and label
            image_layout = QVBoxLayout()

            # Create the image label
            image_label = QLabel()
            pixmap = QPixmap(os.path.join(image_folder, image_file))
            image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            image_layout.addWidget(image_label)

            # Create the label below the image
            label_text = QLabel(label)
            label_text.setAlignment(Qt.AlignCenter)  # Align the label text to the center
            image_layout.addWidget(label_text)

            feature_map_layout.addLayout(image_layout)

        right_layout.addLayout(feature_map_layout)

        main_layout.addLayout(right_layout)

        self.show()

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
"""

