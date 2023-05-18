import os
import re

import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, getTextBoxSuccessRateFeatures, \
    getButtonFeaturesTrain
from src.resources.Environments import pngFolder, pngWarningBox, pathDatasets, pngInfoBox, pngAdd, pngErrorBox, \
    pathFaceCascade, inputSize, minFaceSize, pathTempFolder
from utils.Utils import dataCount, useEnviron, checkJpgFileOfTheHaveNumber, changeNameToASCII, checkFolder, switchFiles

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize


class LocalFile(QWidget):
    def __init__(self, mainWidget):
        super(LocalFile, self).__init__()
        self.startSaveWindow = None
        # self.textboxDataInfoCount = None
        self.closeCameraStatus: bool = False
        self.saveStatus: bool = False
        self.isSaveButtonOpen: bool = False
        self.saveData = None

        self.window = None
        self.mainWidget = mainWidget

    def faceAddLocalFileScreen(self):
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
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter(
                'Tümü (*.jpg *.jpeg *.png *.mp4);;Resimler (*.jpg *.jpeg *.png);;Videolar (*.mp4)')
            if file_dialog.exec_():
                filePath = file_dialog.selectedFiles()[0]
                # url = QtCore.QUrl.fromLocalFile(filePath).toString()  # Dosya yolunu URL'e dönüştürün
                if re.search("[ıİğĞüÜşŞöÖçÇ]", filePath):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                      "Lütfen 'Türkçe Karakter' içermeyen bir yol seçin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                elif filePath.endswith('.jpg') or filePath.endswith('.jpeg') or filePath.endswith('.png'):
                    self.addDataFromImage(imagePath=filePath, datasetName=datasetName, datasetDataName=datasetDataName)
                elif filePath.endswith('.mp4'):
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
                    self.addDataFromVideo(videoPath=filePath, datasetName=datasetName, datasetDataName=datasetDataName)
                else:
                    getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Hata", "Desteklenmeyen dosya biçimi!",
                                      QMessageBox.Critical,
                                      QMessageBox.Ok, isQuestion=False).exec_()

    def addDataFromImage(self, imagePath: str, datasetName: str, datasetDataName: str):
        isThereTurkishChar: bool = False
        originalSavePath: str = pathDatasets + datasetName + "/" + datasetDataName

        img = cv2.imread(imagePath)

        if re.search("[ıİğĞüÜşŞöÖçÇ]", datasetDataName):
            isThereTurkishChar = True

        if isThereTurkishChar:
            asciiDatasetDataName: str = changeNameToASCII(datasetDataName)
            asciiSavePath: str = pathTempFolder + asciiDatasetDataName
            checkFolder(asciiSavePath)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Yüzleri tespit edin
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(minFaceSize, minFaceSize))

        for (x, y, w, h) in faces:
            # Yüz bölgesinin kesilmesi ve boyutlandırılması
            faceImage = img[y:y + h, x:x + w]
            faceImage = cv2.resize(faceImage, (size, size))
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Yuz kaydedildi.", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                        2)

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

        cv2.imshow('Resim', img)
        cv2.waitKey(0)

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

    def closeSaveProcess(self):
        if not self.mainWidget.getIsMainScreenClosing():
            self.setCloseCameraStatus(True)
            self.setSaveButtonOpenStatus(False)
            self.startSaveWindow.close()

    def saveFace(self):
        self.setCloseCameraStatus(False)
        self.saveStatus = True

    def addDataFromVideo(self, videoPath: str, datasetName: str, datasetDataName: str):
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

    # def updateCount(self, datasetName: str, datasetDataName: str):
    #     newCount: int = dataCount(pathDatasets + datasetName + "/" + datasetDataName)
    #     if self.textboxDataInfoCount is not None:
    #         self.textboxDataInfoCount.setText(str(newCount))

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
