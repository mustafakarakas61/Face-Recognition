import pickle
import cv2
import numpy as np
from keras.models import load_model

from Environments import pathModels, pathFaceCascade, inputSize, successRate, pathTest, pathResultsMap, minFaceSize, \
    minTestFaceSize
from utils.Utils import useEnviron, getFileList, changeNameToASCII

useEnviron()

faceCascade = cv2.CascadeClassifier(pathFaceCascade)

# input
size = inputSize

getFileList(pathModels, ".h5")
# modelName = input("Kullanılacak model ismini giriniz:")
modelName = "myset_10_30_128_ryc.h5"

model = load_model(pathModels + modelName)

# getFileList(pathTest, ".jpg")
# testImagePath = input("Kullanılacak test resmini seçiniz:")
testImagePath = pathTest + "test_6161.jpg"

testImage = cv2.imread(testImagePath)
gray = cv2.cvtColor(testImage, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(minTestFaceSize, minTestFaceSize))

results = []
# Eğitimde kullanılan yüz isimleri ve kodları
with open(pathResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as fileReadStream:
    ResultMap = pickle.load(fileReadStream)

if len(faces) == 0:
    print("Yüz bulunamadı.")
else:
    for (x, y, w, h) in faces:
        faceImage = testImage[y:y + h, x:x + w]
        faceImage = cv2.cvtColor(faceImage, cv2.COLOR_BGR2GRAY) #1
        faceImage = cv2.resize(faceImage, (size, size))
        faceImage = faceImage / 255.0
        faceImage = np.expand_dims(faceImage, axis=0)
        result = model.predict(faceImage)

        label = np.argmax(result)
        confidence = round(result[0][label] * 100, 2)
    if confidence > successRate:
        cv2.rectangle(testImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(testImage,
                    changeNameToASCII(ResultMap[label]) + " " + str(
                        confidence) + "%",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow("Test Image", testImage)
        cv2.waitKey(0)

        results = sorted(result[0], reverse=True)
        for i, confidence in enumerate(results[:3]):
            index = np.where(result[0] == confidence)[0][0]
            name = ResultMap[index]
            print(f"{i + 1}. {name} : {confidence * 100:.2f}%")

    else:
        print("Başarı oranı (%" + str(successRate) + ") altında olan isim ve yüzdesi:\n" + changeNameToASCII(
            ResultMap[label]) + " " + str(
            confidence) + "%")
