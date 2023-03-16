import os
import cv2

from Environments import pathTempFolder, pathFaceCascade, pathNoFace, minFaceSize
from utils.Utils import switchFiles, changeNameToASCII, switchFile

faceCascade = cv2.CascadeClassifier(pathFaceCascade)


def extractFaces(name, srcFolder):
    destFolder = pathTempFolder

    switchFiles(srcFolder, destFolder)

    for imageName in os.listdir(destFolder):
        asciiName = changeNameToASCII(imageName)
        os.rename(destFolder + "/" + imageName, destFolder + "/" + asciiName)

    for imageName in os.listdir(destFolder):
        if imageName.endswith(".jpg"):
            imagePath = destFolder + "/" + imageName
            img = cv2.imread(imagePath)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                 minSize=(minFaceSize, minFaceSize))

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

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                 minSize=(minFaceSize, minFaceSize))

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
