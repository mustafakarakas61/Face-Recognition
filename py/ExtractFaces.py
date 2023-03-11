import os
import shutil

import cv2

from utils.Utils import getFolderList, switchFiles

faceCascade = cv2.CascadeClassifier("C:/Project/Proje-2/face_recognition/haarcascade_frontalface_default.xml")

# SETS
datasetName = "myset"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"

isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")

if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y") | isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    getFolderList("C:/Project/Proje-2/face_recognition/datasets/myset/train")
    personName = input("Lütfen bir isim girin ya da bir isim seçin: ")
    folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
    if not os.path.exists(folderNameFolderInTrain):
        os.makedirs(folderNameFolderInTrain)
    folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
    if not os.path.exists(folderNameFolderInValidation):
        os.makedirs(folderNameFolderInValidation)
folderNameFolderInTest = pathDatasets + datasetName + "/test/"
pathNoFace = "C:/Project/Proje-2/face_recognition/utils/NoFace.txt"


def extractFaces(name, srcFolder):
    destFolder = "C:/Project/Proje-2/face_recognition/utils/tempFolder"

    switchFiles(srcFolder, destFolder)

    for imageName in os.listdir(destFolder):
        asciiName = imageName.translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii"))
        os.rename(destFolder + "/" + imageName, destFolder + "/" + asciiName)

    for imageName in os.listdir(destFolder):
        if imageName.endswith(".jpg"):
            imagePath = destFolder + "/" + imageName
            img = cv2.imread(imagePath)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Yüzleri çıkar
                for i, (x, y, w, h) in enumerate(faces):
                    faceCrop = img[y:y + h, x:x + w]

                    # Yüzü kaydet
                    outputName = imageName
                    outputPath = destFolder + "/" + outputName
                    cv2.imwrite(outputPath, faceCrop)

                    # Yüzleri göster
                    # cv2.imshow("Face " + str(i), faceCrop)
            else:
                # Yüz bulunamadı
                print("Yüz bulunamadı: " + imageName)
                with open(pathNoFace, "a") as f:
                    f.write(srcFolder + "/" + name + "_" + imageName.split("_")[1] + "\n")

            cv2.waitKey()
            cv2.destroyAllWindows()

    for i, file in enumerate(os.listdir(destFolder)):
        os.rename(os.path.join(destFolder, file),
                  os.path.join(destFolder, name + "_" + file.split("_")[1]))

    switchFiles(destFolder, srcFolder)


if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    extractFaces(personName, folderNameFolderInTrain)

if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    extractFaces(personName, folderNameFolderInValidation)

# image = folderTrain + "test_695151.jpg"

# img = cv2.imread(image)

# Gri tonlamalı resim oluştur
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Yüzleri tespit etmek için yüz tanıma modelini kullan
# faces = faceCascade.detectMultiScale(gray, 1.1, 4)

# Yüzleri çıkar
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#     faceCrop = img[y:y + h, x:x + w]
#     outputName = folderTrain + "c-test_418284_.jpg"
#     cv2.imwrite(outputName, faceCrop)
#     print("Çıktı : " + outputName)
# # Yüzleri göster
# cv2.imshow('img', img)
# cv2.waitKey()
