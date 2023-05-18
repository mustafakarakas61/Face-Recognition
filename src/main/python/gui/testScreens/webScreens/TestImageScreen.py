import pickle
import re
import webbrowser
import random

import cv2
import numpy as np
import requests
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox

from keras.models import load_model
from keras.api.keras.preprocessing import image

from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, \
    getFaceButtonFeatures, getExceptionMsgBox, fontTextBox
from src.resources.Environments import pathFaceResultsMap, pngImageUrl, pngFaceDetection0, pngFaceDetection1, \
    pathFaceCascade, minFaceSize, inputSize, pathModels, pathTempFolder, pngFaceDetection2, pngWarningBox, pngErrorBox
from utils.Utils import changeNameToASCII, randomString


class TestImage(QWidget):
    def __init__(self, mainWidget):
        super(TestImage, self).__init__()
        self.mainWidget = mainWidget
        self.controlOpenGoogle = True

    def testUrlImageScreen(self):
        mainWidth = 300
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Url')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngImageUrl))

        if self.controlOpenGoogle:
            with open(pathFaceResultsMap + self.mainWidget.selectedModel.replace(".h5", ".pkl"), 'rb') as fileReadStream:
                resultMap = pickle.load(fileReadStream)

            randomId = random.choice(list(resultMap.keys()))
            name = resultMap[randomId]

            webbrowser.open("https://www.google.com/search?q=" + str(name).replace(" ",
                                                                                   "+") + "&sxsrf=APwXEdesmw72efa4-dds-FUED9TjAXQVAQ:1680383725172&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjhu5mYzYn-AhVLQvEDHS4EBnMQ_AUoAnoECAEQBA&biw=951&bih=612&dpr=1")
            self.controlOpenGoogle = False
        labelInfo = getLabelFeatures(QLabel("Görüntü bağlantısını yapıştırın.", self.window), False, True)
        labelInfo.setAlignment(Qt.AlignCenter)
        labelInfo.setGeometry(0, 0, mainWidth, mainHeight)

        layout = QVBoxLayout()
        layout.addWidget(labelInfo)

        textBoxGetUrl = QLineEdit()
        textBoxGetUrl.setFont(fontTextBox)

        layout.addWidget(textBoxGetUrl)
        buttonLayout = QHBoxLayout()

        btnFaceScanner = getFaceButtonFeatures(QPushButton(self), pngFaceDetection0, isVisible=True)
        buttonLayout.addWidget(btnFaceScanner)
        layout.addLayout(buttonLayout)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth - mainWidth - mainWidth * 0.2),
                                int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWidth, mainHeight)
        self.window.setObjectName("testUrlImageScreen")
        self.window.show()
        textBoxGetUrl.textChanged.connect(lambda: self.updateUrlImageButtonStatus(textBoxGetUrl, btnFaceScanner))

    def updateUrlImageButtonStatus(self, textBoxGetUrl, btnFaceScanner):
        text = textBoxGetUrl.text()

        if len(text) <= 1:
            btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection0))
        else:
            # URL doğrulaması yap
            pattern = re.compile(r'https?://.*\.(jpg|png|jpeg)', re.IGNORECASE)
            if pattern.match(text):
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection1))
                self.mainWidget.control = True
                btnFaceScanner.clicked.connect(lambda: self.getImage(textBoxGetUrl))
            else:
                btnFaceScanner.setIcon(QtGui.QIcon(pngFaceDetection0))

    def getImage(self, textBoxGetUrl):
        try:
            response = requests.get(textBoxGetUrl.text(), timeout=10)
            if response.status_code == 200:
                arr = np.asarray(bytearray(response.content), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)

                faceCascade = cv2.CascadeClassifier(pathFaceCascade)
                if img is None:
                    getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Hata",
                                      "Resim yüklenemedi.",
                                      QMessageBox.Critical,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                    # textBoxGetUrl.setText("")
                    # btnFaceScanner.setIcon(QtGui.QIcon(pngFace404))
                    self.window.setAttribute(Qt.WA_DeleteOnClose)
                    self.window.destroyed.connect(self.testUrlImageScreen)
                    self.window.close()

                else:
                    # Eğitimde kullanılan yüz isimleri ve kodları
                    with open(pathFaceResultsMap + self.mainWidget.selectedModel.replace(".h5", ".pkl"), 'rb') as fileReadStream:
                        ResultMap = pickle.load(fileReadStream)

                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                         minSize=(minFaceSize, minFaceSize))

                    if len(faces) > 0:
                        for (x, y, w, h) in faces:
                            # Yüz bölgesinin kesilmesi ve boyutlandırılması
                            faceImage = img[y:y + h, x:x + w]
                            faceImage = cv2.resize(faceImage, (inputSize, inputSize))
                            faceImage = image.img_to_array(faceImage)
                            faceImage = np.expand_dims(faceImage, axis=0)
                            faceImage /= 255

                            # Yüz tahmini
                            model = load_model(pathModels + self.mainWidget.selectedModel)
                            prediction = model.predict(faceImage, verbose=0)
                            predictedClass = np.argmax(prediction)
                            predictedName = ResultMap[predictedClass]
                            accuracy = round(np.max(prediction) * 100, 2)
                            if int(accuracy) > int(self.mainWidget.textBoxSuccessRate.text()):
                                cv2.putText(img, changeNameToASCII(predictedName) + " " + str(
                                    accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # green
                            else:
                                cv2.putText(img, "%" + str(
                                    accuracy), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # red
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

                        name = pathTempFolder + randomString(10) + ".jpg"
                        cv2.imwrite(name, img)
                        self.openAnalizedImageScreen(name, img)
                    else:
                        getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                          "Yüz bulunamadı.",
                                          QMessageBox.Warning,
                                          QMessageBox.Ok, isQuestion=False).exec_()
                        self.window.setAttribute(Qt.WA_DeleteOnClose)
                        self.window.destroyed.connect(self.testUrlImageScreen)
                        self.window.close()
            elif self.mainWidget.control:
                getMsgBoxFeatures(QMessageBox(self), pngErrorBox, "Hata",
                                  "Resim indirilemedi.",
                                  QMessageBox.Critical,
                                  QMessageBox.Ok, isQuestion=False).exec_()
                self.mainWidget.control = False
                self.window.close()
        except Exception as e:
            getExceptionMsgBox(QMessageBox(self), str(e)).exec_()
            self.mainWidget.control = False
            self.window.close()

    def openAnalizedImageScreen(self, name, img):
        height, width, channels = img.shape
        imgWith = width
        imgHeight = height
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Sonuç')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngFaceDetection2))

        btn = QPushButton(self)
        btn.setIcon(QtGui.QIcon(name))

        if int(imgWith) > int(screenWidth - screenWidth * 0.2):
            imgWith = int(screenWidth - screenWidth * 0.2)
        if int(imgHeight) > int(screenHeight - screenHeight * 0.2):
            imgHeight = int(screenHeight - screenHeight * 0.2)

        btn.setFixedSize(imgWith, imgHeight)
        btn.setIconSize(QtCore.QSize(imgWith, imgHeight))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.mainWidget.testUrlScreen)

        # Ana düzenleyici
        layoutFace = QVBoxLayout()
        layoutFace.addWidget(btn)

        self.window.setLayout(layoutFace)
        self.window.setGeometry(int(screenWidth / 2 - int(imgWith / 2)), int(screenHeight / 2 - int(imgHeight / 2)),
                                imgWith, imgHeight)
        self.window.show()
