import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QLabel, \
    QCheckBox

from src.resources.Environments import pngInfo, pathDatasets, pngChecked, pngUnChecked


class InfoFace(QWidget):
    def __init__(self, mainWidget):
        super(InfoFace, self).__init__()
        self.dataset = None
        self.selectedLastTableFileDataList = None
        self.selectedLastDatasetName = None
        self.selectedLastTableFileList = None
        self.selectedLastRow = None
        self.window = None
        self.mainWidget = mainWidget

    def faceInfoScreen(self):
        mainWidth = 950
        mainHeight = 330
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Veri Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        # Ana düzenleyici
        layout = QHBoxLayout()

        # Dataset listesi
        datasetList = QListWidget()
        datasetList.addItems(os.listdir(pathDatasets))
        datasetList.setMinimumSize(150, 332)
        datasetList.setMaximumSize(150, 332)
        datasetList.setFont(QFont("Times New Roman", 12, QFont.Bold))


        # Dosya listesi
        fileList = QTableWidget()
        fileList.setColumnCount(2)
        fileList.setColumnWidth(0, 200)
        fileList.setHorizontalHeaderLabels(["Veri Listesi", "Veri Sayısı"])
        fileList.setMinimumSize(345, 331)  # tablonun minimum boyutu width, height
        fileList.setMaximumSize(345, 331)  # tablonun maksimum boyutu width, height
        fileList.horizontalHeaderItem(0).setFont(QFont("Times New Roman", 13, QFont.Bold))
        fileList.horizontalHeaderItem(1).setFont(QFont("Times New Roman", 13, QFont.Bold))
        fileList.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        fileList.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        fileList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Dosya veri listesi tablo
        fileDataList = QTableWidget()
        fileDataList.setColumnCount(2)
        # tableFileDataList.setColumnWidth(0, 200)
        fileDataList.setHorizontalHeaderLabels(["Resim", "Dosya İsmi"])
        fileDataList.setMinimumSize(450, 332)  # tablonun minimum boyutu width, height
        fileDataList.setMaximumSize(450, 332)  # tablonun maksimum boyutu width, height
        fileDataList.setColumnWidth(0, 100)
        fileDataList.setColumnWidth(1, 300)
        fileDataList.horizontalHeaderItem(0).setFont(QFont("Times New Roman", 13, QFont.Bold))
        fileDataList.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        fileDataList.horizontalHeaderItem(1).setFont(QFont("Times New Roman", 13, QFont.Bold))
        fileDataList.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        fileDataList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        layout.addWidget(datasetList)
        layout.addWidget(fileList)
        layout.addWidget(fileDataList)

        # Layout ayarları
        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)

        datasetList.itemClicked.connect(lambda item: self.showFileList(item.text(), fileList, fileDataList))

        self.window.show()

    def showFileList(self, datasetName, fileList, fileDataList):
        self.setterDataSetName(datasetName)
        self.setterSelectedLast(fileList, datasetName, None, fileDataList)
        fileList.clearContents()
        fileList.setRowCount(0)
        fileDataList.clearContents()
        fileDataList.setRowCount(0)

        files = os.listdir(f'{pathDatasets}/{datasetName}')
        fileList.setRowCount(len(files))
        if len(files) > 0:
            for i, file in enumerate(files):
                itemButton = QPushButton()
                countItemButton = QPushButton()

                itemButton.setText(file)
                itemButton.setStyleSheet(
                    "background-color: white; color: black; border-radius: 0px; text-align:left; padding-left: 2px;")

                itemButton.setFont(QFont("Times New Roman", 12))


                data = os.listdir(f'{pathDatasets}/{datasetName}/{file}')
                countItemButton.setText(str(len(data)))
                countItemButton.setStyleSheet(
                    "background-color: white; color: black; border-radius: 0px; text-align:left; padding-left: 2px;")
                countItemButton.setFont(QFont("Times New Roman", 12))

                fileList.setCellWidget(i, 0, itemButton)
                fileList.setCellWidget(i, 1, countItemButton)

                itemButton.clicked.connect(
                    lambda checked, row=i: self.selectedButton(datasetName, fileList, row,
                                                               fileDataList))

                countItemButton.clicked.connect(
                    lambda checked, row=i: self.selectedButton(datasetName, fileList, row,
                                                               fileDataList))


    def selectedButton(self, datasetName, tableFileList, row, tableFileDataList):
        for i in range(tableFileList.rowCount()):
            if i == row:
                tableFileList.cellWidget(i, 0).setStyleSheet(
                    "background-color: #DC143C; color: white; border-radius: 0px; text-align:left; padding-left: 2px;")
                tableFileList.cellWidget(i, 1).setStyleSheet(
                    "background-color: #DC143C; color: white; border-radius: 0px; text-align:left; padding-left: 2px;")

            else:
                tableFileList.cellWidget(i, 0).setStyleSheet(
                    "background-color: white; color: black; border-radius: 0px; text-align:left; padding-left: 2px;")

                tableFileList.cellWidget(i, 1).setStyleSheet(
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

                itemDataName = QLabel(str(file))
                itemDataName.setFont(QFont("Times New Roman", 15))
                itemDataName.setAlignment(Qt.AlignCenter)
                tableFileDataList.setCellWidget(i, 0, itemData)
                tableFileDataList.setCellWidget(i, 1, itemDataName)

                tableFileDataList.resizeRowsToContents()

    def setterDataSetName(self, name):
        self.dataset = name

    def setterSelectedLast(self, tableFileList, datasetName, row, tableFileDataList):
        self.selectedLastTableFileList = tableFileList
        self.selectedLastDatasetName = datasetName
        self.selectedLastRow = row
        self.selectedLastTableFileDataList = tableFileDataList
