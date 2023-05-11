from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.resources.Environments import pngFolder


class LocalFile(QWidget):
    def __init__(self, mainWidget):
        super(LocalFile, self).__init__()
        self.window = None
        self.mainWidget = mainWidget

    def faceAddLocalFileScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yerelden Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngFolder))

        # # Çarpı işaretine basıldığında eski pencere açılsın
        # self.window.setAttribute(
        #     QtCore.Qt.WA_DeleteOnClose)
        # self.window.destroyed.connect(self.mainWidget.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def closeScreen(self):
        if self.window is not None:
            self.window.close()
