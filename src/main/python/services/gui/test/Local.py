import pickle
import cv2
import numpy as np
from keras.models import load_model
from keras.api.keras.preprocessing import image
from src.resources.Environments import pathModels, pathFaceCascade, inputSize, pathFaceResultsMap, minFaceSize
from utils.Utils import useEnviron, changeNameToASCII

useEnviron()
faceCascade = cv2.CascadeClassifier(pathFaceCascade)
size = inputSize


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
