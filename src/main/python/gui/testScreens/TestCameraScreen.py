import cv2
import numpy as np
import pickle

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from keras.api.keras.preprocessing import image
from keras.models import load_model

from src.main.python.services.FeaturesService import getMsgBoxFeatures
from src.resources.Environments import pathModels, pathFaceResultsMap, pathFaceCascade, minFaceSize, \
    inputSize, pngMustafa, pngWarningBox
from src.main.python.services.DatabaseService import updateAttendance
from utils.Utils import useEnviron, changeNameToASCII

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize


class TestCamera(QWidget):
    def __init__(self, mainWidget):
        super(TestCamera, self).__init__()
        self.mainWidget = mainWidget
        self.setWindowIcon(QIcon(pngMustafa))

    def testCameraScreen(self):
        modelName = self.mainWidget.selectedModel
        sRate = self.mainWidget.textBoxSuccessRate.text()
        if str(sRate).__len__() == 0:
            sRate = "0"
        # Model seçilmemişse uyarı verme
        rateLimit = 35
        if modelName.__eq__("Model Seçiniz") or int(sRate) < int(rateLimit):
            if modelName.__eq__("Model Seçiniz"):
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir model seçin", QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
            if int(sRate) < int(rateLimit):
                getMsgBoxFeatures(QMessageBox(self), pngWarningBox,"Uyarı",
                                  "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer giriniz.",
                                  QMessageBox.Warning,
                                  QMessageBox.Ok, isQuestion=False).exec_()
        else:
            # Mesaj kutusunu gösterme
            # self.showWarn()

            testCamera(str(modelName), int(sRate))


def testCamera(modelName, successRate):
    model = load_model(pathModels + modelName)
    videoCapture = cv2.VideoCapture(0)

    # Eğitimde kullanılan yüz isimleri ve kodları
    with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as fileReadStream:
        ResultMap = pickle.load(fileReadStream)

    count = 0
    prevClass = None
    while True:
        # Webcam'den bir kare alınması
        _, frame = videoCapture.read()

        frame = cv2.flip(frame, 1)

        # Gri tonlamalı görüntüye dönüştürme
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüz tespiti
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(minFaceSize, minFaceSize)
        )

        # Görüntü üzerinde tespit edilen yüzlerin tahmin edilmesi
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

            if accuracy > successRate:
                # Tahmin sonucunun ekrana yazdırılması
                cv2.putText(frame, changeNameToASCII(predictedName) + " " + str(
                    accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if predictedClass in ResultMap.keys():
                    # Önceki tahmin sonucu ile karşılaştırma
                    if predictedClass == prevClass:
                        count += 1
                    else:
                        prevClass = predictedClass
                        count = 1

                    # Öğrencinin yoklama bilgisini güncelleme
                    if count == 10:
                        updateAttendance(modelName.replace(".h5", ""), int(predictedClass), predictedName)
            else:
                cv2.putText(frame, str(accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Görüntünün ekranda gösterilmesi
        cv2.imshow('Video', frame)

        # Çıkış için 'q' tuşuna basılması
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Her şey tamamlandıktan sonra, video yakalama ve görüntüleme objelerinin serbest bırakılması
    videoCapture.release()
    cv2.destroyAllWindows()
