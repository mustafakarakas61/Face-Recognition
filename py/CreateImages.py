import cv2
import os
import time

# SETS
personName = input("Lütfen isminizi giriniz: ")
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")
datasetName = "myset"
countTrainImage = 10
countValidationImage = 10

# PATHS
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
folderNameFolderInTest = pathDatasets + datasetName + "/test"


# Generate Images
def createImages(name, count, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Kamera başlatma
    camera = cv2.VideoCapture(0)

    print("Lütfen kameranın açık olduğundan emin olun ve 3 saniye içinde kameraya bakın.")
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
            filePath = folder + "/" + name + "_" + str(i + 1) + ".jpg"
            cv2.imwrite(filePath, fileName)
            i += 1
            time.sleep(1)

    camera.release()
    cv2.destroyAllWindows()


# Eğitim seti için
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    createImages(personName, countTrainImage, folderNameFolderInTrain)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    createImages(personName, countValidationImage, folderNameFolderInValidation)

# Test için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    createImages(personName, 1, folderNameFolderInTest)
