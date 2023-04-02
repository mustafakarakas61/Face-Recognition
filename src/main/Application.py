import os
import pickle
import re
import requests
import webbrowser
import random

import cv2
import numpy as np
import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, \
    QMessageBox, QFrame, QFileDialog

from src.main.python.services.FeaturesService import getTextBoxFeatures, getMsgBoxFeatures, getLabelFeatures, \
    getButtonFeatures, getComboBoxFeatures, getTextBoxSuccessRateFeatures, getFaceButtonFeatures
from src.main.python.services.gui.test.Camera import testCamera
from src.main.python.services.gui.test.Local import testImage, testVideo
from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube, pathModels, pathFaceResultsMap, pathFaceCascade, pathTempFolder, \
    pngFaceDetection0, pngFaceDetection1, pngFace404, pngFaceDetection2
from utils.Utils import randomString, deleteJpgFilesOnFolder


def getLine():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet("background-color: black;")
    return line


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.selectedModel = "Model Seçiniz"
        self.textBoxSuccessRate = getTextBoxSuccessRateFeatures(QLineEdit(self), "90", isEnabled=True, isVisible=False)
        self.isMainScreenClosing = False
        self.initUI()

    def closeEvent(self, event):
        reply = getMsgBoxFeatures(QMessageBox(self), "Dikkat!", 'Programdan çıkmak istiyor musun?',
                                  QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                  isQuestion=True).exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            for widget in QtWidgets.QApplication.topLevelWidgets():
                widget.close()
            self.setIsMainScreenClosing(True)
            deleteJpgFilesOnFolder(pathTempFolder)
            event.accept()
        else:
            event.ignore()

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

        #########
        # Y Ü Z #
        #########
        labelFace = getLabelFeatures(QLabel('Yüz'), isUseFont=True, isUseSecondFont=False)
        # Yüzler için butonlar
        btnFaceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        btnFaceAdd.clicked.connect(self.faceAddScreen)
        btnFaceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnFaceDelete.clicked.connect(self.faceDeleteScreen)
        btnFaceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnFaceInfo.clicked.connect(self.faceInfoScreen)

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
        btnModelTrain.clicked.connect(self.modelTrainScreen)
        btnModelDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnModelDelete.clicked.connect(self.modelDeleteScreen)
        btnModelInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnModelInfo.clicked.connect(self.modelInfoScreen)
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

        # Seçili olan modelin adını alma
        def onComboboxSelection(modelName):
            self.selectedModel = modelName

        comboModel.currentIndexChanged.connect(lambda index: onComboboxSelection(comboModel.itemText(index)))

        # Test için butonlar
        btnTestCamera = getButtonFeatures(QPushButton(self), pngCamera)
        btnTestCamera.clicked.connect(self.testCameraScreen)
        btnTestLocal = getButtonFeatures(QPushButton(self), pngFolder)
        btnTestLocal.clicked.connect(self.testLocalScreen)
        btnTestUrl = getButtonFeatures(QPushButton(self), pngUrl)
        btnTestUrl.clicked.connect(self.testUrlScreen)
        # Test için düzenleyici
        layoutTest = QHBoxLayout()

        # Düzenleyiciye ekleme
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

        labelSuccessRate = getTextBoxSuccessRateFeatures(QLineEdit(self), "% Başarı Oranı", isEnabled=False,
                                                         isVisible=True)
        labelSuccessRate.setAlignment(Qt.AlignLeft)
        layoutH.addWidget(labelSuccessRate)

        layoutV.addWidget(comboModel)
        layoutV.addLayout(layoutH)
        layoutV.addLayout(layoutTest)
        self.setLayout(layoutV)
        self.show()

    # SCREENS
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
            btnVideoCamera.clicked.connect(self.faceAddVideoCameraScreen)
            btnImageFolder = getButtonFeatures(QPushButton(self), pngFolder)
            btnImageFolder.clicked.connect(self.faceAddImageFolderScreen)
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
            btnImageUrl.clicked.connect(self.faceAddImageUrlScreen)
            btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
            btnVideoYoutube.clicked.connect(self.faceAddVideoYoutubeScreen)
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

    def faceAddImageFolderScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yerelden Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngFolder))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(
            QtCore.Qt.WA_DeleteOnClose)  # todo eğer anaekranınkine basıldıysa açılmasın burası ve bu gibiler
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddImageUrlScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('URL\'den Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngImageUrl))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddVideoCameraScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Kameradan Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngCamera))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddVideoYoutubeScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Youtube\'dan Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngYoutube))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceDeleteScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceInfoScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelTrainScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Eğitimi')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngTrain))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelDeleteScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelInfoScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testCameraScreen(self):
        modelName = self.selectedModel
        sRate = self.textBoxSuccessRate.text()
        if str(sRate).__len__() == 0:
            sRate = "0"
        # Model seçilmemişse uyarı verme
        rateLimit = 35
        if modelName.__eq__("Model Seçiniz") or int(sRate) < int(rateLimit):
            if modelName.__eq__("Model Seçiniz"):
                getMsgBoxFeatures(QMessageBox(self), "Uyarı", "Lütfen bir model seçin", QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            if int(sRate) < int(rateLimit):
                getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                  "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer giriniz.",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
        else:
            # Mesaj kutusunu gösterme
            # self.showWarn()

            testCamera(str(modelName), int(sRate))

    def testLocalScreen(self):
        modelName = self.selectedModel
        sRate = self.textBoxSuccessRate.text()
        if str(sRate).__len__() == 0:
            sRate = "0"
        # Model seçilmemişse uyarı verme
        rateLimit = 35
        if modelName.__eq__("Model Seçiniz") or int(sRate) < int(rateLimit):
            if modelName.__eq__("Model Seçiniz"):
                getMsgBoxFeatures(QMessageBox(self), "Uyarı", "Lütfen bir model seçin.", QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            if int(sRate) < int(rateLimit):
                getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                  "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer girin.",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
        else:
            # Mesaj kutusunu gösterme
            # self.showWarn()

            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter(
                'Tümü (*.jpg *.jpeg *.png *.mp4);;Resimler (*.jpg *.jpeg *.png);;Videolar (*.mp4)')
            if file_dialog.exec_():
                filePath = file_dialog.selectedFiles()[0]
                # url = QtCore.QUrl.fromLocalFile(filePath).toString()  # Dosya yolunu URL'e dönüştürün
                if re.search("[ıİğĞüÜşŞöÖçÇ]", filePath):
                    getMsgBoxFeatures(QMessageBox(self), "Uyarı", "Lütfen 'Türkçe Karakter' içermeyen bir yol seçin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                elif filePath.endswith('.jpg') or filePath.endswith('.jpeg') or filePath.endswith('.png'):
                    testImage(imagePath=filePath, modelName=modelName, successRate=sRate)
                elif filePath.endswith('.mp4'):
                    testVideo(videoPath=filePath, modelName=modelName, successRate=sRate)
                else:
                    getMsgBoxFeatures(QMessageBox(self), "Hata", "Desteklenmeyen dosya biçimi!", QMessageBox.Critical,
                                      QMessageBox.Ok, isQuestion=False).exec_()

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
                    getMsgBoxFeatures(QMessageBox(self), "Uyarı", "Lütfen bir model seçin.", QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                if int(sRate) < int(rateLimit):
                    getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                      "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer girin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
            else:
                # Mesaj kutusunu gösterme
                # self.showWarn()

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
                btnImageUrl.clicked.connect(self.testUrlImageScreen)
                layoutImage = QHBoxLayout()
                layoutImage.addWidget(btnImageUrl)

                #################
                # Y O U T U B E #
                #################
                btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
                btnVideoYoutube.clicked.connect(self.testUrlYoutubeScreen)
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

    def testUrlImageScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Url')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngImageUrl))

        # eğitilmiş yüz tanıma modelinin sonuçlarını içeren dosyayı aç
        with open(pathFaceResultsMap + self.selectedModel.replace(".h5", ".pkl"), 'rb') as fileReadStream:
            resultMap = pickle.load(fileReadStream)

        randomId = random.choice(list(resultMap.keys()))
        name = resultMap[randomId]

        webbrowser.open("https://www.google.com/search?q=" + str(name).replace(" ",
                                                                               "+") + "&sxsrf=APwXEdesmw72efa4-dds-FUED9TjAXQVAQ:1680383725172&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjhu5mYzYn-AhVLQvEDHS4EBnMQ_AUoAnoECAEQBA&biw=951&bih=612&dpr=1")
        # URL'nin görüntülendiği etiket
        labelInfo = getLabelFeatures(QLabel("Görüntü bağlantısını yapıştırın.", self.window), False, True)
        labelInfo.setAlignment(Qt.AlignCenter)
        labelInfo.setGeometry(0, 0, mainWith, mainHeight)

        # Ana düzenleyici
        layout = QVBoxLayout()
        layout.addWidget(labelInfo)

        textBoxGetUrl = getTextBoxFeatures(QLineEdit(self), "", isVisible=True)
        layout.addWidget(textBoxGetUrl)
        buttonLayout = QHBoxLayout()

        btnFaceScanner = getFaceButtonFeatures(QPushButton(self), pngFaceDetection0, isVisible=True)
        buttonLayout.addWidget(btnFaceScanner)
        layout.addLayout(buttonLayout)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.setObjectName("testUrlImageScreen")
        self.window.show()
        # Metin kutusunu dinle
        textBoxGetUrl.textChanged.connect(lambda: self.updateButtonStatus(textBoxGetUrl, btnFaceScanner))

    def updateButtonStatus(self, textBoxGetUrl, btnFaceScanner):
        # Metin kutusunun içeriğini al
        text = textBoxGetUrl.text()

        # Metin kutusunun uzunluğunu kontrol et
        if len(text) <= 1:
            btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection0))
        else:
            # URL doğrulaması yap
            pattern = re.compile(r'https?://.*\.(jpg|png|jpeg)', re.IGNORECASE)
            if pattern.match(text):
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection1))
                btnFaceScanner.clicked.connect(lambda: self.getImage(textBoxGetUrl, btnFaceScanner))
            else:
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection0))

    def getImage(self, textBoxGetUrl, btnFaceScanner):
        response = requests.get(textBoxGetUrl.text())
        arr = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        faceCascade = cv2.CascadeClassifier(pathFaceCascade)
        if img is None:
            getMsgBoxFeatures(QMessageBox(self), "Hata",
                              "Resim yüklenemedi.",
                              QMessageBox.Critical,
                              QMessageBox.Ok, isQuestion=False).exec_()
            textBoxGetUrl.setText("")
            btnFaceScanner.setIcon(QtGui.QIcon(pngFace404))
            # Çarpı işaretine basıldığında eski pencere açılsın
            self.window.setAttribute(Qt.WA_DeleteOnClose)
            self.window.destroyed.connect(self.testUrlScreen)

        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Yüzleri algıla
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                name = pathTempFolder + randomString(10) + ".jpg"
                cv2.imwrite(name, img)
                imgg = cv2.imread(name)
                self.openAnalizedImageScreen(imgg, name)
            else:
                getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                  "Yüz bulunamadı.",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
                btnFaceScanner.setIcon(QtGui.QIcon(pngFace404))

    def openAnalizedImageScreen(self, imgg, name):
        height, width, channels = imgg.shape
        imgWith = width
        imgHeight = height
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Sonuç')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngFaceDetection2))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.testUrlScreen)

        btn = QPushButton(self)
        btn.setIcon(QtGui.QIcon(name))

        if int(imgWith) > int(screenWidth - screenWidth * 0.2):
            imgWith = int(screenWidth - screenWidth * 0.2)
        if int(imgHeight) > int(screenHeight - screenHeight * 0.2):
            imgHeight = int(screenHeight - screenHeight * 0.2)

        btn.setFixedSize(imgWith, imgHeight)
        btn.setIconSize(QtCore.QSize(imgWith, imgHeight))

        # Ana düzenleyici
        layoutFace = QVBoxLayout()
        layoutFace.addWidget(btn)

        self.window.setLayout(layoutFace)
        self.window.setGeometry(int(screenWidth / 2 - int(imgWith / 2)), int(screenHeight / 2 - int(imgHeight / 2)),
                                imgWith, imgHeight)
        self.window.show()

    def testUrlYoutubeScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Youtube')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngYoutube))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.testUrlScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def showWarn(self):
        getMsgBoxFeatures(QMessageBox(self), "Kullanılacak Model ve Başarı Oranı",
                          self.selectedModel + "\nBaşarı oranı " + str(
                              self.textBoxSuccessRate.text()) + " olarak belirlenmiştir.",
                          QMessageBox.Information, QMessageBox.Ok, isQuestion=False).exec_()

    def getIsMainScreenClosing(self):
        return self.isMainScreenClosing

    def setIsMainScreenClosing(self, value):
        self.isMainScreenClosing = value


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
