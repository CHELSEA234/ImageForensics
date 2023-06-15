import sys
"""
Classes that are used for creating GUI components of the application
"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QVBoxLayout, QWidget
"""
Qt provides various constants and enums that are used in PyQt5 applications, such as alignment flags and drop actions
"""
from PyQt5.QtCore import Qt, QMimeData

from PyQt5.QtGui import QPixmap


from PyQt5.QtWidgets import QPushButton




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Analysis Application")

        # Create the drag box label
        self.dragLabel = QLabel("Drag and drop image here", self)
        self.dragLabel.setAlignment(Qt.AlignCenter)
        # label with a dashed border - width 2 pixels
        self.dragLabel.setStyleSheet("QLabel { border: 2px dashed }")
        # Allows for label to accept drop events (when an item is dragged and dropped onto it)
        self.dragLabel.setAcceptDrops(True)
        self.setCentralWidget(self.dragLabel)
        self.resize(500, 500)


        # create a label for the mask visualization
        # QLabel is a simple text or image display area in PyQt5
        # Aligns the content to be displayed in the center
        self.maskLabel = QLabel(self)
        self.maskLabel.setAlignment(Qt.AlignCenter)

        """
        Create a layout to hold the labels
        QVBoxLayout is a layout manager that arranges widgets vertically, one on top of the other 
        These lines add the self.dragLabel and self.maskLabel widgets to the layout created earlier.
        The addWidget() method is used to add widgets to a layout. In this case, the dragLabel and 
        maskLabel widgets are added to the vertical layout, layout.
        """
        layout = QVBoxLayout()
        layout.addWidget(self.dragLabel)
        layout.addWidget(self.maskLabel)

        # Create a central widget and set the layout
        # By setting the layout for the central widget, you're specifying
        # how the child widgets (dragLabel and maskLabel) should be arranged within the central widget.
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.centralWidget().setLayout(layout)

        # Connect the drag events
        # This method is called when a drag event enters the widget (graphical component or element
        # that can be displayed and interacted with in the graphical user interface (GUI))
        self.dragLabel.dragEnterEvent = self.dragEnterEvent
        self.dragLabel.dragMoveEvent = self.dragMoveEvent
        self.dragLabel.dragLeaveEvent = self.dragLeaveEvent
        self.dragLabel.dropEvent = self.dropEvent

        # Create the gallery button

        self.galleryButton = QPushButton("Gallery", self)
        self.galleryButton.clicked.connect(self.openGallery)
        layout.addWidget(self.galleryButton)

    def displayResult(self, analysisResult):
        """
         imageDecision = analysisResult['imageDecision']
        localizationResult = analysisResult['localizationResult']

        #update the GUI labels with the results
        self.dragLabel.setText(f"Image Decision: {imageDecision}")

        # Fit the mask visualization within the window
        self.fitMaskInWindow(localizationResult)

        :param analysisResult:
        :return:
        """
        pass

    def openGallery(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog

        folderDialog = QFileDialog.getExistingDirectory(self, "Open Gallery", "", options=options)
        if folderDialog:
            print("Selected folder", folderDialog)

    def dragEnterEvent(self, event):
        # Checks if the dragged data has one or more URLs
        if event.mimeData().hasImage():
            event.acceptProposedAction()

        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

        #  Method is called when a drag event moves within the widget.
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()
    # when a drag event leaves the widget, nothing will happen or change
    # in the user interface as a result of this method.
    def dragLeaveEvent(self, event):
        pass
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()

            # Get the file path of the dropped image
            filePath = event.mimeData().urls()[0].toLocalFile()

            # Perform image analysis and display results
            analysisResult = self.analyzeImage(filePath)
            self.displayResult(analysisResult)
    #  responsible for opening a file dialog window to allow the
    #  user to select an image file from their local system.

        if event.mimeData().hasImage():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            image = event.mimeData().imageData()
            pixmap = QPixmap.fromImage(image)
            self.displayImage(pixmap)
        else:
            event.ignore()

    def displayImage(self, pixmap):
        self.dragLabel.setPixmap(pixmap.scaled(self.dragLabel.size(), Qt.KeepAspectRatio))
    def openFileDialog(self):
        fileDialog = QFileDialog()
        # method is called on the file dialog object to set the mode to ExistingFile, which means
        # the user can only select existing files, not create new ones.
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        """
        method is called on the file dialog object to display the file dialog window and
        wait for the user's interaction. If the user selects one or more files and clicks the "Open" button,
        the if fileDialog.exec(): condition will evaluate to True.
        """
        if fileDialog.exec():
            filePaths = fileDialog.selectedFiles()
            # If there is at least one selected file (0 < len(filePaths)), the first
            # file path (filePaths[0]) is extracted and stored in the filePath variable.
            if 0 < len(filePaths):
                filePath = filePaths[0]
                # method is called with the selected filePath as an argument to perform image analysis,
                # and the displayResults method is called to display the analysis results in the user interface.
                analysisResult = self.analyzeImage(filePath)
                self.displayResult(analysisResult)


    def analyzeImage(self, filePath):
        """
        :param filePath:
        :return:

        Image preprocessing
        Implement image preprocessing steps here

        Feature extraction
        Implement feature extraction pipeline

        Classification
        Implement image classification module here

        Localization
        Implement image localization module here

        Return the analysis results as a dictionary
        """
        # Placeholder implementation for demonstration purposes
        return {
            'imageDecision': 'Real',  # Placeholder result, replace with actual decision
            'localizationResult': [(100, 100, 200, 200)] # Placeholder result, replace with actual localization
        }

    def fitMaskInWindow(self, localizationResult):
        """
        Calculates the minimum and maximum coordinates of the box enclosing the mask.
        It iterates over the 'localizationResult', which is a list of tuples
        (x, y, width, height) for each mask. Min and Max values are determined separately
        for the x coordinates, y coordinates, and sum of x coordinate and width, and y coordinate
        and height respectively. This provides the boundary of the mask in terms of its position and size
        :param localizationResult:
        :return:
        """
        minX = min([x for (x, y, width, height) in localizationResult])
        minY = min([y for (x, y, width, height,) in localizationResult])
        maxX = max([x + width for (x, y, width, height) in localizationResult])
        maxY = max([y + height for (x, y, width, height) in localizationResult])

        # Calculate the dimensions of the bounding box
        boxWidth = maxX - minX
        boxHeight = maxY - minY

        # Represents window where widget is being displayed
        windowWidth = self.maskLabel.width()
        windowHeight = self.maskLabel.height()


        """
        Calculate the scale factor to fit the box within the window
        Scale ensures that the entire mask fits within the window while
        maintaining its aspect ratio  
        """
        scaleFactor = min(windowWidth / boxWidth, windowHeight / boxHeight )
        """
        Coordiantes and dimensions of each mask in localization result are scaled according to the 
        calculated scale factor. The scaling is performed by multiplying the differences between 
        the original coordinates and minimum values. Resulting scaled coordinates and dimensions are added 
        to the scaledLocalizationResult list. 
        """
        # Scale the bounding box coordinates
        scaledLocalizationResult = []
        for (x, y, width, height) in localizationResult:
            scaledX = int((x - minX) * scaleFactor)
            scaledY = int((y - minY) * scaleFactor)
            scaledWidth = int(width * scaleFactor)
            scaledHeight = int(height * scaleFactor)

            scaledLocalizationResult.append((scaledX, scaledY, scaledWidth, scaledHeight))

        # Update the GUI to display the mask using the scaled coordinates and dimensions
        self.displayMask(scaledLocalizationResult)

if __name__ == '__main__':
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())





