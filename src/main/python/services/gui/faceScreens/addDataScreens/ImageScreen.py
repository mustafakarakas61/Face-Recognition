import os
import re

import cv2
import numpy as np
import requests
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QPushButton, QLabel, QLineEdit

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, getTextBoxSuccessRateFeatures, \
    getButtonFeaturesTrain, fontTextBox, getFaceButtonFeatures, getExceptionMsgBox
from src.resources.Environments import pngImageUrl, pngWarningBox, pathDatasets, pngAdd, pngInfoBox, pngSaveImage0, \
    pngSaveImage1, pngErrorBox, pathFaceCascade, inputSize, minFaceSize, pathTempFolder, pngClearText, pngDeleteImage0, \
    pngDeleteImage1
from utils.Utils import dataCount, useEnviron, changeNameToASCII, checkFolder, checkJpgFileOfTheHaveNumber, switchFiles

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize


class Image(QWidget):
    def __init__(self, mainWidget):
        super(Image, self).__init__()
        self.startSaveWindow = None
        self.textboxDataInfoCount = None
        self.saveStatus: bool = False
        self.showException: bool = False
        self.saveData = None
        self.outputPath = None

        self.window = None
        self.mainWidget = mainWidget

    def faceAddImageUrlScreen(self):
        datasetName: str = self.mainWidget.selectedDatasetName
        datasetDataName: str = self.mainWidget.selectedDatasetDataName
        if datasetName.__eq__("Veriseti Seçiniz") or datasetDataName.__eq__(
                "Veri Seçiniz") or datasetName is None or datasetDataName is None:
            if datasetName.__eq__("Veriseti Seçiniz") or datasetName is None:
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir <b>veriseti</b> seçin",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            if not datasetName.__eq__("Veriseti Seçiniz") or datasetName is not None:
                if datasetDataName.__eq__("Veri Seçiniz") or datasetDataName is None:
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir <b>veri</b> seçin",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
        else:
            mainWidth = 320
            mainHeight = 150
            screen = QtWidgets.QApplication.desktop().screenGeometry()
            screenWidth, screenHeight = screen.width(), screen.height()

            self.window = QWidget()
            self.window.setWindowTitle('Image Url')
            self.window.setStyleSheet("background-color: white;")
            self.window.setWindowIcon(QIcon(pngImageUrl))

            # URL'nin görüntülendiği etiket
            labelInfo = getLabelFeatures(QLabel("Görüntü bağlantısını yapıştırın.", self.window), False, True)
            labelInfo.setAlignment(Qt.AlignCenter)
            labelInfo.setGeometry(0, 0, mainWidth, mainHeight)

            # Ana düzenleyici
            layout = QVBoxLayout()
            layout.addWidget(labelInfo)

            textBoxGetUrl = QLineEdit()
            textBoxGetUrl.setFont(fontTextBox)

            layout.addWidget(textBoxGetUrl)
            buttonLayout = QHBoxLayout()

            btnClearText = getFaceButtonFeatures(QPushButton(self), pngClearText, isVisible=True)
            btnFaceScanner = getFaceButtonFeatures(QPushButton(self), pngSaveImage0, isVisible=True)
            btnDeleteFace = getFaceButtonFeatures(QPushButton(self), pngDeleteImage0, isVisible=True)
            buttonLayout.addWidget(btnClearText)
            buttonLayout.addWidget(btnFaceScanner)
            buttonLayout.addWidget(btnDeleteFace)
            layout.addLayout(buttonLayout)

            self.window.setLayout(layout)
            self.window.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                    int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWidth, mainHeight)
            self.window.setObjectName("ImageScreen")
            self.window.show()

            textBoxGetUrl.textChanged.connect(
                lambda: self.updateUrlImageButtonStatus(textBoxGetUrl, btnFaceScanner, datasetName, datasetDataName,
                                                        btnDeleteFace))

            btnClearText.clicked.connect(
                lambda: self.deleteText(textBoxGetUrl)
            )

            btnDeleteFace.clicked.connect(
                lambda: self.deleteSavedFace(self.getOutputPath(), btnDeleteFace)
            )

    def deleteSavedFace(self, savedImagePath, btnDeleteFace: QPushButton):
        if savedImagePath is not None:
            reply = getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Dikkat!", 'Tespit edilen yüz silinsin mi?',
                                      QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                      isQuestion=True).exec_()

            if reply == QtWidgets.QMessageBox.Yes:
                if os.path.exists(savedImagePath):
                    os.remove(savedImagePath)
                self.setOutputPath(None, button=btnDeleteFace, isCameraClosed=True)
            else:
                getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Bilgi",
                                  "Silme işlemi iptal edildi.",
                                  QMessageBox.Critical,
                                  QMessageBox.Ok, isQuestion=False).exec_()

    def updateUrlImageButtonStatus(self, textBoxGetUrl, btnFaceScanner, datasetName, datasetDataName, btnDeleteFace):
        # Metin kutusunun içeriğini al
        text = textBoxGetUrl.text()

        # Metin kutusunun uzunluğunu kontrol et
        if len(text) <= 1:
            btnFaceScanner.setIcon(QtGui.QIcon(pngSaveImage0))
        else:
            # URL doğrulaması yap
            pattern = re.compile(r'https?://.*\.(jpg|png|jpeg)', re.IGNORECASE)
            if pattern.match(text):
                btnFaceScanner.setIcon(QtGui.QIcon(pngSaveImage1))
                self.mainWidget.control = True
                btnFaceScanner.clicked.connect(
                    lambda: self.getImage(textBoxGetUrl=textBoxGetUrl, datasetName=datasetName,
                                          datasetDataName=datasetDataName, btnDeleteFace=btnDeleteFace))
            else:
                btnFaceScanner.setIcon(QtGui.QIcon(pngSaveImage0))

    def getImage(self, textBoxGetUrl, datasetName: str, datasetDataName: str, btnDeleteFace: QPushButton):
        self.closeCv2()
        self.setOutputPath(None, button=btnDeleteFace, isCameraClosed=False)
        self.setSaveStatus(True)
        self.setShowExceptionStatus(True)
        if len(textBoxGetUrl.text()) > 1:
            try:
                isThereTurkishChar: bool = False
                originalSavePath: str = pathDatasets + datasetName + "/" + datasetDataName

                response = requests.get(textBoxGetUrl.text(), timeout=10)
                if response.status_code == 200:
                    arr = np.asarray(bytearray(response.content), dtype=np.uint8)
                    img = cv2.imdecode(arr, -1)

                    if img is None:
                        getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Hata",
                                          "Resim yüklenemedi.",
                                          QMessageBox.Critical,
                                          QMessageBox.Ok, isQuestion=False).exec_()
                        self.window.setAttribute(Qt.WA_DeleteOnClose)
                        self.window.destroyed.connect(self.closeCv2)
                        self.window.close()

                    else:
                        if re.search("[ıİğĞüÜşŞöÖçÇ]", datasetDataName):
                            isThereTurkishChar = True

                        if isThereTurkishChar:
                            asciiDatasetDataName: str = changeNameToASCII(datasetDataName)
                            asciiSavePath: str = pathTempFolder + asciiDatasetDataName
                            checkFolder(asciiSavePath)

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        # Yüzleri algıla
                        faces = faceCascade.detectMultiScale(
                            gray,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(minFaceSize, minFaceSize)
                        )

                        if len(faces) > 0:
                            if self.getSaveStatus():
                                self.setSaveStatus(False)
                                idx = np.random.randint(0, len(faces))
                                (x, y, w, h) = faces[idx]
                                faceImage = img[y:y + h, x:x + w]
                                faceImage = cv2.resize(faceImage, (size, size))
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                                cv2.putText(img, "Yuz kaydedildi.", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                            (255, 0, 0),
                                            2)

                                if isThereTurkishChar:
                                    tempFileName = checkJpgFileOfTheHaveNumber(originalSavePath,
                                                                               datasetDataName + "_1.jpg")
                                    numberOfFile = tempFileName.split("_")[1].replace(".jpg", "")
                                    self.setOutputPath(asciiSavePath + "/" + tempFileName, button=btnDeleteFace,
                                                       isCameraClosed=False)
                                else:
                                    tempFileName = checkJpgFileOfTheHaveNumber(originalSavePath,
                                                                               datasetDataName + "_1.jpg")
                                    numberOfFile = tempFileName.split("_")[1].replace(".jpg", "")
                                    self.setOutputPath(originalSavePath + "/" + tempFileName, button=btnDeleteFace,
                                                       isCameraClosed=False)

                                cv2.imwrite(self.getOutputPath(), faceImage)
                                self.deleteText(textBoxGetUrl)

                                if isThereTurkishChar:
                                    for i, file in enumerate(os.listdir(asciiSavePath)):
                                        os.rename(os.path.join(asciiSavePath, file),
                                                  os.path.join(asciiSavePath,
                                                               datasetDataName + "_" + numberOfFile + ".jpg"))

                                    switchFiles(asciiSavePath, originalSavePath)

                                height, width, _ = img.shape

                                screen = QtWidgets.QApplication.desktop().screenGeometry()
                                screenWidth, screenHeight = screen.width(), screen.height()

                                if ((width * 2) / 3) > screenWidth or ((height * 2) / 3) > screenHeight:
                                    scale_percent = 20
                                    new_width = int(width * scale_percent / 100)
                                    new_height = int(height * scale_percent / 100)
                                    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

                                    cv2.imshow('Resim', resized_img)
                                    cv2.waitKey(0)
                                else:
                                    cv2.imshow('Resim', img)
                                    cv2.waitKey(0)

                        else:
                            getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                              "Yüz bulunamadı.",
                                              QMessageBox.Warning,
                                              QMessageBox.Ok, isQuestion=False).exec_()
                            # self.window.setAttribute(Qt.WA_DeleteOnClose)
                            # self.window.destroyed.connect(self.closeScreen)
                elif self.mainWidget.control:
                    getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Hata",
                                      "Resim indirilemedi.",
                                      QMessageBox.Critical,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                    self.mainWidget.control = False
            except Exception as e:
                if self.getShowExceptionStatus():
                    getExceptionMsgBox(QMessageBox(self),
                                       str("Resim URL'sinden bir veri alınamadı : " + str(e))).exec_()
                    self.setShowExceptionStatus(False)
                    self.mainWidget.control = False

    def closeCv2(self):
        cv2.destroyAllWindows()

    def closeScreen(self):
        if self.window is not None:
            self.window.close()
        self.closeCv2()

    def deleteText(self, textBoxGetUrl: QLineEdit):
        textBoxGetUrl.clear()

    def getOutputPath(self):
        return self.outputPath

    def setOutputPath(self, nameOutput, button: QPushButton, isCameraClosed: bool):
        if nameOutput is not None:
            button.setIcon(QtGui.QIcon(pngDeleteImage1))
        else:
            button.setIcon(QtGui.QIcon(pngDeleteImage0))
            if isCameraClosed:
                self.closeCv2()
        self.outputPath = nameOutput

    def getShowExceptionStatus(self):
        return self.showException

    def setShowExceptionStatus(self, status: bool):
        self.showException = status

    def getSaveStatus(self):
        return self.saveStatus

    def setSaveStatus(self, status: bool):
        self.saveStatus = status
