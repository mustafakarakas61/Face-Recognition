import cv2
import os
import numpy as np
from keras.models import load_model
from keras.api.keras.preprocessing import image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pathModels = "C:/Project/Proje-2/face_recognition/models/"

successRate = 60  # % cinsinden
size = 64
modelName = "myset_16_30_64_nkh.h5"

model = load_model(pathModels + modelName)

testImagePath = "C:/Project/Proje-2/face_recognition/datasets/myset/test/test_448650.jpg"
faceCascade = cv2.CascadeClassifier("C:/Project/Proje-2/face_recognition/haarcascade_frontalface_default.xml")

testImage = cv2.imread(testImagePath)
gray = cv2.cvtColor(testImage, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

datasetName = "myset"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
trainSource = pathDatasets + datasetName + "/train"

trainDatagen = image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

trainGenerator = trainDatagen.flow_from_directory(
    trainSource,
    target_size=(size, size),
    batch_size=32,
    class_mode='categorical'
)

ResultMap = {}
results = []
for faceValue, faceName in zip(trainGenerator.class_indices.values(), trainGenerator.class_indices.keys()):
    ResultMap[faceValue] = faceName
    # print(str(faceValue) + " : " + faceName)

if len(faces) == 0:
    print("Yüz bulunamadı.")
else:
    for (x, y, w, h) in faces:
        faceImage = testImage[y:y + h, x:x + w]
        faceImage = cv2.resize(faceImage, (size, size))
        faceImage = faceImage / 255.0
        faceImage = np.expand_dims(faceImage, axis=0)
        result = model.predict(faceImage)

        label = np.argmax(result)
        confidence = round(result[0][label] * 100, 2)
    if confidence > successRate:
        cv2.rectangle(testImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(testImage,
                    ResultMap[label].translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii")) + " " + str(
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
        print("Başarı oranı (%" + str(successRate) + ") altında olan isim ve yüzdesi:\n" + ResultMap[label].translate(
            str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii")) + " " + str(
            confidence) + "%")
