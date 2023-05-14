from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout

from src.main.python.MPltLib import printGraph
from src.main.python.PostgreSQL import listModels
from src.resources.Environments import pngInfo, pngMainGraphic, pngGraphic


class InfoModel(QWidget):
    def __init__(self, mainWidget):
        super(InfoModel, self).__init__()
        self.window = None
        self.mainWidget = mainWidget

    def modelInfoScreen(self):
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        models = listModels()
        modelMId = [model["m_id"] for model in models]
        modelMRId = [model["mr_id"] for model in models]
        modelNames = [model["model_name"] for model in models]
        modelTrainDataPercentage = [model["data_train_percentage"] for model in models]
        modelValidationDataPercentage = [model["data_validation_percentage"] for model in models]
        modelTrainDuration = [model["total_time"] for model in models]
        modelTrainLoss = [model["train_loss"] for model in models]
        modelTrainAcc = [model["train_acc"] for model in models]
        modelValidationLoss = [model["validation_loss"] for model in models]
        modelValidationAcc = [model["validation_acc"] for model in models]
        modelCreateDateTime = [model["create_date_time"] for model in models]

        modelItems = modelMId, modelMRId, modelNames, modelTrainDataPercentage, modelValidationDataPercentage, modelTrainDuration, modelTrainLoss, modelTrainAcc, modelValidationLoss, modelValidationAcc, modelCreateDateTime
        # todo: model analiz sayısı da eklensin

        mainWidth = 1570
        if len(modelNames) <= 10:
            mainHeight = 230
        else:
            mainHeight = 410

        table = QTableWidget()
        table.setColumnCount(12)
        table.setRowCount(len(modelNames))

        table.setHorizontalHeaderLabels(
            ["m_id", "mr_id", "Model", "Eğitim Veri Yüzdesi", "Doğrulama Veri Yüzdesi", "Eğitim Süresi",
             "Eğitim Kayıp Oranı", "Eğitim Doğruluk Oranı", "Doğrulama Kayıp Oranı", "Doğrulama Doğruluk Oranı",
             "Oluşturulma Tarihi", ""])
        table.setMinimumSize(1555, 180)  # tablonun minimum boyutu width, height
        table.setMaximumSize(1555, 335)  # tablonun maksimum boyutu width, height
        # table.setColumnWidth(0, 20)
        # table.setColumnWidth(1, 360)
        # table.setColumnWidth(2, 20)
        for i in range(len(modelItems)):
            table.horizontalHeaderItem(i).setFont(QFont("Times New Roman", 11, QFont.Bold))
            table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
        table.horizontalHeaderItem(len(modelItems)).setIcon(QIcon(pngMainGraphic))
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        for i in range(len(modelNames)):

            for j in range(len(modelItems)):
                item = QtWidgets.QTableWidgetItem(str(modelItems[j][i]))
                item.setFont(QFont("Times New Roman", 10))
                table.setItem(i, j, item)

            itemButton = QPushButton()
            itemButton.setIcon(QIcon(pngGraphic))  # todo : güzel renk ayarla
            itemButton.setStyleSheet("background-color: #Cbe2e2; color: white; font-weight: bold;")
            itemButton.clicked.connect(lambda checked, row=i: self.printModelName(table, row))
            table.setCellWidget(i, len(modelItems), itemButton)

        # Ana düzenleyici
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)

        # Tabloyu içeren layout
        layoutTable = QHBoxLayout()
        layoutTable.addWidget(table)
        mainLayout.addLayout(layoutTable)

        self.window.setLayout(mainLayout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)
        self.window.show()

    def printModelName(self, table, row):
        modelName = table.item(row, 2).text()
        printGraph(modelName)
