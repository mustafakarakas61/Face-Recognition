from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton, QHBoxLayout

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, getTextBoxSuccessRateFeatures, \
    getButtonFeaturesTrain
from src.resources.Environments import pngFolder, pngWarningBox, pathDatasets, pngInfoBox, pngAdd
from utils.Utils import dataCount


class LocalFile(QWidget):
    def __init__(self, mainWidget):
        super(LocalFile, self).__init__()
        self.startSaveWindow = None
        self.textboxDataInfoCount = None
        self.saveStatus: bool = False
        self.saveData = None

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
            mainWidth = 530
            mainHeight = 180
            screen = QtWidgets.QApplication.desktop().screenGeometry()
            screenWidth, screenHeight = screen.width(), screen.height()

            self.window = QWidget()
            self.window.setWindowTitle('Yerelden Ekle')
            self.window.setStyleSheet("background-color: white;")
            self.window.setWindowIcon(QIcon(pngFolder))

            labelDataInfo: QLabel = getLabelFeatures(QLabel(), False, True)
            labelDataInfo.setText(
                "<b><i>\"</i>" + datasetName + "</b> verisetinden <b>" + datasetDataName + "</b> verisi<b><i>\"</i></b>")

            labelDataCount: QLabel = getLabelFeatures(QLabel(), False, True)
            labelDataCount.setText("<b>Mevcut Adet</b>")

            self.textboxDataInfoCount: QLineEdit = getTextBoxSuccessRateFeatures(QLineEdit(), None, isEnabled=False,
                                                                                 isVisible=False)
            self.textboxDataInfoCount.setStyleSheet("background-color: white; color:black; text-align:center;")
            self.textboxDataInfoCount.setFixedSize(40, 40)
            self.textboxDataInfoCount.setText(str(dataCount(pathDatasets + datasetName + "/" + datasetDataName)))

            btnAddData: QPushButton = getButtonFeaturesTrain(QPushButton(self), text="Başlat")
            btnAddData.clicked.connect(
                lambda: self.startSaveProcess(str(datasetName), str(datasetDataName)))

            layoutV = QVBoxLayout()
            layoutV.addWidget(labelDataInfo)
            layoutCountV = QVBoxLayout()
            layoutCountV.addWidget(labelDataCount)
            layoutCountV.addWidget(self.textboxDataInfoCount)
            layoutCountV.setAlignment(labelDataCount, Qt.AlignCenter)
            layoutCountV.setAlignment(self.textboxDataInfoCount, Qt.AlignCenter)
            layoutV.addLayout(layoutCountV)
            layoutV.addWidget(btnAddData)
            layoutV.setAlignment(labelDataInfo, Qt.AlignCenter)
            layoutV.setAlignment(btnAddData, Qt.AlignCenter)

            layoutH = QHBoxLayout()
            layoutH.addLayout(layoutV)


            # Ana düzenleyici
            layout = QVBoxLayout()
            layout.addLayout(layoutH)

            self.window.setLayout(layout)
            self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWidth, mainHeight)
            self.window.show()
            self.textboxDataInfoCount.setVisible(True)

    def startSaveProcess(self, datasetName: str, datasetDataName: str):
        getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi",
                          "Her yeni bir yüz kaydı için <b>Kaydet</b> butonuna tıklayınız.",
                          QMessageBox.Information,
                          QMessageBox.Ok, isQuestion=False).exec_()

        mainWidth = 220
        mainHeight = 170
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.startSaveWindow = QWidget()
        self.startSaveWindow.setWindowTitle('Kaydet')
        self.startSaveWindow.setStyleSheet("background-color: white;")
        self.startSaveWindow.setWindowIcon(QIcon(pngAdd))

        self.saveData: QPushButton = QPushButton(self)
        self.saveData.setFont(QtGui.QFont("Times New Roman", 20))
        self.saveData.setText("Kaydet")
        self.saveData.setFixedSize(200, 150)
        self.saveData.setStyleSheet("background-color: #44d091; color: white; font-weight: bold;")
        self.saveData.clicked.connect(lambda: self.saveFace())

        # Ana düzenleyici
        layoutStartSave = QHBoxLayout()
        layoutStartSave.addWidget(self.saveData)
        layoutStartSave.setAlignment(self.saveData, Qt.AlignCenter)

        self.startSaveWindow.setLayout(layoutStartSave)
        self.startSaveWindow.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                         int(screenHeight / 2 - int(mainHeight / 2)),
                                         mainWidth, mainHeight)
        self.startSaveWindow.closeEvent = self.onClosedSaveProcess
        self.startSaveWindow.show()
        self.addFaceFromLocal(datasetName, datasetDataName)

    def onClosedSaveProcess(self, event):
        if not self.mainWidget.getIsMainScreenClosing():
            reply = getMsgBoxFeatures(QMessageBox(), pngWarningBox, "Dikkat!",
                                      'Kaydet işlemi bitirilsin mi?',
                                      QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                      isQuestion=True).exec_()
            if reply == QtWidgets.QMessageBox.Yes:
                # self.closeCameraStatus = True
                event.accept()
            else:
                event.ignore()

    def saveFace(self):
        # self.closeCameraStatus = False
        self.saveStatus = True

    def addFaceFromLocal(self, datasetName: str, datasetDataName: str):
        print()

    def updateCount(self, datasetName: str, datasetDataName: str):
        newCount: int = dataCount(pathDatasets + datasetName + "/" + datasetDataName)
        if self.textboxDataInfoCount is not None:
            self.textboxDataInfoCount.setText(str(newCount))

    def closeScreen(self):
        if self.window is not None:
            self.window.close()
