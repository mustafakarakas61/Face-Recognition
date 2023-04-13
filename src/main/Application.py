import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, \
    QMessageBox

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, \
    getButtonFeatures, getComboBoxFeatures, getTextBoxSuccessRateFeatures, fontTextBox
from src.main.python.services.gui.faceScreens.DeleteFaceScreen import DeleteFace
from src.main.python.services.gui.faceScreens.InfoFaceScreen import InfoFace
from src.main.python.services.gui.faceScreens.addFaceScreens.CameraScreen import Camera
from src.main.python.services.gui.faceScreens.addFaceScreens.ImageScreen import Image
from src.main.python.services.gui.faceScreens.addFaceScreens.LocalFileScreen import LocalFile
from src.main.python.services.gui.faceScreens.addFaceScreens.YoutubeScreen import Youtube
from src.main.python.services.gui.modelScreens.DeleteModel import DeleteModel
from src.main.python.services.gui.modelScreens.InfoModel import InfoModel
from src.main.python.services.gui.modelScreens.TrainModel import TrainModel
from src.main.python.services.gui.testScreens.TestCameraScreen import TestCamera
from src.main.python.services.gui.testScreens.TestLocalFileScreen import TestLocalFile
from src.main.python.services.gui.testScreens.webScreens.TestImageScreen import TestImage
from src.main.python.services.gui.testScreens.webScreens.TestYoutubeScreen import TestYoutube
from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube, pathModels, pathTempFolder, pngInfoBox, pngWarningBox
from utils.Utils import deleteJpgFilesOnFolder, getLine, deleteMp4FilesOnFolder


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # started
        self.control = False
        self.controlOpenGoogle = True
        self.selectedModel = "Model Seçiniz"
        self.textBoxSuccessRate = getTextBoxSuccessRateFeatures(QLineEdit(self), "90", isEnabled=True, isVisible=False)
        self.isMainScreenClosing = False

        # another classes
        # face
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
        mainWith = 500
        mainHeight = 500
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                         mainWith, mainHeight)
        self.setWindowTitle('Yüz Tanıma Projesi created by Mustafa Karakaş')
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon(pngMustafa))

        ###########
        # F A C E #
        ###########
        labelFace = getLabelFeatures(QLabel('Yüz'), isUseFont=True, isUseSecondFont=False)
        # Yüzler için butonlar
        btnFaceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        btnFaceAdd.clicked.connect(self.faceAddScreen)
        btnFaceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnFaceDelete.clicked.connect(self.faceDeleteWidget.faceDeleteScreen)
        btnFaceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnFaceInfo.clicked.connect(self.faceInfoWidget.faceInfoScreen)
        # Yüzler için düzenleyici
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
        # ComboBox ayarı
        # Dizin içindeki .h5 uzantılı dosyaları bulma
        modelFiles = [f for f in os.listdir(pathModels) if f.endswith('.h5')]
        # Dosya isimlerinden model adlarını ayırma
        modelNames = ['Model Seçiniz'] + [os.path.splitext(f)[0] + ".h5" for f in modelFiles]
        # ComboBox oluşturma ve model isimlerini ekleme
        comboModel = getComboBoxFeatures(QComboBox(self))
        comboModel.addItems(modelNames)
        comboModel.currentIndexChanged.connect(lambda index: self.onComboboxSelection(comboModel.itemText(index)))
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
        layoutV.addWidget(comboModel)
        layoutV.addLayout(layoutH)
        layoutV.addLayout(layoutTest)
        self.setLayout(layoutV)
        self.show()

    # Main Screens
    def faceAddScreen(self):
        if not self.getIsMainScreenClosing():
            mainWith = 300
            mainHeight = 300
            screen = QtWidgets.QApplication.desktop().screenGeometry()
            screenWidth, screenHeight = screen.width(), screen.height()

            self.window = QWidget()
            self.window.setWindowTitle('Yüz Ekle')
            self.window.setStyleSheet("background-color: white;")
            self.window.setWindowIcon(QIcon(pngAdd))

            #############
            # Y E R E L #
            #############
            # Yerel etiketi
            labelImage = getLabelFeatures(QLabel('Yerel'), isUseFont=True, isUseSecondFont=False)
            # Yerel için butonlar
            btnVideoCamera = getButtonFeatures(QPushButton(self), pngCamera)
            btnVideoCamera.clicked.connect(self.faceAddCameraWidget.faceAddVideoCameraScreen)
            btnImageFolder = getButtonFeatures(QPushButton(self), pngFolder)
            btnImageFolder.clicked.connect(self.faceAddLocalFileWidget.faceAddLocalFileScreen)
            # Yerel için düzenleyici
            layoutImage = QHBoxLayout()
            layoutImage.addWidget(btnVideoCamera)
            layoutImage.addWidget(btnImageFolder)

            #########
            # W E B #
            #########
            # Web etiketi
            labelVideo = getLabelFeatures(QLabel('Web'), isUseFont=True, isUseSecondFont=False)
            # Web için butonlar
            btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
            btnImageUrl.clicked.connect(self.faceAddImageWidget.faceAddImageUrlScreen)
            btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
            btnVideoYoutube.clicked.connect(self.faceAddYoutubeWidget.faceAddVideoYoutubeScreen)
            # Web için düzenleyici
            layoutVideo = QHBoxLayout()
            layoutVideo.addWidget(btnImageUrl)
            layoutVideo.addWidget(btnVideoYoutube)

            # Ana düzenleyici
            layout = QVBoxLayout()
            layout.addWidget(labelImage)
            layout.addLayout(layoutImage)
            layout.addWidget(getLine())
            layout.addWidget(labelVideo)
            layout.addLayout(layoutVideo)

            self.window.setLayout(layout)
            self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)),
                                    int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWith, mainHeight)
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
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir model seçin.", QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                if int(sRate) < int(rateLimit):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                      "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer girin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
            else:
                mainWith = 300
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
                self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)),
                                        int(screenHeight / 2 - int(mainHeight / 2)),
                                        mainWith, mainHeight)
                self.window.setObjectName("testUrlScreen")
                self.window.show()

    def closeEvent(self, event):
        reply = getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Dikkat!", 'Programdan çıkmak istiyor musun?',
                                  QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                  isQuestion=True).exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            for widget in QtWidgets.QApplication.topLevelWidgets():
                widget.close()
            self.setIsMainScreenClosing(True)
            deleteJpgFilesOnFolder(pathTempFolder)
            deleteMp4FilesOnFolder(pathTempFolder)
            event.accept()
        else:
            event.ignore()

    def showWarn(self):
        getMsgBoxFeatures(QMessageBox(self), pngInfoBox,"Kullanılacak Model ve Başarı Oranı",
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


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
