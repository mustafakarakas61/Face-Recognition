import os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, \
    QMessageBox

from src.main.python.services.DatabaseService import listModels
from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, \
    getButtonFeatures, getComboBoxFeatures, getTextBoxSuccessRateFeatures, fontTextBox
from src.main.python.gui.faceScreens.DeleteDataScreen import DeleteFace
from src.main.python.gui.faceScreens.InfoDataScreen import InfoFace
from src.main.python.gui.faceScreens.addDataScreens.CameraScreen import Camera
from src.main.python.gui.faceScreens.addDataScreens.ImageScreen import Image
from src.main.python.gui.faceScreens.addDataScreens.LocalFileScreen import LocalFile
from src.main.python.gui.faceScreens.addDataScreens.NewDatasetDataScreen import NewDatasetData
from src.main.python.gui.faceScreens.addDataScreens.NewDatasetScreen import NewDataset
from src.main.python.gui.faceScreens.addDataScreens.YoutubeScreen import Youtube
from src.main.python.gui.modelScreens.DeleteModelScreen import DeleteModel
from src.main.python.gui.modelScreens.InfoModelScreen import InfoModel
from src.main.python.gui.modelScreens.TrainModelScreen import TrainModel
from src.main.python.gui.testScreens.TestCameraScreen import TestCamera
from src.main.python.gui.testScreens.TestLocalFileScreen import TestLocalFile
from src.main.python.gui.testScreens.webScreens.TestImageScreen import TestImage
from src.main.python.gui.testScreens.webScreens.TestYoutubeScreen import TestYoutube
from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube, pathTempFolder, pngInfoBox, pngWarningBox, pathDatasets, pathClippedVideos, \
    pathControlFolder
from utils.Utils import getLine, deleteJpgAndMp4FilesOnFolder, deleteFoldersOnFolder


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # started
        self.comboDatasetsData = None
        self.comboDatasets = None
        self.window = None
        self.selectedDatasetDataName = None
        self.selectedDatasetName = None
        self.comboModel = None
        self.control = False
        self.controlOpenGoogle = True
        self.selectedModel = "Model Seçiniz"
        self.textBoxSuccessRate = getTextBoxSuccessRateFeatures(QLineEdit(self), "90", isEnabled=True, isVisible=False)
        self.isMainScreenClosing = False

        # another classes
        # Data
        self.newDatasetWidget = NewDataset(self)
        self.newDatasetDataWidget = NewDatasetData(self)
        self.faceAddLocalFileWidget = LocalFile(self)
        self.faceAddCameraWidget = Camera(self)
        self.faceAddImageWidget = Image(self)
        self.faceAddYoutubeWidget = Youtube(self)
        self.faceDeleteWidget = DeleteFace(self)
        self.faceInfoWidget = InfoFace(self)

        # model
        self.modelTrainWidget = TrainModel(self)
        self.modelDeleteWidget = DeleteModel(self)
        self.modelInfoWidget = InfoModel(self)

        # test
        self.testLocalFileWidget = TestLocalFile(self)
        self.testCameraWidget = TestCamera(self)
        self.testImageWidget = TestImage(self)
        self.testYoutubeWidget = TestYoutube(self)

        # init
        self.initUI()

    def initUI(self):
        mainWidth = 500
        mainHeight = 500
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                         mainWidth, mainHeight)
        self.setWindowTitle('Yüz Tanıma Projesi created by Mustafa Karakaş')
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon(pngMustafa))

        ###########
        # D A T A #
        ###########
        labelFace = getLabelFeatures(QLabel('Veri'), isUseFont=True, isUseSecondFont=False)
        # Veri için butonlar
        btnFaceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        btnFaceAdd.clicked.connect(self.faceAddScreen)
        btnFaceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnFaceDelete.clicked.connect(self.faceDeleteWidget.faceDeleteScreen)
        btnFaceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnFaceInfo.clicked.connect(self.faceInfoWidget.faceInfoScreen)
        # Veri için düzenleyici
        layoutFace = QHBoxLayout()
        layoutFace.addWidget(btnFaceAdd)
        layoutFace.addWidget(btnFaceDelete)
        layoutFace.addWidget(btnFaceInfo)

        ############
        # M O D E L#
        ############
        # Modeller etiketi
        labelModel = getLabelFeatures(QLabel('Model'), isUseFont=True, isUseSecondFont=False)
        # Modeller için butonlar
        btnModelTrain = getButtonFeatures(QPushButton(self), pngTrain)
        btnModelTrain.clicked.connect(self.modelTrainWidget.modelTrainScreen)
        btnModelDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnModelDelete.clicked.connect(self.modelDeleteWidget.modelDeleteScreen)
        btnModelInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnModelInfo.clicked.connect(self.modelInfoWidget.modelInfoScreen)
        # Modeller için düzenleyici
        layoutModel = QHBoxLayout()
        layoutModel.addWidget(btnModelTrain)
        layoutModel.addWidget(btnModelDelete)
        layoutModel.addWidget(btnModelInfo)

        ###########
        # T E S T #
        ###########
        # Test etiketi
        labelTest = getLabelFeatures(QLabel('Test'), isUseFont=True, isUseSecondFont=False)

        # ComboBox oluşturma ve model isimlerini ekleme
        self.comboModel = getComboBoxFeatures(QComboBox(self))
        self.updateModelList()
        self.comboModel.currentIndexChanged.connect(
            lambda index: self.onComboboxSelection(self.comboModel.itemText(index)))
        # Test için butonlar
        btnTestCamera = getButtonFeatures(QPushButton(self), pngCamera)
        btnTestCamera.clicked.connect(self.testCameraWidget.testCameraScreen)
        btnTestLocal = getButtonFeatures(QPushButton(self), pngFolder)
        btnTestLocal.clicked.connect(self.testLocalFileWidget.testLocalFileScreen)
        btnTestUrl = getButtonFeatures(QPushButton(self), pngUrl)
        btnTestUrl.clicked.connect(self.testUrlScreen)
        # Test için düzenleyici
        layoutTest = QHBoxLayout()
        layoutTest.addWidget(btnTestCamera)
        layoutTest.addWidget(btnTestLocal)
        layoutTest.addWidget(btnTestUrl)

        # Ana düzenleyici
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutV.addWidget(labelFace)
        layoutV.addLayout(layoutFace)
        layoutV.addWidget(getLine())
        layoutV.addWidget(labelModel)
        layoutV.addLayout(layoutModel)
        layoutV.addWidget(getLine())
        layoutV.addWidget(labelTest)
        self.textBoxSuccessRate.setVisible(True)
        layoutH.addWidget(self.textBoxSuccessRate)
        labelSuccessRate = QLineEdit()
        labelSuccessRate.setText("% Başarı Oranı")
        labelSuccessRate.setEnabled(False)
        labelSuccessRate.setFont(fontTextBox)
        labelSuccessRate.setStyleSheet("background-color: white; color: black;")

        labelSuccessRate.setAlignment(Qt.AlignLeft)
        layoutH.addWidget(labelSuccessRate)
        layoutV.addWidget(self.comboModel)
        layoutV.addLayout(layoutH)
        layoutV.addLayout(layoutTest)
        self.setLayout(layoutV)
        self.show()

    # Main Screens
    def faceAddScreen(self):
        if not self.getIsMainScreenClosing():
            mainWidth = 330
            mainHeight = 420
            screen = QtWidgets.QApplication.desktop().screenGeometry()
            screenWidth, screenHeight = screen.width(), screen.height()

            self.window = QWidget()
            self.window.setWindowTitle('Yüz Verisi Ekle')
            self.window.setStyleSheet("background-color: white;")
            self.window.setWindowIcon(QIcon(pngAdd))

            # todo : veriseti ve veri seçildiğinde yüz ekleme ekranları açılsın
            # todo : kameradan ve localfile'den ekle sayfası ayarlansın
            # todo : webImage ve youtube 'dan ekle sayfası ayarlansın

            #############
            #  D A T A  #
            #############
            # Combobox
            labelDataset: QLabel = getLabelFeatures(QLabel("<b>Veriseti:</b>"), False, True)
            self.comboDatasets: QComboBox = getComboBoxFeatures(QComboBox(self))
            self.comboDatasets.setFixedSize(150, 30)
            self.updateDatasetList()

            self.comboDatasetsData: QComboBox = getComboBoxFeatures(QComboBox(self))
            self.comboDatasetsData.setFixedSize(150, 30)
            self.comboDatasets.currentIndexChanged.connect(
                lambda index: self.onComboDatasetsSelection(self.comboDatasets.itemText(index), self.comboDatasetsData))

            layoutHDataset = QHBoxLayout()
            layoutHDataset.addWidget(labelDataset, alignment=Qt.AlignLeft)
            layoutHDataset.addWidget(self.comboDatasets, alignment=Qt.AlignRight)

            labelDatasetData: QLabel = getLabelFeatures(QLabel("<b>Veri:</b>"), False, True)
            layoutHDatasetData = QHBoxLayout()
            layoutHDatasetData.addWidget(labelDatasetData, alignment=Qt.AlignLeft)
            layoutHDatasetData.addWidget(self.comboDatasetsData, alignment=Qt.AlignRight)

            layoutHNew = QHBoxLayout()
            # Button
            fontButton = QtGui.QFont("Times New Roman", 15)
            buttonSizes = (150, 50)

            btnNewDataset = QPushButton(self)
            btnNewDataset.setText("Veriseti Oluştur")
            btnNewDataset.setFont(fontButton)
            btnNewDataset.setFixedSize(*buttonSizes)
            btnNewDataset.setStyleSheet("background-color: gray; color: white; border-radius: 5px; font-weight: bold;")
            btnNewDataset.clicked.connect(self.newDatasetWidget.newDatasetScreen)
            layoutHNew.addWidget(btnNewDataset)

            btnNewDatasetData = QPushButton(self)
            btnNewDatasetData.setText("Veri Oluştur")
            btnNewDatasetData.setFont(fontButton)
            btnNewDatasetData.setFixedSize(*buttonSizes)
            btnNewDatasetData.setStyleSheet(
                "background-color: gray; color: white; border-radius: 5px; font-weight: bold;")
            btnNewDatasetData.clicked.connect(
                lambda: self.newDatasetDataWidget.newDatasetDataScreen() if not str(self.selectedDatasetName).__eq__(
                    "Veriseti Seçiniz") and self.selectedDatasetName is not None else getMsgBoxFeatures(
                    QMessageBox(), pngWarningBox, "Uyarı", "Lütfen bir <b>veriseti</b> seçin.",
                    QMessageBox.Warning,
                    QMessageBox.Ok, isQuestion=False).exec_())
            layoutHNew.addWidget(btnNewDatasetData)

            #############
            # Y E R E L #
            #############
            # Yerel etiketi
            labelLocal = getLabelFeatures(QLabel('Yerel'), isUseFont=True, isUseSecondFont=False)
            # Yerel için butonlar
            btnVideoCamera = getButtonFeatures(QPushButton(self), pngCamera)
            btnVideoCamera.clicked.connect(self.faceAddCameraWidget.faceAddVideoCameraScreen)
            btnLocalFile = getButtonFeatures(QPushButton(self), pngFolder)
            btnLocalFile.clicked.connect(self.faceAddLocalFileWidget.faceAddLocalFileScreen)
            # Yerel için düzenleyici
            layoutLocal = QHBoxLayout()
            layoutLocal.addWidget(btnVideoCamera)
            layoutLocal.addWidget(btnLocalFile)

            #########
            # W E B #
            #########
            # Web etiketi
            labelWeb = getLabelFeatures(QLabel('Web'), isUseFont=True, isUseSecondFont=False)
            # Web için butonlar
            btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
            btnImageUrl.clicked.connect(self.faceAddImageWidget.faceAddImageUrlScreen)
            btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
            btnVideoYoutube.clicked.connect(self.faceAddYoutubeWidget.faceAddVideoYoutubeScreen)
            # Web için düzenleyici
            layoutWeb = QHBoxLayout()
            layoutWeb.addWidget(btnImageUrl)
            layoutWeb.addWidget(btnVideoYoutube)

            # Ana düzenleyici
            layout = QVBoxLayout()

            layoutV = QVBoxLayout()
            layoutV.addLayout(layoutHDataset)
            layoutV.addLayout(layoutHDatasetData)

            layoutV.addLayout(layoutHNew)

            layout.addLayout(layoutV)
            layout.addWidget(getLine())
            layout.addWidget(labelLocal)
            layout.addLayout(layoutLocal)
            layout.addWidget(getLine())
            layout.addWidget(labelWeb)
            layout.addLayout(layoutWeb)

            self.window.setLayout(layout)
            self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                    int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWidth, mainHeight)
            # Çarpı işaretine basıldığında
            self.window.setAttribute(Qt.WA_DeleteOnClose)
            # self.window.destroyed.connect(self.onClosedFaceAddScreen)
            self.window.closeEvent = self.onClosedFaceAddScreen
            self.window.show()

    def testUrlScreen(self):
        if not self.getIsMainScreenClosing():
            modelName = self.selectedModel
            sRate = self.textBoxSuccessRate.text()
            if str(sRate).__len__() == 0:
                sRate = "0"
            # Model seçilmemişse uyarı verme
            rateLimit = 35
            if modelName.__eq__("Model Seçiniz") or int(sRate) < int(rateLimit):
                if modelName.__eq__("Model Seçiniz"):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir model seçin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                if int(sRate) < int(rateLimit):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                      "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer girin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
            else:
                mainWidth = 300
                mainHeight = 150
                screen = QtWidgets.QApplication.desktop().screenGeometry()
                screenWidth, screenHeight = screen.width(), screen.height()

                self.window = QWidget()
                self.window.setWindowTitle('Test Web')
                self.window.setStyleSheet("background-color: white;")
                self.window.setWindowIcon(QIcon(pngUrl))

                #############
                # R E S İ M #
                #############
                btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
                btnImageUrl.clicked.connect(self.testImageWidget.testUrlImageScreen)
                layoutImage = QHBoxLayout()
                layoutImage.addWidget(btnImageUrl)

                #################
                # Y O U T U B E #
                #################
                btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
                btnVideoYoutube.clicked.connect(self.testYoutubeWidget.testUrlYoutubeScreen)
                layoutYoutube = QHBoxLayout()
                layoutYoutube.addWidget(btnVideoYoutube)

                # Ana düzenleyici
                layout = QHBoxLayout()
                layout.addLayout(layoutImage)
                layout.addLayout(layoutYoutube)

                self.window.setLayout(layout)
                self.window.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                        int(screenHeight / 2 - int(mainHeight / 2)),
                                        mainWidth, mainHeight)
                self.window.setObjectName("testUrlScreen")
                self.window.show()

    def closeEvent(self, event):
        reply = getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Dikkat!", 'Programdan çıkmak istiyor musun?',
                                  QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                  isQuestion=True).exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            self.setIsMainScreenClosing(True)
            for widget in QtWidgets.QApplication.topLevelWidgets():
                widget.close()
            deleteJpgAndMp4FilesOnFolder(pathClippedVideos)
            deleteJpgAndMp4FilesOnFolder(pathControlFolder)
            deleteJpgAndMp4FilesOnFolder(pathTempFolder)
            deleteFoldersOnFolder(pathTempFolder)

            event.accept()
        else:
            event.ignore()

    def onClosedFaceAddScreen(self, event):
        if not self.getIsMainScreenClosing():
            if self.selectedDatasetName is not None or self.selectedDatasetDataName is not None:
                reply = getMsgBoxFeatures(QMessageBox(), pngWarningBox, "Dikkat!",
                                          'Veri Ekle ekranından çıkış yapılsın mı?',
                                          QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                          isQuestion=True).exec_()
                if reply == QtWidgets.QMessageBox.Yes:
                    self.selectedDatasetName = None
                    self.selectedDatasetDataName = None
                    if self.newDatasetWidget and self.newDatasetWidget.window and self.newDatasetWidget.window.isVisible():
                        self.newDatasetWidget.window.close()
                    if self.newDatasetDataWidget and self.newDatasetDataWidget.window and self.newDatasetDataWidget.window.isVisible():
                        self.newDatasetDataWidget.window.close()
                    event.accept()
                else:
                    event.ignore()
            self.closeSubScreens()

    def closeSubScreens(self):
        if self.faceAddCameraWidget is not None:
            self.faceAddCameraWidget.closeScreen()

        if self.faceAddLocalFileWidget is not None:
            self.faceAddLocalFileWidget.closeScreen()

        if self.faceAddImageWidget is not None:
            self.faceAddImageWidget.closeScreen()

        if self.faceAddYoutubeWidget is not None:
            self.faceAddYoutubeWidget.closeScreen()

    def updateDatasetList(self):
        if self.comboDatasets is not None:
            datasetFolders = [f for f in os.listdir(pathDatasets) if os.path.isdir(os.path.join(pathDatasets, f))]
            datasetNames = ['Veriseti Seçiniz'] + datasetFolders
            self.comboDatasets.clear()
            self.comboDatasets.addItems(datasetNames)

    def updateModelList(self):
        if self.comboModel is not None:
            models = listModels()
            modelNames = ["Model Seçiniz"] + [model["model_name"] for model in models]
            # ComboBox öğesi güncelleme
            self.comboModel.clear()
            self.comboModel.addItems(modelNames)

    def showWarn(self):
        getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Kullanılacak Model ve Başarı Oranı",
                          self.selectedModel + "\nBaşarı oranı " + str(
                              self.textBoxSuccessRate.text()) + " olarak belirlenmiştir.",
                          QMessageBox.Information, QMessageBox.Ok, isQuestion=False).exec_()

    def getIsMainScreenClosing(self):
        return self.isMainScreenClosing

    def setIsMainScreenClosing(self, value):
        self.isMainScreenClosing = value

    # Seçili olan modelin adını alma
    def onComboboxSelection(self, newName):
        self.selectedModel = newName

    def onComboDatasetsSelection(self, newName, comboDatasetsData: QComboBox):
        self.selectedDatasetName = newName
        if self.selectedDatasetName is not None and len(
                self.selectedDatasetName) > 0 and not self.selectedDatasetName.__eq__("Veriseti Seçiniz"):
            datasetDataFolders = [f for f in os.listdir(pathDatasets + self.selectedDatasetName) if
                                  os.path.isdir(os.path.join(pathDatasets + self.selectedDatasetName, f))]
            datasetDataNames = ['Veri Seçiniz'] + datasetDataFolders
            comboDatasetsData.clear()
            comboDatasetsData.addItems(datasetDataNames)
            comboDatasetsData.currentIndexChanged.connect(
                lambda index: self.onComboDatasetsDataSelection(comboDatasetsData.itemText(index)))
        else:
            comboDatasetsData.clear()

    def onComboDatasetsDataSelection(self, newName):
        self.selectedDatasetDataName = newName


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
