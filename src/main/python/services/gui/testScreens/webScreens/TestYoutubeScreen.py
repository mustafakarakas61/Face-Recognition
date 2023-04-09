import pickle
import re
import webbrowser
import random

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, \
    getFaceButtonFeatures, fontTextBox
from src.main.python.services.YoutubeDownloaderService import downloadYoutubeVideo
from src.main.python.services.gui.testScreens.TestLocalFileScreen import testVideo
from src.resources.Environments import pngYoutube, pathFaceResultsMap, pngFaceDetectionYoutube0, \
    pngFaceDetectionYoutube1


class TestYoutube(QWidget):
    def __init__(self, mainWidget):
        super(TestYoutube, self).__init__()
        self.mainWidget = mainWidget
        self.controlOpenYoutube = True
        self.startTimeText = "00:00:00"
        self.endTimeText = "00:00:00"

    def onTextBoxStartTimeChanged(self, text):
        self.startTimeText = text

    def onTextBoxEndTimeChanged(self, text):
        self.endTimeText = text

    def testUrlYoutubeScreen(self):
        mainWidth = 300
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Youtube')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngYoutube))

        if self.controlOpenYoutube:
            # eğitilmiş yüz tanıma modelinin sonuçlarını içeren dosyayı aç
            with open(pathFaceResultsMap + self.mainWidget.selectedModel.replace(".h5", ".pkl"),
                      'rb') as fileReadStream:
                resultMap = pickle.load(fileReadStream)

            randomId = random.choice(list(resultMap.keys()))
            name = resultMap[randomId]

            webbrowser.open("https://www.youtube.com/results?search_query=" + str(name).replace(" ", "+"))
            self.controlOpenYoutube = False

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

        # # Çarpı işaretine basıldığında eski pencere açılsın
        # self.window.setAttribute(Qt.WA_DeleteOnClose)
        # self.window.destroyed.connect(self.testUrlScreen)

        self.window.setLayout(layoutV)
        self.window.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)
        self.window.setObjectName("testUrlYoutubeScreen")
        self.window.show()

        textBoxStartTime.textChanged.connect(lambda index: self.onTextBoxStartTimeChanged(textBoxStartTime.text()))
        textBoxEndTime.textChanged.connect(lambda index: self.onTextBoxEndTimeChanged(textBoxEndTime.text()))

        textBoxGetUrl.textChanged.connect(
            lambda: self.updateUrlYoutubeButtonStatus(textBoxGetUrl, btnFaceScanner))

    def updateUrlYoutubeButtonStatus(self, textBoxGetUrl, btnFaceScanner):
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
                    lambda: self.getVideo(url, self.startTimeText, self.endTimeText,
                                          self.mainWidget.selectedModel, self.mainWidget.textBoxSuccessRate.text()))
            else:
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetectionYoutube0))

    # todo : inen videolar, kliplenen videolar silinsin
    def getVideo(self, url, startTime, endTime, modelName, sRate):
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
                getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                  "Lütfen geçerli formatta (HH:mm:ss) zaman giriniz!",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            elif durationStartTime >= durationEndTime:
                getMsgBoxFeatures(QMessageBox(self), "Uyarı",
                                  "Videonun başlangıç süresi, bitiş süresinden büyük veya eşit olamaz!",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            else:
                filePath = downloadYoutubeVideo(url=url, startTime=str(startTime),
                                                durationStartTime=int(durationStartTime),
                                                durationEndTime=int(durationEndTime))
                testVideo(videoPath=str(filePath), modelName=str(modelName), successRate=int(sRate))

                self.window.setAttribute(Qt.WA_DeleteOnClose)
                self.window.destroyed.connect(self.testUrlYoutubeScreen())
                self.window.close()
        except Exception as e:
            # getExceptionMsgBox(QMessageBox(self), str(e)).exec_()
            self.window.close()
