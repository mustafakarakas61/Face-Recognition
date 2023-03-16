import os
import cv2

from Environments import pathTempFolder, pathFaceCascade, pathNoFace
from utils.Utils import switchFiles, changeNameToASCII, switchFile, getFileList, getJpgFileList

faceCascade = cv2.CascadeClassifier(pathFaceCascade)


# todo : SADECE İSTENİLEN ARALIKTAKİ HER SANİYEDE VİDEODAN O ANKİ RESMİ KAYDETSİN İSTENİLEN SAYIYA ULAŞANA KADAR.
# todo : SONRASINDA RESİMLERDEN YÜZ ETME OLAYINA DÖNÜŞTÜRÜLÜR
def extractFacesFromVideo(mp4Video, count, name, folder):
    # video dosyasını okuyun
    cap = cv2.VideoCapture(mp4Video)
    skip_frames = 5  # 10 kareyi atlayın
    for i in range(skip_frames):  # İlk 10 kareyi atlayın
        cap.read()

    # her kare için yüzleri tespit edin ve ilgili konuma aktarın
    frameCount = 0
    imageCount = 0
    while True:
        # her kareyi okuyun
        ret, frame = cap.read()
        if not ret:
            break

        # yüzleri tespit etmek için gri tonlamalı görüntü oluşturun
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # yüzleri tespit edin
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        # her yüz için ilgili konuma aktarın ve kareyi gösterin
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # her 10 kare için bir resim kaydedin
        if frameCount % skip_frames == 0 and len(faces) == 1:
            file_list = getJpgFileList(folder)
            filename = f'{name}_{str(len(file_list) + 1)}.jpg'

            outputPath = folder + "/" + filename
            cv2.imwrite(outputPath, frame)
            print(outputPath + " kaydedildi.")
            imageCount += 1
        if imageCount == count:
            break
        frameCount += 1

    cap.release()
    cv2.destroyAllWindows()


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
