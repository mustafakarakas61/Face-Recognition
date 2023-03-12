import cv2
import os
import time

from Environments import pathTrain, pathValidation, pathTest, countTrainImage, countValidationImage, countTestImage
from py.services.ExtractFaceService import extractFaces
from utils.Utils import randomInt, checkFolder, getFolderList, changeNameToASCII

# inputs
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")

if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y") | isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    getFolderList(pathTrain)
    personName = input("Lütfen bir isim girin ya da bir isim seçin: ")

    folderNameFolderInTrain = pathTrain + personName
    checkFolder(folderNameFolderInTrain)

    folderNameFolderInValidation = pathValidation + personName
    checkFolder(folderNameFolderInValidation)

folderNameFolderInTest = pathTest
checkFolder(folderNameFolderInTest)


def createImages(type, name, count, folder, status):
    asciiFolder = changeNameToASCII(folder)
    asciiName = changeNameToASCII(name)
    os.rename(folder, asciiFolder)

    # Kamera başlatma
    camera = cv2.VideoCapture(0)

    print(
        type + " için " + count + " adet resim çekilecektir. Lütfen kameranın açık olduğundan emin olun ve 3 saniye içinde kameraya bakın.")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    i = 0
    while i < count:
        ret, fileName = camera.read()

        if ret:
            cv2.imshow("Kameraya bakın ve 2 saniye bekleyin. " + str(count - i) + ". resim.", fileName)
            if status:
                filePath = asciiFolder + "/" + asciiName + ".jpg"
            else:
                filePath = asciiFolder + "/" + asciiName + "_" + str(i + 1) + ".jpg"

            cv2.imwrite(filePath, fileName)
            if not status:
                print(name + "_" + str(i + 1) + ".jpg")
            i += 1
            time.sleep(2)

    camera.release()
    cv2.destroyAllWindows()

    # Resim ve klasör adlarını değiştirme
    if not name.__eq__(asciiName):
        os.rename(asciiFolder, folder)
        for i, file in enumerate(os.listdir(folder)):
            os.rename(os.path.join(folder, file),
                      os.path.join(folder, name + "_" + file.split("_")[1]))


# Eğitim seti için
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    createImages("Train", personName, countTrainImage, folderNameFolderInTrain, False)
    extractFaces(personName, folderNameFolderInTrain)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    createImages("Validation", personName, countValidationImage, folderNameFolderInValidation, False)
    extractFaces(personName, folderNameFolderInValidation)

# Test için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    createImages("Test", "test_" + str(randomInt(6)), countTestImage, folderNameFolderInTest, True)
