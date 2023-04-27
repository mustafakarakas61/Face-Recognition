import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QTableWidget, QCheckBox, \
    QMessageBox, QLabel

from src.main.python.services.FeaturesService import getComboBoxFeatures, getButtonFeaturesDelete
from src.resources.Environments import pngDelete, pathModels, pngTrash


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

        # ComboBox ayarı
        # Dizin içindeki .h5 uzantılı dosyaları bulma
        modelFiles = [f for f in os.listdir(pathModels) if f.endswith('.h5')]
        # Dosya isimlerinden model adlarını ayırma
        modelNames = [os.path.splitext(f)[0] + ".h5" for f in modelFiles]

        mainWith = 440
        if len(modelFiles) <= 10:
            mainHeight = 260
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
        table.setColumnCount(2)
        table.setRowCount(len(modelNames))  # tablo satır sayısı combobox seçeneklerinin sayısı kadar olacak

        table.setHorizontalHeaderLabels(["Model Listesi", ""])  # tablo başlığı
        table.setMinimumSize(420, 180)  # tablonun minimum boyutu
        table.setMaximumSize(420, 330)  # tablonun maksimum boyutu
        table.horizontalHeaderItem(0).setFont(QFont("Arial", 15, QFont.Bold))
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        table.setColumnWidth(0, 360)
        table.setColumnWidth(1, 40)
        table.horizontalHeaderItem(1).setIcon(QIcon(pngTrash))
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)

        # table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        for i in range(len(modelNames)):
            # Model ismini QTableWidget'e ekleme
            item = QtWidgets.QTableWidgetItem(modelNames[i])
            item.setFont(QFont("Times New Roman", 13))
            table.setItem(i, 0, item)

            # Seçim kutusunu QTableWidget'e ekleme
            checkbox = QCheckBox()
            table.setCellWidget(i, 1, checkbox)

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
            checkbox = table.cellWidget(i, 1)
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
                    modelName = table.item(i, 0).text()
                    filePath = os.path.join(pathModels, modelName)
                    if os.path.exists(filePath):
                        os.remove(filePath)
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
