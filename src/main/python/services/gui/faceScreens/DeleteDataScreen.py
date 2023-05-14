import os
import shutil

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QTableWidget, QHBoxLayout, QListWidget, QPushButton, QVBoxLayout, \
    QLabel, QCheckBox, QMessageBox

from src.main.python.services.FeaturesService import getButtonFeaturesDelete, getButtonFeaturesSelectAll, \
    getButtonFeaturesClear
from src.resources.Environments import pngDelete, pathDatasets, pngTrash, pngUnChecked, pngChecked, pngWarningBox


class DeleteFace(QWidget):
    def __init__(self, mainWidget):
        super(DeleteFace, self).__init__()
        self.dataset = None
        self.selectedLastTableFileDataList = None
        self.selectedLastDatasetName = None
        self.selectedLastTableFileList = None
        self.selectedLastRow = None
        self.window = None
        self.mainWidget = mainWidget

    def faceDeleteScreen(self):
        mainWidth = 910
        mainHeight = 330
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Veri Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Dataset listesi
        datasetList = QListWidget()
        datasetList.addItems(os.listdir(pathDatasets))
        datasetList.setMinimumSize(150, 332)
        datasetList.setMaximumSize(150, 332)
        datasetList.setFont(QFont("Times New Roman", 13, QFont.Bold))

        # Dosya listesi tablo
        tableFileList = QTableWidget()
        tableFileList.setColumnCount(1)
        tableFileList.setColumnWidth(0, 200)
        tableFileList.setHorizontalHeaderLabels(["Veri Listesi"])
        tableFileList.setMinimumSize(250, 330)  # tablonun minimum boyutu width, height
        tableFileList.setMaximumSize(250, 330)  # tablonun maksimum boyutu width, height
        tableFileList.horizontalHeaderItem(0).setFont(QFont("Times New Roman", 13, QFont.Bold))
        tableFileList.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        tableFileList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Dosya veri listesi tablo
        tableFileDataList = QTableWidget()
        tableFileDataList.setColumnCount(3)
        # tableFileDataList.setColumnWidth(0, 200)
        tableFileDataList.setHorizontalHeaderLabels(["Resim", "Dosya İsmi", ""])
        tableFileDataList.setMinimumSize(480, 332)  # tablonun minimum boyutu width, height
        tableFileDataList.setMaximumSize(480, 332)  # tablonun maksimum boyutu width, height
        tableFileDataList.setColumnWidth(0, 100)
        tableFileDataList.setColumnWidth(1, 300)
        tableFileDataList.setColumnWidth(2, 30)
        tableFileDataList.horizontalHeaderItem(0).setFont(QFont("Times New Roman", 13, QFont.Bold))
        tableFileDataList.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        tableFileDataList.horizontalHeaderItem(1).setFont(QFont("Times New Roman", 13, QFont.Bold))
        tableFileDataList.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        tableFileDataList.horizontalHeaderItem(2).setIcon(QIcon(pngTrash))
        tableFileDataList.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        tableFileDataList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        datasetList.itemClicked.connect(
            lambda item: self.showFileList(item.text(), tableFileList, tableFileDataList))

        btnDeleteDataSet = getButtonFeaturesDelete(QPushButton(), text="Verisetini Sil", butonSizes=(130, 50))
        btnDeleteDataSet.clicked.connect(lambda: self.deleteSelectedDataset(datasetList, tableFileList, tableFileDataList))

        btnDeleteDataSetFile = getButtonFeaturesDelete(QPushButton(), text="Veriyi Sil", butonSizes=(110, 50))
        btnDeleteDataSetFile.clicked.connect(
            lambda: self.deleteSelectedDatasetFile(self.selectedLastTableFileList, self.selectedLastDatasetName,
                                                   self.selectedLastRow, self.selectedLastTableFileDataList))

        btnSelectAll = getButtonFeaturesSelectAll(QPushButton(), text="Tümünü Seç")
        btnSelectAll.clicked.connect(lambda: self.selectAllCheckboxes(tableFileDataList))

        btnClearSelected = getButtonFeaturesClear(QPushButton(), text="Temizle")
        btnClearSelected.clicked.connect(lambda: self.clearSelectedCheckboxes(tableFileDataList))

        btnDeleteModel = getButtonFeaturesDelete(QPushButton(), text="Sil", butonSizes=(70, 50))
        btnDeleteModel.clicked.connect(lambda: self.deleteSelectedCheckBox(tableFileDataList))

        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(datasetList)
        layoutV1.addWidget(btnDeleteDataSet)
        layoutV1.setAlignment(datasetList, Qt.AlignCenter)
        layoutV1.setAlignment(btnDeleteDataSet, Qt.AlignCenter)

        layoutV2 = QVBoxLayout()
        layoutV2.addWidget(tableFileList)
        layoutV2.addWidget(btnDeleteDataSetFile)
        layoutV2.setAlignment(tableFileList, Qt.AlignCenter)
        layoutV2.setAlignment(btnDeleteDataSetFile, Qt.AlignCenter)

        layoutV3 = QVBoxLayout()
        layoutV3.addWidget(tableFileDataList)
        layoutH = QHBoxLayout()
        layoutH.addStretch(1)
        layoutH.addWidget(btnSelectAll)
        layoutH.addWidget(btnClearSelected)
        layoutH.addWidget(btnDeleteModel)
        layoutH.addStretch(1)
        layoutV3.setAlignment(btnDeleteModel, Qt.AlignCenter)
        layoutV3.addLayout(layoutH)

        # Ana düzenleyici
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layoutV1)
        mainLayout.addLayout(layoutV2)
        mainLayout.addLayout(layoutV3)

        mainLayout.setAlignment(layoutV1, Qt.AlignCenter)
        mainLayout.setAlignment(layoutV2, Qt.AlignCenter)
        mainLayout.setAlignment(layoutV3, Qt.AlignCenter)

        # Layout ayarları
        self.window.setLayout(mainLayout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)

        self.window.destroyed.connect(self.onWindowClosed)
        self.window.show()

    def showFileList(self, datasetName, tableFileList, tableFileDataList):
        self.setterDataSetName(datasetName)
        self.setterSelectedLast(tableFileList, datasetName, None, tableFileDataList)
        tableFileDataList.clearContents()
        tableFileDataList.setRowCount(0)
        tableFileList.clearContents()
        tableFileList.setRowCount(0)

        files = os.listdir(f'{pathDatasets}/{datasetName}')
        tableFileList.setRowCount(len(files))
        if len(files) > 0:
            for i, file in enumerate(files):
                itemButton = QPushButton()
                itemButton.setText(file)
                itemButton.setStyleSheet(
                    "background-color: white; color: black; border-radius: 0px; text-align:left; padding-left: 2px;")
                itemButton.clicked.connect(
                    lambda checked, row=i: self.selectedButton(datasetName, tableFileList, row,
                                                               tableFileDataList))
                itemButton.setFont(QFont("Times New Roman", 12))
                tableFileList.setCellWidget(i, 0, itemButton)

    def selectedButton(self, datasetName, tableFileList, row, tableFileDataList):
        for i in range(tableFileList.rowCount()):
            if i == row:
                tableFileList.cellWidget(i, 0).setStyleSheet(
                    "background-color: #DC143C; color: white; border-radius: 0px; text-align:left; padding-left: 2px;")
            # Diğer düğmelerin arkaplan rengini değiştir
            else:
                tableFileList.cellWidget(i, 0).setStyleSheet(
                    "background-color: white; color: black; border-radius: 0px; text-align:left; padding-left: 2px;")

        self.setterSelectedLast(tableFileList, datasetName, row, tableFileDataList)

        tableFileDataList.clearContents()
        tableFileDataList.setRowCount(0)

        files = os.listdir(f'{pathDatasets}/{datasetName}/{tableFileList.cellWidget(row, 0).text()}')
        tableFileDataList.setRowCount(len(files))
        if len(files) > 0:
            for i, file in enumerate(files):
                itemData = QPushButton()
                pathData = f'{pathDatasets}{datasetName}/{tableFileList.cellWidget(row, 0).text()}/{file}'

                itemData.setStyleSheet(
                    "border-radius: 0px; text-align:center; padding-left: 2px;")
                itemData.setFixedSize(100, 100)
                itemData.setIconSize(QtCore.QSize(100, 100))
                itemData.setIcon(QIcon(pathData))
                # itemData.clicked.connect(
                #     lambda checked, row=i: self.selectedButton(datasetName, tableFileList, row, tableFileDataList,
                #                                                itemData.text()))
                # itemData.setFont(QFont("Times New Roman", 12))
                itemDataName = QLabel(str(file))
                itemDataName.setFont(QFont("Times New Roman", 15))
                itemDataName.setAlignment(Qt.AlignCenter)
                tableFileDataList.setCellWidget(i, 0, itemData)
                tableFileDataList.setCellWidget(i, 1, itemDataName)

                itemCheckbox = QCheckBox()
                itemCheckbox.setStyleSheet(
                    "QCheckBox::indicator { width: 30px; height: 30px; background-color: white;padding-left: 4px;}"
                    "QCheckBox::indicator:checked { image: url(" + str(pngChecked) + "); }"
                                                                                     "QCheckBox::indicator:unchecked { image: url(" + str(
                        pngUnChecked) + "); }"
                )
                tableFileDataList.setCellWidget(i, 2, itemCheckbox)

                tableFileDataList.resizeRowsToContents()

    def onWindowClosed(self):
        self.dataset = None

    def deleteSelectedDataset(self, datasetList: QListWidget, tableFileList: QTableWidget,
                              tableFileDataList: QTableWidget):
        if self.dataset is not None:
            messageBox = QMessageBox(self)
            messageBox.setWindowIcon(QIcon(pngWarningBox))
            messageBox.setFont(QtGui.QFont("Times New Roman", 12))
            messageBox.setWindowTitle("Veriseti Silme Onayı")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setText("Verisetinin tamamen silinmesini istiyor musunuz?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('Evet')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('Hayır')
            messageBox.setDefaultButton(buttonN)
            messageBox.exec_()

            if messageBox.clickedButton() == buttonY:
                messageBox2 = QMessageBox(self)
                messageBox2.setWindowIcon(QIcon(pngWarningBox))
                messageBox2.setFont(QtGui.QFont("Times New Roman", 12))
                messageBox2.setWindowTitle("Dikkat")
                messageBox2.setIcon(QMessageBox.Question)
                messageBox2.setText("Emin misiniz?")
                messageBox2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                buttonY2 = messageBox2.button(QMessageBox.Yes)
                buttonY2.setText('Evet')
                buttonN2 = messageBox2.button(QMessageBox.No)
                buttonN2.setText('Hayır')
                messageBox2.setDefaultButton(buttonN2)
                messageBox2.exec_()
                if messageBox2.clickedButton() == buttonY2:
                    pathDataset = f'{pathDatasets}/{self.dataset}'
                    if os.path.exists(pathDataset):
                        shutil.rmtree(pathDataset)

                    datasetNameForInfo: str = self.dataset
                    self.updateDatasetList(datasetList)
                    tableFileList.clearContents()
                    tableFileList.setRowCount(0)
                    tableFileDataList.clearContents()
                    tableFileDataList.setRowCount(0)

                    msgBoxDeleteInfo = QMessageBox(self)
                    msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                    msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                    msgBoxDeleteInfo.setWindowTitle("Uyarı")
                    msgBoxDeleteInfo.setIcon(QMessageBox.Warning)
                    msgBoxDeleteInfo.setText(
                        "<b>" + datasetNameForInfo + "</b> veriseti tamamen silindi.")
                    msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                    buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                    buttonOK.setText("Tamam")
                    msgBoxDeleteInfo.exec_()
                else:
                    msgBoxDeleteInfo = QMessageBox(self)
                    msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                    msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                    msgBoxDeleteInfo.setWindowTitle("Bilgi")
                    msgBoxDeleteInfo.setIcon(QMessageBox.Information)
                    msgBoxDeleteInfo.setText(
                        "Herhangi bir veri silinmedi.")
                    msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                    buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                    buttonOK.setText("Tamam")
                    msgBoxDeleteInfo.exec_()
            else:
                msgBoxDeleteInfo = QMessageBox(self)
                msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                msgBoxDeleteInfo.setWindowTitle("Uyarı")
                msgBoxDeleteInfo.setIcon(QMessageBox.Warning)
                msgBoxDeleteInfo.setText(
                    "İşlem iptal edildi!")
                msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                buttonOK.setText("Tamam")
                msgBoxDeleteInfo.exec_()

        else:
            msgBox = QMessageBox(self)
            msgBox.setWindowIcon(QIcon(pngWarningBox))
            msgBox.setFont(QtGui.QFont("Times New Roman", 12))
            msgBox.setWindowTitle("Uyarı")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Lütfen bir veriseti seçin.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            buttonOK = msgBox.button(QMessageBox.Ok)
            buttonOK.setText("Tamam")
            msgBox.exec_()

    def updateDatasetList(self, datasetList: QListWidget):
        self.dataset = None
        datasetList.clear()
        datasetList.addItems(os.listdir(pathDatasets))

    def deleteSelectedDatasetFile(self, tableFileList, datasetName, row, tableFileDataList):

        if row is not None and datasetName is not None:
            messageBox = QMessageBox(self)
            messageBox.setWindowIcon(QIcon(pngWarningBox))
            messageBox.setFont(QtGui.QFont("Times New Roman", 12))
            messageBox.setWindowTitle("Veri Silme Onayı")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setText("İçindekilerle beraber verinin silinmesini istiyor musunuz?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('Evet')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('Hayır')
            messageBox.setDefaultButton(buttonN)
            messageBox.exec_()

            if messageBox.clickedButton() == buttonY:
                messageBox2 = QMessageBox(self)
                messageBox2.setWindowIcon(QIcon(pngWarningBox))
                messageBox2.setFont(QtGui.QFont("Times New Roman", 12))
                messageBox2.setWindowTitle("Dikkat")
                messageBox2.setIcon(QMessageBox.Question)
                messageBox2.setText("Emin misiniz?")
                messageBox2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                buttonY2 = messageBox2.button(QMessageBox.Yes)
                buttonY2.setText('Evet')
                buttonN2 = messageBox2.button(QMessageBox.No)
                buttonN2.setText('Hayır')
                messageBox2.setDefaultButton(buttonN2)
                messageBox2.exec_()
                dataName: str = tableFileList.cellWidget(row, 0).text()
                if messageBox2.clickedButton() == buttonY2:
                    pathData = f'{pathDatasets}/{datasetName}/{dataName}'
                    if os.path.exists(pathData):
                        shutil.rmtree(pathData)
                    self.showFileList(datasetName, tableFileList, tableFileDataList)
                    tableFileDataList.clearContents()
                    tableFileDataList.setRowCount(0)

                    msgBoxDeleteInfo = QMessageBox(self)
                    msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                    msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                    msgBoxDeleteInfo.setWindowTitle("Uyarı")
                    msgBoxDeleteInfo.setIcon(QMessageBox.Warning)
                    msgBoxDeleteInfo.setText(
                        "<b>" + datasetName + "</b> veriseti içerisindeki <b>" + dataName + "</b> verisi tamamen silindi.")
                    msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                    buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                    buttonOK.setText("Tamam")
                    msgBoxDeleteInfo.exec_()
                else:
                    msgBoxDeleteInfo = QMessageBox(self)
                    msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                    msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                    msgBoxDeleteInfo.setWindowTitle("Bilgi")
                    msgBoxDeleteInfo.setIcon(QMessageBox.Information)
                    msgBoxDeleteInfo.setText(
                        "Herhangi bir veri silinmedi.")
                    msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                    buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                    buttonOK.setText("Tamam")
                    msgBoxDeleteInfo.exec_()
            else:
                msgBoxDeleteInfo = QMessageBox(self)
                msgBoxDeleteInfo.setWindowIcon(QIcon(pngWarningBox))
                msgBoxDeleteInfo.setFont(QtGui.QFont("Times New Roman", 12))
                msgBoxDeleteInfo.setWindowTitle("Uyarı")
                msgBoxDeleteInfo.setIcon(QMessageBox.Warning)
                msgBoxDeleteInfo.setText(
                    "İşlem iptal edildi!")
                msgBoxDeleteInfo.setStandardButtons(QMessageBox.Ok)
                buttonOK = msgBoxDeleteInfo.button(QMessageBox.Ok)
                buttonOK.setText("Tamam")
                msgBoxDeleteInfo.exec_()
        else:
            msgBox = QMessageBox(self)
            msgBox.setWindowIcon(QIcon(pngWarningBox))
            msgBox.setFont(QtGui.QFont("Times New Roman", 12))
            msgBox.setWindowTitle("Uyarı")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Lütfen bir veri seçin.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            buttonOK = msgBox.button(QMessageBox.Ok)
            buttonOK.setText("Tamam")
            msgBox.exec_()

    def selectAllCheckboxes(self, table):
        for i in range(table.rowCount()):
            checkbox = table.cellWidget(i, 2)
            checkbox.setChecked(True)

    def clearSelectedCheckboxes(self, table):
        for i in range(table.rowCount()):
            checkbox = table.cellWidget(i, 2)
            if checkbox.isChecked():
                checkbox.setChecked(False)

    def deleteSelectedCheckBox(self, table):
        checkedItems = []

        for i in range(table.rowCount()):
            checkbox = table.cellWidget(i, 2)
            if checkbox.isChecked():
                checkedItems.append(i)

        if checkedItems:
            messageBox = QMessageBox(self)
            messageBox.setWindowIcon(QIcon(pngWarningBox))
            messageBox.setFont(QtGui.QFont("Times New Roman", 12))
            messageBox.setWindowTitle("Veri Silme Onayı")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setText("Seçili verileri silmek istediğinize emin misiniz?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('Evet')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('Hayır')
            messageBox.setDefaultButton(buttonN)
            messageBox.exec_()
            if messageBox.clickedButton() == buttonY:
                for i in reversed(checkedItems):
                    dataFileName: str = table.cellWidget(i, 1).text()
                    dataName: str = dataFileName.split("_")[0]
                    dataPath: str = f'{pathDatasets}{self.dataset}/{dataName}/{dataFileName}'
                    if os.path.exists(dataPath):
                        os.remove(dataPath)
                    table.removeRow(i)
                # updates
                self.mainWidget.updateModelList()
        else:
            msgBox = QMessageBox(self)
            msgBox.setWindowIcon(QIcon(pngWarningBox))
            msgBox.setFont(QtGui.QFont("Times New Roman", 12))
            msgBox.setWindowTitle("Uyarı")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Lütfen önce silinecek verileri seçin.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            buttonOK = msgBox.button(QMessageBox.Ok)
            buttonOK.setText("Tamam")
            msgBox.exec_()

    def setterDataSetName(self, name):
        self.dataset = name

    def setterSelectedLast(self, tableFileList, datasetName, row, tableFileDataList):
        self.selectedLastTableFileList = tableFileList
        self.selectedLastDatasetName = datasetName
        self.selectedLastRow = row
        self.selectedLastTableFileDataList = tableFileDataList
