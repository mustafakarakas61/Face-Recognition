import os.path

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox

from src.main.python.services.FeaturesService import getLabelFeatures, fontTextBox, getButtonFeaturesTrain, \
    getMsgBoxFeatures
from src.resources.Environments import pngAdd, pathDatasets, pngInfoBox, pngWarningBox


class NewDataset(QWidget):
    def __init__(self, mainWidget):
        super(NewDataset, self).__init__()
        self.newDatasetName = None
        self.window = None
        self.mainWidget = mainWidget

    def newDatasetScreen(self):
        mainWidth = 300
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yeni Veriseti')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngAdd))

        # TextBox
        labelNewDataset = getLabelFeatures(QLabel("<b>Yeni Veriseti Adı</b>"), False, True)
        textBoxNewDataset = QLineEdit()
        textBoxNewDataset.setValidator(QRegExpValidator(QRegExp("[a-zA-Z]+")))
        textBoxNewDataset.setFixedSize(150, 30)
        textBoxNewDataset.setFont(fontTextBox)
        textBoxNewDataset.textChanged.connect(
            lambda index: self.onTextBoxInputNewDataset(textBoxNewDataset.text(), self.mainWidget.comboDatasets))
        btnNewDataset = getButtonFeaturesTrain(QPushButton(self), text="Ekle")
        btnNewDataset.clicked.connect(lambda: self.addNewDataset())

        layoutVNewDataset = QVBoxLayout()
        layoutVNewDataset.addWidget(labelNewDataset, alignment=Qt.AlignCenter)
        layoutVNewDataset.addWidget(textBoxNewDataset, alignment=Qt.AlignCenter)
        layoutVNewDataset.addWidget(btnNewDataset, alignment=Qt.AlignCenter)

        # Ana düzenleyici
        layout = QVBoxLayout()
        layout.addLayout(layoutVNewDataset)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)
        self.window.show()

    def addNewDataset(self):
        if self.newDatasetName is not None and len(self.newDatasetName) > 2:
            newDataset: str = str(self.newDatasetName) + "_v"
            i: int = 1
            j: int = 1
            finalDatasetName: str = newDataset + str(i)
            if os.path.exists(pathDatasets + finalDatasetName):
                while True:
                    if j < 10:
                        finalDatasetName = newDataset + str(i) + "." + str(j)
                        j = j + 1
                    else:
                        i = i + 1
                        j = 1
                        finalDatasetName = newDataset + str(i) + "." + str(j)
                    if not os.path.exists(pathDatasets + finalDatasetName):
                        break

                os.makedirs(pathDatasets + finalDatasetName)
                self.mainWidget.updateDatasetList()
                getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi",
                                  "<b>"+finalDatasetName + "</b> veriseti başarıyla eklendi.",
                                  QMessageBox.Information,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            else:
                os.makedirs(pathDatasets + finalDatasetName)
                self.mainWidget.updateDatasetList()
                getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi",
                                  "<b>" + finalDatasetName + "</b> veriseti başarıyla eklendi.",
                                  QMessageBox.Information,
                                  QMessageBox.Ok, isQuestion=False).exec_()
        else:
            getMsgBoxFeatures(
                QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen geçerli bir veriseti ismi girin.",
                QMessageBox.Warning,
                QMessageBox.Ok, isQuestion=False).exec_()

    def onTextBoxInputNewDataset(self, inputText: str, comboDatasets: QComboBox):
        # if comboDatasets.count() > 0:
        #     comboDatasets.setCurrentIndex(0)
        self.newDatasetName = inputText
