import pickle
import re

import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from keras.models import load_model
from keras.api.keras.preprocessing import image

from src.main.python.services.FeaturesService import getMsgBoxFeatures
from src.resources.Environments import pathModels, pathFaceCascade, inputSize, pathFaceResultsMap, minFaceSize, \
    pngMustafa
from utils.Utils import useEnviron, changeNameToASCII

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize


class TestLocalFile(QWidget):
    def __init__(self, mainWidget):
        super(TestLocalFile, self).__init__()
        self.mainWidget = mainWidget
        self.setWindowIcon(QIcon(pngMustafa))

    def testLocalFileScreen(self):
        modelName = self.mainWidget.selectedModel
        sRate = self.mainWidget.textBoxSuccessRate.text()
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


def testImage(imagePath, modelName, successRate):
    model = load_model(pathModels + modelName)
    img = cv2.imread(imagePath)

    # Eğitimde kullanılan yüz isimleri ve kodları
    with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as fileReadStream:
        ResultMap = pickle.load(fileReadStream)

        # Grayscale formata çevirin
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit edin
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(minFaceSize, minFaceSize))

    for (x, y, w, h) in faces:
        # Yüz bölgesinin kesilmesi ve boyutlandırılması
        faceImage = img[y:y + h, x:x + w]
        faceImage = cv2.resize(faceImage, (size, size))
        faceImage = image.img_to_array(faceImage)
        faceImage = np.expand_dims(faceImage, axis=0)
        faceImage /= 255

        # Yüz tahmini
        prediction = model.predict(faceImage, verbose=0)
        predictedClass = np.argmax(prediction)
        predictedName = ResultMap[predictedClass]
        accuracy = round(np.max(prediction) * 100, 2)
        if int(accuracy) > int(successRate):
            cv2.putText(img, changeNameToASCII(predictedName) + " " + str(
                accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(img, "Bilinmeyen", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('Resim', img)
    cv2.waitKey(0)


def testVideo(videoPath, modelName, successRate):
    model = load_model(pathModels + modelName)
    videoCapture = cv2.VideoCapture(videoPath)

    # Eğitimde kullanılan yüz isimleri ve kodları
    with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as fileReadStream:
        ResultMap = pickle.load(fileReadStream)

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
        # Videodan bir frame okuyun
        ret, frame = videoCapture.read()
        # Videonun sonuna geldiyseniz döngüyü sonlandırın
        if not ret:
            break
        # Grayscale formata çevirin
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri tespit edin
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(minFaceSize, minFaceSize))

        # Her yüz için dikdörtgen çizerek gösterin
        for (x, y, w, h) in faces:
            # Yüz bölgesinin kesilmesi ve boyutlandırılması
            faceImage = frame[y:y + h, x:x + w]
            faceImage = cv2.resize(faceImage, (size, size))
            faceImage = image.img_to_array(faceImage)
            faceImage = np.expand_dims(faceImage, axis=0)
            faceImage /= 255

            # Yüz tahmini
            prediction = model.predict(faceImage, verbose=0)
            predictedClass = np.argmax(prediction)
            predictedName = ResultMap[predictedClass]
            accuracy = round(np.max(prediction) * 100, 2)

            if int(accuracy) > int(successRate):
                # Tahmin sonucunun ekrana yazdırılması
                cv2.putText(frame, changeNameToASCII(predictedName) + " " + str(
                    accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, str(accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Frame'i gösterin
        cv2.imshow('Video', frame)

        # "q" tuşuna basarak çıkın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
            break

    # İşlemi bitirin
    videoCapture.release()
    cv2.destroyAllWindows()
