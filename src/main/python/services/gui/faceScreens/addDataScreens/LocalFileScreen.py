from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from src.main.python.services.FeaturesService import getMsgBoxFeatures
from src.resources.Environments import pngFolder, pngWarningBox


class LocalFile(QWidget):
    def __init__(self, mainWidget):
        super(LocalFile, self).__init__()
        self.window = None
        self.mainWidget = mainWidget

    def faceAddLocalFileScreen(self):
        datasetName: str = self.mainWidget.selectedDatasetName
        datasetDataName: str = self.mainWidget.selectedDatasetDataName
        if datasetName.__eq__("Veriseti Seçiniz") or datasetDataName.__eq__(
                "Veri Seçiniz") or datasetName is None or datasetDataName is None:
            if datasetName.__eq__("Veriseti Seçiniz") or datasetName is None:
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir <b>veriseti</b> seçin",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            if not datasetName.__eq__("Veriseti Seçiniz") or datasetName is not None:
                if datasetDataName.__eq__("Veri Seçiniz") or datasetDataName is None:
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir <b>veri</b> seçin",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
        else:
            mainWidth = 300
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
            self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWidth, mainHeight)
            self.window.show()

    def closeScreen(self):
        if self.window is not None:
            self.window.close()
