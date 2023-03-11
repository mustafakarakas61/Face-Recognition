import os
import io

import cv2
import requests
from PIL import Image

from utils.Utils import randomInt, switchFile

# PATHS
faceCascade = cv2.CascadeClassifier("C:/Project/Proje-2/face_recognition/haarcascade_frontalface_default.xml")
pathNoFace = "C:/Project/Proje-2/face_recognition/utils/NoFace.txt"


def downloadImage(url, name, folder, isTest):
    if not os.path.exists(folder):
        os.makedirs(folder)

    fileList = os.listdir(folder)
    jpgCount = 0
    for fileName in fileList:
        if fileName.endswith('.jpg'):
            jpgCount += 1

    try:
        if isTest:
            tempName = "test_" + str(randomInt(6)) + ".jpg"
            filePath = folder + "/" + tempName

        else:
            tempName = name + "_" + str(jpgCount + 1) + ".jpg"
            filePath = folder + "/" + tempName
        filePath = filePath.replace("//", "/")
        response = requests.get(url.strip())

        img = Image.open(io.BytesIO(response.content))
        img.save(filePath)

        print(filePath + " indirildi.")
        extractFace(name, folder, tempName)
        print("\n")
    except:
        print(url.strip() + " indirilemedi.")
        print("\n")


def extractFace(name, srcFolder, fileName):
    destFolder = "C:/Project/Proje-2/face_recognition/utils/tempFolder"
    switchFile(srcFolder, destFolder, fileName)

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
                print("Yüz çıkarıldı. " + srcFolder + " konumuna " + fileName + " kaydedildi.")
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

    switchFile(destFolder, srcFolder, fileName)
