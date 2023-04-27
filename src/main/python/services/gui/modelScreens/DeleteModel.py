import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QTableWidget, QCheckBox, \
    QMessageBox

from src.main.python.PostgreSQL import removeFromDB, listModels
from src.main.python.services.FeaturesService import getComboBoxFeatures, getButtonFeaturesDelete
from src.resources.Environments import pngDelete, pathModels, pngTrash, pathFaceOutputs, pathFaceMaps, pathEyeOutputs, \
    pathEyeMaps


class DeleteModel(QWidget):
    def __init__(self, mainWidget):
        super(DeleteModel, self).__init__()
        self.mainWidget = mainWidget

    def modelDeleteScreen(self):
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        models = listModels()
        modelNames = [model["model_name"] for model in models]
        modelIds = [model["id"] for model in models]

        mainWith = 500
        if len(modelNames) <= 10:
            mainHeight = 230
        else:
            mainHeight = 410

        # ComboBox oluşturma ve model isimlerini ekleme
        comboDeleteModel = getComboBoxFeatures(QComboBox(self))
        comboDeleteModel.addItems(modelNames)
        comboDeleteModel.currentIndexChanged.connect(
            lambda index: self.onComboboxSelection(comboDeleteModel.itemText(index)))

        btnDeleteModel = getButtonFeaturesDelete(QPushButton(self), text="Sil")
        btnDeleteModel.clicked.connect(lambda: self.deleteSelectedCheckBox(table, comboDeleteModel))

        # QTableWidget oluşturma
        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(len(modelNames))  # tablo satır sayısı combobox seçeneklerinin sayısı kadar olacak

        table.setHorizontalHeaderLabels(["id", "Model Listesi", ""])  # tablo başlığı
        table.setMinimumSize(480, 180)  # tablonun minimum boyutu width, height
        table.setMaximumSize(480, 335)  # tablonun maksimum boyutu width, height
        table.setColumnWidth(0, 20)
        table.setColumnWidth(1, 360)
        table.setColumnWidth(2, 20)
        table.horizontalHeaderItem(0).setFont(QFont("Arial", 15, QFont.Bold))
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        table.horizontalHeaderItem(1).setFont(QFont("Arial", 15, QFont.Bold))
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        table.horizontalHeaderItem(2).setIcon(QIcon(pngTrash))
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for i in range(len(modelNames)):
            itemId = QtWidgets.QTableWidgetItem(str(modelIds[i]))
            itemId.setFont(QFont("Times New Roman", 13))
            table.setItem(i, 0, itemId)

            itemName = QtWidgets.QTableWidgetItem(modelNames[i])
            itemName.setFont(QFont("Times New Roman", 13))
            table.setItem(i, 1, itemName)

            itemCheckbox = QCheckBox()
            table.setCellWidget(i, 2, itemCheckbox)

        # Ana layout oluşturma
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)

        # Tabloyu içeren layout
        layoutTable = QHBoxLayout()
        layoutTable.addWidget(table)
        mainLayout.addLayout(layoutTable)

        # Butonu içeren layout
        layoutButton = QHBoxLayout()
        layoutButton.addStretch(1)
        layoutButton.addWidget(btnDeleteModel)
        layoutButton.addStretch(1)
        mainLayout.addLayout(layoutButton)

        self.window.setLayout(mainLayout)
        self.window.setGeometry(int((screenWidth - mainWith) / 2), int((screenHeight - mainHeight) / 2), mainWith,
                                mainHeight)
        self.window.show()

    def onComboboxSelection(self, selectedText):
        self.selectedModel = selectedText

    def deleteSelectedCheckBox(self, table, combo):
        checkedItems = []

        for i in range(table.rowCount()):
            checkbox = table.cellWidget(i, 2)
            if checkbox.isChecked():
                checkedItems.append(i)

        if checkedItems:
            messageBox = QMessageBox(self)
            messageBox.setFont(QtGui.QFont("Times New Roman", 12))
            messageBox.setWindowTitle("Model Silme Onayı")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setText("Seçili modelleri silmek istediğinize emin misiniz?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('Evet')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('Hayır')
            messageBox.setDefaultButton(buttonN)
            messageBox.exec_()
            if messageBox.clickedButton() == buttonY:
                for i in reversed(checkedItems):
                    modelId: int = table.item(i, 0).text()
                    modelName: str = table.item(i, 1).text()
                    modelPath: str = os.path.join(pathModels, modelName)
                    if modelName.__contains__("face_"):
                        outputsPath: str = os.path.join(pathFaceOutputs, modelName.replace(".h5", ".txt"))
                        mapsPath: str = os.path.join(pathFaceMaps, str("ResultsMap-" + modelName.replace(".h5", ".pkl")))
                    else:
                        outputsPath: str = os.path.join(pathEyeOutputs, modelName.replace(".h5", ".txt"))
                        mapsPath: str = os.path.join(pathEyeMaps, str("ResultsMap-" + modelName.replace(".h5", ".pkl")))
                    # removes
                    removeFromDB(modelId)
                    if os.path.exists(modelPath):
                        os.remove(modelPath)
                    if os.path.exists(outputsPath):
                        os.remove(outputsPath)
                    if os.path.exists(mapsPath):
                        os.remove(mapsPath)
                    combo.removeItem(combo.findText(modelName))
                    table.removeRow(i)
                self.mainWidget.updateModelList()
        else:
            msgBox = QMessageBox(self)
            msgBox.setFont(QtGui.QFont("Times New Roman", 12))
            msgBox.setWindowTitle("Uyarı")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Lütfen önce silinecek modelleri seçin.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            buttonOK = msgBox.button(QMessageBox.Ok)
            buttonOK.setText("Tamam")
            msgBox.exec_()
