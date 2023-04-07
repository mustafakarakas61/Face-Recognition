import datetime

import cv2
import os
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.resources.Environments import pngCamera
from utils.Utils import checkFolder, changeNameToASCII


class Camera(QWidget):
    def __init__(self, mainWidget):
        super(Camera, self).__init__()
        self.mainWidget = mainWidget

    def faceAddVideoCameraScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Kameradan Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngCamera))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.mainWidget.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()


# inputs
# isUseTrain = input("Train? (y,n): ")
# isUseValidation = input("Validation? (y,n): ")
# isUseTest = input("Test? (y,n): ")
#
# if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y") | isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
#     getFolderList(pathTrain)
#     personName = input("Lütfen bir isim girin ya da bir isim seçin: ")
#     videoPath = input("Lütfen video path'i giriniz: ")
#
#     folderNameFolderInTrain = pathTrain + personName
#     checkFolder(folderNameFolderInTrain)
#
#     folderNameFolderInValidation = pathValidation + personName
#     checkFolder(folderNameFolderInValidation)
#
# folderNameFolderInTest = pathTest
# checkFolder(folderNameFolderInTest)


# TODO : VİDEOYA DÖNÜŞTÜRÜELECEK ve asciiler yeniden kontrol ettiirelecek
def createVideo(type, name, duration, folder):
    checkFolder(folder)
    asciiFolder = changeNameToASCII(folder)
    asciiName = changeNameToASCII(name)
    if not os.path.exists(asciiFolder):
        os.rename(folder, asciiFolder)

    # Kamera başlatma
    camera = cv2.VideoCapture(0)
    fps = camera.get(cv2.CAP_PROP_FPS)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(type + " için " + str(
        duration) + " saniye boyunca video kaydedilecektir. Lütfen kameranın açık olduğundan emin olun ve kayıt başlamadan önce 3 saniye bekleyin.")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=duration)
    output_path = os.path.join(asciiFolder, asciiName + ".mp4")
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while datetime.datetime.now() < end_time:
        ret, frame = camera.read()
        if ret:
            out.write(frame)

    camera.release()
    out.release()
    cv2.destroyAllWindows()


# Eğitim seti için
# if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
#     createVideo("Train", personName, durationVideo, folderNameFolderInTrain)
#     extractFaces(personName, folderNameFolderInTrain)

# Doğrulama seti için
# if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
#     createVideo("Validation", personName, durationVideo, folderNameFolderInValidation)
#     extractFaces(personName, folderNameFolderInValidation)
#
# # Test için
# if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
#     createVideo("Test", "test_" + str(randomInt(6)), countTestImage, folderNameFolderInTest)
