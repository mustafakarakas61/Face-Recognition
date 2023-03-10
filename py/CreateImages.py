import cv2
import os
import time

from py.ExtractFaces import extractFace
from utils.Utils import randomInt

# SETS
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")
datasetName = "myset"
countTrainImage = 10
countValidationImage = 10

# PATHS
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y") | isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    personName = input("Lütfen isminizi giriniz: ")
    folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
    if not os.path.exists(folderNameFolderInTrain):
        os.makedirs(folderNameFolderInTrain)
    folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
    if not os.path.exists(folderNameFolderInValidation):
        os.makedirs(folderNameFolderInValidation)
folderNameFolderInTest = pathDatasets + datasetName + "/test/"
if not os.path.exists(folderNameFolderInTest):
    os.makedirs(folderNameFolderInTest)


# Generate Images
def createImages(type, name, count, folder, status):
    asciiFolder = folder.translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii"))
    asciiName = name.translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii"))
    os.rename(folder, asciiFolder)

    # Kamera başlatma
    camera = cv2.VideoCapture(0)

    print(type + " için lütfen kameranın açık olduğundan emin olun ve 3 saniye içinde kameraya bakın.")
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
            cv2.imshow("Kameraya bakın ve 1 saniye bekleyin. " + str(count - i) + ". resim.", fileName)

            if status:
                filePath = asciiFolder + "/" + asciiName + ".jpg"
            else:
                filePath = asciiFolder + "/" + asciiName + "_" + str(i + 1) + ".jpg"

            cv2.imwrite(filePath, fileName)
            i += 1
            time.sleep(1)

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
    extractFace(personName, folderNameFolderInTrain)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    createImages("Validation", personName, countValidationImage, folderNameFolderInValidation, False)
    extractFace(personName, folderNameFolderInValidation)

# Test için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    createImages("Test", "test_" + str(randomInt(6)), 1, folderNameFolderInTest, True)
