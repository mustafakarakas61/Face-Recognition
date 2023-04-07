from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.resources.Environments import pngDelete


class DeleteModel(QWidget):
    def __init__(self, mainWidget):
        super(DeleteModel, self).__init__()
        self.mainWidget = mainWidget

    def modelDeleteScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()