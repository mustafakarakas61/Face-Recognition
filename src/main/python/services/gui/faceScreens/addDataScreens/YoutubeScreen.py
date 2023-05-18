import os
import re

import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QPushButton, QLabel, QLineEdit

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, getTextBoxSuccessRateFeatures, \
    getButtonFeaturesTrain, fontTextBox, getFaceButtonFeatures, getExceptionMsgBox
from src.main.python.services.YoutubeDownloaderService import downloadYoutubeVideo
from src.resources.Environments import pngYoutube, pngWarningBox, pathDatasets, pngAdd, pngInfoBox, \
    pngFaceDetectionYoutube0, pngFaceDetectionYoutube1, minFaceSize, pathTempFolder, inputSize, pathFaceCascade
from utils.Utils import dataCount, switchFiles, checkJpgFileOfTheHaveNumber, changeNameToASCII, checkFolder, useEnviron

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize

class Youtube(QWidget):
    def __init__(self, mainWidget):
        super(Youtube, self).__init__()
        self.startSaveWindow = None
        self.textboxDataInfoCount = None
        self.closeCameraStatus: bool = False
        self.saveStatus: bool = False
        self.showException: bool = False
        self.isSaveButtonOpen: bool = False
        self.saveData = None

        self.startTimeText = "00:00:00"
        self.endTimeText = "00:00:00"

        self.window = None
        self.mainWidget = mainWidget

    def faceAddVideoYoutubeScreen(self):
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
            mainWidth = 300
            mainHeight = 150
            screen = QtWidgets.QApplication.desktop().screenGeometry()
            screenWidth, screenHeight = screen.width(), screen.height()

            self.window = QWidget()
            self.window.setWindowTitle('Youtube Url')
            self.window.setStyleSheet("background-color: white;")
            self.window.setWindowIcon(QIcon(pngYoutube))

            # URL'nin görüntülendiği etiket
            labelInfo = getLabelFeatures(QLabel("Youtube bağlantısını yapıştırın.", self.window), False, True)
            labelInfo.setAlignment(Qt.AlignCenter)
            labelInfo.setGeometry(0, 0, mainWidth, mainHeight)

            # Ana düzenleyici V _   H |
            layoutV = QVBoxLayout()
            layoutV.addWidget(labelInfo)

            textBoxGetUrl = QLineEdit()
            textBoxGetUrl.setFont(fontTextBox)
            layoutV.addWidget(textBoxGetUrl)
            layoutH = QHBoxLayout()

            btnFaceScanner = getFaceButtonFeatures(QPushButton(self), pngFaceDetectionYoutube0, isVisible=True)

            layoutStartV = QVBoxLayout()
            labelStartInfo = getLabelFeatures(QLabel("Başlangıç", self.window), False, True)
            textBoxStartTime = QLineEdit()
            textBoxStartTime.setFont(fontTextBox)

            textBoxStartTime.setInputMask("99:99:99")
            textBoxStartTime.setText("00:00:00")
            layoutStartV.addWidget(labelStartInfo)
            layoutStartV.addWidget(textBoxStartTime)

            layoutH.addLayout(layoutStartV)
            layoutH.addWidget(btnFaceScanner)

            layoutEndV = QVBoxLayout()
            labelEndInfo = getLabelFeatures(QLabel("Bitiş", self.window), False, True)
            textBoxEndTime = QLineEdit()
            textBoxEndTime.setFont(fontTextBox)
            textBoxEndTime.setInputMask("99:99:99")
            textBoxEndTime.setText("00:00:00")
            layoutEndV.addWidget(labelEndInfo)
            layoutEndV.addWidget(textBoxEndTime, alignment=Qt.AlignCenter)

            layoutH.addLayout(layoutEndV)

            layoutV.addLayout(layoutH)

            self.window.setLayout(layoutV)
            self.window.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                    int(screenHeight / 2 - int(mainHeight / 2)),
                                    mainWidth, mainHeight)
            self.window.setObjectName("YoutubeScreen")
            self.window.show()

            textBoxStartTime.textChanged.connect(lambda index: self.onTextBoxStartTimeChanged(textBoxStartTime.text()))
            textBoxEndTime.textChanged.connect(lambda index: self.onTextBoxEndTimeChanged(textBoxEndTime.text()))

            textBoxGetUrl.textChanged.connect(
                lambda: self.updateUrlYoutubeButtonStatus(textBoxGetUrl, btnFaceScanner, datasetName, datasetDataName))

    def updateUrlYoutubeButtonStatus(self, textBoxGetUrl, btnFaceScanner, datasetName: str, datasetDataName: str):
        # Metin kutusunun içeriğini al
        url = str(textBoxGetUrl.text())

        # Metin kutusunun uzunluğunu kontrol et
        if len(url) <= 1:
            btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetectionYoutube0))
        else:
            # URL doğrulaması yap
            pattern = re.compile(
                r'(?:https?://)?(?:www\.)?(?:youtu\.be|youtube\.com)/(?:watch\?v=)?(?:shorts/)?([\w-]{11})',
                re.IGNORECASE)
            if pattern.match(url):
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetectionYoutube1))
                self.mainWidget.control = True

                btnFaceScanner.clicked.connect(
                    lambda: self.getVideo(url, self.startTimeText, self.endTimeText, datasetName, datasetDataName))
            else:
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetectionYoutube0))

    def getVideo(self, url, startTime, endTime, datasetName: str, datasetDataName: str):
        self.setShowExceptionStatus(True)
        try:
            splitStartTime = str(startTime).split(":")
            sTHH = int(splitStartTime[0]) * int(60 * 60)
            sTMM = int(splitStartTime[1]) * int(60)
            stSS = int(splitStartTime[2])
            durationStartTime = int(sTHH + sTMM + stSS)

            splitEndTime = str(endTime).split(":")
            eTHH = int(splitEndTime[0]) * int(60 * 60)
            eTMM = int(splitEndTime[1]) * int(60)
            etSS = int(splitEndTime[2])
            durationEndTime = int(eTHH + eTMM + etSS)

            if len(self.startTimeText) != 8 and len(self.endTimeText) != 8:
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                  "Lütfen geçerli formatta (HH:mm:ss) zaman giriniz!",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            elif durationStartTime >= durationEndTime:
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                  "Videonun başlangıç süresi, bitiş süresinden büyük veya eşit olamaz!",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            else:
                filePath = downloadYoutubeVideo(url=url, startTime=str(startTime),
                                                durationStartTime=int(durationStartTime),
                                                durationEndTime=int(durationEndTime))
                self.addDataFromYoutube(videoPath=str(filePath), datasetName=datasetName, datasetDataName=datasetDataName)

                self.window.setAttribute(Qt.WA_DeleteOnClose)
                self.window.destroyed.connect(self.faceAddVideoYoutubeScreen())
                self.window.close()

        except Exception as e:
            if self.getShowExceptionStatus():
                getExceptionMsgBox(QMessageBox(self),
                                   str("Youtube URL'sinden bir veri alınamadı : " + str(e))).exec_()
                self.setShowExceptionStatus(False)

    def closeSaveProcess(self):
        if not self.mainWidget.getIsMainScreenClosing():
            self.setCloseCameraStatus(True)
            self.setSaveButtonOpenStatus(False)
            self.startSaveWindow.close()

    def saveFace(self):
        self.setCloseCameraStatus(False)
        self.saveStatus = True

    def addDataFromYoutube(self, videoPath: str, datasetName: str, datasetDataName: str):
        self.setCloseCameraStatus(False)
        self.setSaveButtonOpenStatus(True)
        getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi",
                          "Her yeni bir yüz kaydı için <b>Kaydet</b> butonuna tıklayınız.",
                          QMessageBox.Information,
                          QMessageBox.Ok, isQuestion=False).exec_()

        mainWidth = 220
        mainHeight = 170
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.startSaveWindow = QWidget()
        self.startSaveWindow.setWindowTitle('Yerel')
        self.startSaveWindow.setStyleSheet("background-color: white;")
        self.startSaveWindow.setWindowIcon(QIcon(pngAdd))

        self.saveData: QPushButton = QPushButton(self)
        self.saveData.setFont(QtGui.QFont("Times New Roman", 20))
        self.saveData.setText("Kaydet")
        self.saveData.setFixedSize(200, 150)
        self.saveData.setStyleSheet("background-color: #44d091; color: white; font-weight: bold;")
        self.saveData.clicked.connect(lambda: self.saveFace())

        # Ana düzenleyici
        layoutStartSave = QHBoxLayout()
        layoutStartSave.addWidget(self.saveData)
        layoutStartSave.setAlignment(self.saveData, Qt.AlignCenter)

        self.startSaveWindow.setLayout(layoutStartSave)
        self.startSaveWindow.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                         int(screenHeight / 2 - int(mainHeight / 2)),
                                         mainWidth, mainHeight)
        self.startSaveWindow.closeEvent = self.onClosedSaveProcess
        self.startSaveWindow.show()

        isThereTurkishChar: bool = False
        originalSavePath: str = pathDatasets + datasetName + "/" + datasetDataName

        videoCapture = cv2.VideoCapture(videoPath)

        if re.search("[ıİğĞüÜşŞöÖçÇ]", datasetDataName):
            isThereTurkishChar = True

        if isThereTurkishChar:
            asciiDatasetDataName: str = changeNameToASCII(datasetDataName)
            asciiSavePath: str = pathTempFolder + asciiDatasetDataName
            checkFolder(asciiSavePath)

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        videoWidth = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if int(videoWidth) > int(screenWidth * 0.8) or int(videoHeight) > int(screenHeight * 0.8):
            videoWidth = int(screenWidth * 0.7)
            videoHeight = int(screenHeight * 0.7)

        # Açılan videonun boyutunu değiştirme
        videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, videoWidth)
        videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, videoHeight)

        while True:
            _, frame = videoCapture.read()

            if not _:
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Bilgi", "Video sonuna ulaşıldı.",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
                if not self.mainWidget.getIsMainScreenClosing():
                    self.setCloseCameraStatus(True)
                    self.setSaveButtonOpenStatus(False)
                    self.startSaveWindow.close()
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(minFaceSize, minFaceSize)
            )

            # Yüz tespit edildiğinde yüzü kaydet
            for (x, y, w, h) in faces:
                faceImage = frame[y:y + h, x:x + w]
                faceImage = cv2.resize(faceImage, (size, size))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

                if self.saveStatus and self.getCloseCameraStatus() is False:
                    self.saveStatus = False
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # green
                    cv2.putText(frame, "Yuz kaydedildi.", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0),
                                2)  # green

                    if isThereTurkishChar:
                        tempFileName = checkJpgFileOfTheHaveNumber(originalSavePath, datasetDataName + "_1.jpg")
                        numberOfFile = tempFileName.split("_")[1].replace(".jpg", "")
                        outputPath = asciiSavePath + "/" + tempFileName
                    else:
                        tempFileName = checkJpgFileOfTheHaveNumber(originalSavePath, datasetDataName + "_1.jpg")
                        numberOfFile = tempFileName.split("_")[1].replace(".jpg", "")
                        outputPath = originalSavePath + "/" + tempFileName

                    cv2.imwrite(outputPath, faceImage)

                    if isThereTurkishChar:
                        for i, file in enumerate(os.listdir(asciiSavePath)):
                            os.rename(os.path.join(asciiSavePath, file),
                                      os.path.join(asciiSavePath, datasetDataName + "_" + numberOfFile + ".jpg"))

                        switchFiles(asciiSavePath, originalSavePath)

                    # self.updateCount(datasetName, datasetDataName)

            cv2.imshow('Video', frame)

            if self.getCloseCameraStatus():
                if self.getSaveButtonOpenStatus():
                    self.closeSaveProcess()
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if self.getSaveButtonOpenStatus():
                    self.closeSaveProcess()
                break
            if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
                if self.getSaveButtonOpenStatus():
                    self.closeSaveProcess()
                break

        videoCapture.release()
        cv2.destroyAllWindows()

    def onTextBoxStartTimeChanged(self, text):
        self.startTimeText = text

    def onTextBoxEndTimeChanged(self, text):
        self.endTimeText = text

    def onClosedSaveProcess(self, event):
        if not self.mainWidget.getIsMainScreenClosing():
            if self.getSaveButtonOpenStatus():
                reply = getMsgBoxFeatures(QMessageBox(), pngWarningBox, "Dikkat!",
                                          'Kaydet işlemi bitirilsin mi?',
                                          QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                          isQuestion=True).exec_()
                if reply == QtWidgets.QMessageBox.Yes:
                    self.setCloseCameraStatus(True)
                    self.setSaveButtonOpenStatus(False)
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()

    def closeScreen(self):
        if self.window is not None:
            self.window.close()

    def getCloseCameraStatus(self):
        return self.closeCameraStatus

    def setCloseCameraStatus(self, newStatus: bool):
        self.closeCameraStatus = newStatus

    def getSaveButtonOpenStatus(self):
        return self.isSaveButtonOpen

    def setSaveButtonOpenStatus(self, newStatus: bool):
        self.isSaveButtonOpen = newStatus

    def getShowExceptionStatus(self):
        return self.showException

    def setShowExceptionStatus(self, status: bool):
        self.showException = status
