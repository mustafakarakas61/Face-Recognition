import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QTableWidget, QTableWidgetItem, QHBoxLayout

from src.resources.Environments import pngInfo, pathDatasets


class InfoFace(QWidget):
    def __init__(self, mainWidget):
        super(InfoFace, self).__init__()
        self.window = None
        self.mainWidget = mainWidget

    def faceInfoScreen(self):
        mainWith = 530
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
        datasetList.setMinimumSize(150, 330)
        datasetList.setMaximumSize(150, 330)
        datasetList.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(datasetList)

        # Dosya listesi
        fileList = QTableWidget()
        fileList.setColumnCount(2)
        fileList.setColumnWidth(0, 200)
        fileList.setHorizontalHeaderLabels(["Veri Listesi", "Veri Sayısı"])
        fileList.setMinimumSize(350, 330)  # tablonun minimum boyutu width, height
        fileList.setMaximumSize(350, 330)  # tablonun maksimum boyutu width, height
        fileList.horizontalHeaderItem(0).setFont(QFont("Times New Roman", 12, QFont.Bold))
        fileList.horizontalHeaderItem(1).setFont(QFont("Times New Roman", 12, QFont.Bold))
        fileList.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        fileList.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        fileList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        layout.addWidget(fileList)

        # Layout ayarları
        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)

        datasetList.itemClicked.connect(lambda item: self.showFileList(item.text(), fileList))

        self.window.show()

    def showFileList(self, datasetName, fileList):
        fileList.clearContents()
        fileList.setRowCount(0)

        files = os.listdir(f'{pathDatasets}/{datasetName}')
        fileList.setRowCount(len(files))

        for i, file in enumerate(files):
            fileNameItem = QTableWidgetItem(file)
            fileNameItem.setFont(QFont("Times New Roman", 12))
            data = os.listdir(f'{pathDatasets}/{datasetName}/{file}')
            dataCount = len(data)
            dataCountItem = QTableWidgetItem(str(dataCount))
            dataCountItem.setFont(QFont("Times New Roman", 12))
            fileList.setItem(i, 0, fileNameItem)
            fileList.setItem(i, 1, dataCountItem)
