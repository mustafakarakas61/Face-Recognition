import os

import cv2
import numpy as np
import pickle
import tensorflow as tf
from keras.api.keras.preprocessing import image
from keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pathModels = "C:/Project/Proje-2/face_recognition/models/"
modelName = "myset_17_30_64_yab.h5"
successRate = 91

# Eğitimde kullanılan yüz isimleri ve kodları
with open("C:/Project/Proje-2/face_recognition/ResultsMap.pkl", 'rb') as fileReadStream:
    ResultMap = pickle.load(fileReadStream)

# Eğitilen modelin yüklenmesi
model = load_model(pathModels + modelName)

# Yüz tanıma için kullanılacak sınıflandırıcı
faceCascade = cv2.CascadeClassifier("C:/Project/Proje-2/face_recognition/haarcascade_frontalface_default.xml")

# Webcam'den görüntü almak için kullanılacak obje
videoCapture = cv2.VideoCapture(0)

print("Başarı oranı %" + str(successRate) + " olarak belirlenmiştir. Başarı oranı altındaki yüzler gösterilmeyecektir.")
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
        minSize=(30, 30)
    )

    # Görüntü üzerinde tespit edilen yüzlerin tahmin edilmesi
    for (x, y, w, h) in faces:
        # Yüz bölgesinin kesilmesi ve boyutlandırılması
        face_image = frame[y:y + h, x:x + w]
        face_image = cv2.resize(face_image, (64, 64))
        face_image = image.img_to_array(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        face_image /= 255

        # Yüz tahmini
        prediction = model.predict(face_image, verbose=0)
        predicted_class = np.argmax(prediction)
        predicted_name = ResultMap[predicted_class]
        accuracy = round(np.max(prediction)*100, 2)

        if accuracy > successRate:
            # Tahmin sonucunun ekrana yazdırılması
            cv2.putText(frame, predicted_name.translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii")) + " " + str(
                            accuracy) + "%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
