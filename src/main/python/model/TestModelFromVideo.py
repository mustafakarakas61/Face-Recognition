import pickle
import cv2
import numpy as np
from keras.models import load_model

from src.resources.Environments import pathModels, pathFaceCascade, inputSize, successRate, pathFaceResultsMap, \
    minTestFaceSize
from utils.Utils import useEnviron, changeNameToASCII

useEnviron()

faceCascade = cv2.CascadeClassifier(pathFaceCascade)

# input
size = inputSize


# getFileList(pathModels, ".h5")
# modelName = input("Kullanılacak model ismini giriniz:")

def findFacesFromVideo(videoPath, modelName):
    model = load_model(pathModels + modelName)

    videoCapture = cv2.VideoCapture(videoPath)

    while True:
        ret, frame = videoCapture.read()

        if not ret:
            print("Video bitti. Çıkış için bir tuşa basınız...")
            cv2.waitKey(0)
            videoCapture.release()
            cv2.destroyAllWindows()
            print("Video Kapatıldı!\n")
            break
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                 minSize=(minTestFaceSize, minTestFaceSize))

            results = []
            with open(pathFaceResultsMap + modelName.replace(".h5", ".pkl"), 'rb') as fileReadStream:
                ResultMap = pickle.load(fileReadStream)

            # if len(faces) == 0:
            #     print("Yüz bulunamadı.")
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    face_image = gray[y:y + h, x:x + w]

                    # face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)  # girdi 1 boyutlu ise
                    resized_image = cv2.resize(face_image, (size, size))
                    input_image = np.expand_dims(resized_image, axis=0)
                    input_image = input_image / 255.0
                    result = model.predict(input_image)

                    label = np.argmax(result)
                    confidence = round(result[0][label] * 100, 2)

                if confidence > successRate:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame,
                                changeNameToASCII(ResultMap[label]) + " " + str(
                                    confidence) + "%",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                    cv2.imshow("Video", frame)

                    # results = sorted(result[0], reverse=True)
                    # for i, confidence in enumerate(results[:3]):
                    #     index = np.where(result[0] == confidence)[0][0]
                    #     name = ResultMap[index]
                    #     print(f"{i + 1}. {name} : {confidence * 100:.2f}%")

                # else:
                #     print("Başarı oranı (%" + str(successRate) + ") altında olan isim ve yüzdesi:\n" + changeNameToASCII(
                #         ResultMap[label]) + " " + str(
                #         confidence) + "%")

                # Çıkış için klavye tuşuna bas
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    videoCapture.release()
                    cv2.destroyAllWindows()
                    print("Video Kapatıldı!\n")
                    break
