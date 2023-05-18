import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox

from src.main.python.services.FeaturesService import getLabelFeatures, fontTextBox, getButtonFeaturesTrain, \
    getMsgBoxFeatures
from src.resources.Environments import pngAdd, pathDatasets, pngInfoBox, pngWarningBox


class NewDatasetData(QWidget):
    def __init__(self, mainWidget):
        super(NewDatasetData, self).__init__()
        self.newDatasetDataName = None
        self.window = None
        self.mainWidget = mainWidget

    def newDatasetDataScreen(self):
        mainWidth = 300
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yeni Veri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngAdd))

        # TextBox
        labelNewDatasetData = getLabelFeatures(QLabel("<b>Yeni Veri Adı</b>"), False, True)
        textBoxNewDatasetData = QLineEdit()
        textBoxNewDatasetData.setValidator(QRegExpValidator(QRegExp("[a-zA-ZçğıöşüÇĞİÖŞÜ\s]+")))
        textBoxNewDatasetData.setFixedSize(150, 30)
        textBoxNewDatasetData.setFont(fontTextBox)
        textBoxNewDatasetData.textChanged.connect(
            lambda index: self.onTextBoxInputNewDatasetData(textBoxNewDatasetData.text(),
                                                            self.mainWidget.comboDatasetsData))
        btnNewDatasetData = getButtonFeaturesTrain(QPushButton(self), text="Ekle")
        btnNewDatasetData.clicked.connect(lambda: self.addNewDatasetData())

        layoutVNewDatasetData = QVBoxLayout()
        layoutVNewDatasetData.addWidget(labelNewDatasetData, alignment=Qt.AlignCenter)
        layoutVNewDatasetData.addWidget(textBoxNewDatasetData, alignment=Qt.AlignCenter)
        layoutVNewDatasetData.addWidget(btnNewDatasetData, alignment=Qt.AlignCenter)

        # Ana düzenleyici
        layout = QVBoxLayout()
        layout.addLayout(layoutVNewDatasetData)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)
        self.window.show()

    def addNewDatasetData(self):
        if self.newDatasetDataName is not None and len(self.newDatasetDataName) > 2 and not self.mainWidget.selectedDatasetName.__eq__("Veriseti Seçiniz"):
            selectedDataset: str = self.mainWidget.selectedDatasetName
            if not selectedDataset.__eq__("Veriseti Seçiniz"):
                if not os.path.exists(pathDatasets + selectedDataset + "/" + self.newDatasetDataName):
                    os.makedirs(pathDatasets + selectedDataset + "/" + self.newDatasetDataName)
                    self.mainWidget.updateDatasetList()
                    getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi",
                                      "<b>"+selectedDataset + "</b> veriseti altına başarıyla <b><i>\"" + self.newDatasetDataName + "\"</i></b> verisi eklendi.",
                                      QMessageBox.Information,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                else:
                    getMsgBoxFeatures(
                        QMessageBox(self), pngWarningBox, "Uyarı",
                        "<b>"+selectedDataset + "</b> veriseti altında bu isim zaten mevcut : <b><i>\"" + self.newDatasetDataName + "\"</i></b>",
                        QMessageBox.Warning,
                        QMessageBox.Ok, isQuestion=False).exec_()
            else:
                getMsgBoxFeatures(
                    QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen geçerli bir veri ismi girin.",
                    QMessageBox.Warning,
                    QMessageBox.Ok, isQuestion=False).exec_()
        else:
            getMsgBoxFeatures(
                QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen geçerli bir veri ismi girin.",
                QMessageBox.Warning,
                QMessageBox.Ok, isQuestion=False).exec_()

    def onTextBoxInputNewDatasetData(self, inputText: str, comboDatasetsData: QComboBox):
        # if comboDatasetsData.count() > 0:
        #     comboDatasetsData.setCurrentIndex(0)
        self.newDatasetDataName = inputText
