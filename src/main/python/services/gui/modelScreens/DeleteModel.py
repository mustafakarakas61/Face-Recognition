import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout

from src.main.python.services.FeaturesService import getComboBoxFeatures, getButtonFeaturesDelete
from src.resources.Environments import pngDelete, pathModels


class DeleteModel(QWidget):
    def __init__(self, mainWidget):
        super(DeleteModel, self).__init__()
        self.mainWidget = mainWidget
        self.selectedDeleteModel = "Silinecek Modeli Seçiniz"

    def modelDeleteScreen(self):
        mainWith = 400
        mainHeight = 100
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # ComboBox ayarı
        # Dizin içindeki .h5 uzantılı dosyaları bulma
        modelFiles = [f for f in os.listdir(pathModels) if f.endswith('.h5')]
        # Dosya isimlerinden model adlarını ayırma
        modelNames = ['Silinecek Modeli Seçiniz'] + [os.path.splitext(f)[0] + ".h5" for f in modelFiles]
        # ComboBox oluşturma ve model isimlerini ekleme
        comboDeleteModel = getComboBoxFeatures(QComboBox(self))
        comboDeleteModel.addItems(modelNames)
        comboDeleteModel.currentIndexChanged.connect(lambda index: self.onComboboxSelection(comboDeleteModel.itemText(index)))

        btnDeleteModel = getButtonFeaturesDelete(QPushButton(self), text="Sil")

        # Ana düzenleyici
        layoutV = QVBoxLayout()
        layoutV.addWidget(comboDeleteModel)

        layoutH = QHBoxLayout()
        layoutH.addWidget(btnDeleteModel)

        layoutV.addLayout(layoutH)
        self.window.setLayout(layoutV)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    # Seçili olan modelin adını alma
    def onComboboxSelection(self, modelName):
        self.selectedDeleteModel = modelName