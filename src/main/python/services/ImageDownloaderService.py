import os
import re

import cv2
import numpy as np
import urllib.request

# Resim URL'si
import requests

from src.resources.Environments import pathTrain, pathFaceCascade, personName
from utils.Utils import checkFolder, getJpgFileList, checkJpgFileOfTheHaveNumber, changeNameToASCII, switchFiles, \
    controlFilesNumbers

inputName = personName


def downloadImageFaceJson(name, url):
    isThereTurkishChar = False
    try:
        originalFolder = pathTrain + name
        controlFilesNumbers(originalFolder)
        checkFolder(originalFolder)
        if re.search("[ıİğĞüÜşŞöÖçÇ]", name):
            isThereTurkishChar = True

        if isThereTurkishChar:
            asciiName = changeNameToASCII(name)
            asciiFolder = pathTrain + asciiName
            checkFolder(asciiFolder)
            switchFiles(originalFolder, asciiFolder)

        # Resmi indirin ve Numpy dizisine dönüştürün
        response = requests.get(url)
        arr = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        # Yüz algılama sınıflandırıcısını yükleyin
        face_cascade = cv2.CascadeClassifier(pathFaceCascade)

        # Gri tonlamalı görüntü elde edin
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Yüzleri algıla
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # En az bir yüz algılandıysa resmi kaydedin
        if len(faces) > 0:
            # İlk yüzü seçin ve kırpın
            (x, y, w, h) = faces[0]
            crop_img = img[y:y + h, x:x + w]

            if isThereTurkishChar:
                file_list = getJpgFileList(asciiFolder)
                filename = asciiName + "_" + str(len(file_list) + 1) + ".jpg"
                filename = checkJpgFileOfTheHaveNumber(asciiFolder, filename)
                outputPath = asciiFolder + "/" + filename
            else:
                file_list = getJpgFileList(originalFolder)
                filename = name + "_" + str(len(file_list) + 1) + ".jpg"
                filename = checkJpgFileOfTheHaveNumber(originalFolder, filename)
                outputPath = originalFolder + "/" + filename

            crop_img = cv2.resize(crop_img, (512, 512))
            cv2.imwrite(outputPath, crop_img)
            if isThereTurkishChar:
                print("Yüz tespit edildi, " + str(filename).replace(asciiName,
                                                                    name) + " olarak kaydedildi. Toplam Resim : " + str(
                    len(file_list) + 1))
            else:
                print("Yüz tespit edildi, " + str(filename) + " olarak kaydedildi. Toplam Resim : " + str(
                    len(file_list) + 1))
        else:
            print("Yüz tespit edilemedi.")

        if isThereTurkishChar:
            for i, file in enumerate(os.listdir(asciiFolder)):
                os.rename(os.path.join(asciiFolder, file),
                          os.path.join(asciiFolder, name + "_" + file.split("_")[1]))

            switchFiles(asciiFolder, originalFolder)
            os.rmdir(asciiFolder)

        return True
    except Exception as e:
        print("Error ", e)
        if isThereTurkishChar:
            for i, file in enumerate(os.listdir(asciiFolder)):
                os.rename(os.path.join(asciiFolder, file),
                          os.path.join(asciiFolder, name + "_" + file.split("_")[1]))

            switchFiles(asciiFolder, originalFolder)
            os.rmdir(asciiFolder)


def downloadImageFaceString(url):
    isThereTurkishChar = False
    try:
        originalFolder = pathTrain + inputName
        controlFilesNumbers(originalFolder)
        checkFolder(originalFolder)
        if re.search("[ıİğĞüÜşŞöÖçÇ]", inputName):
            isThereTurkishChar = True

        if isThereTurkishChar:
            asciiName = changeNameToASCII(inputName)
            asciiFolder = pathTrain + asciiName
            checkFolder(asciiFolder)
            switchFiles(originalFolder, asciiFolder)

        # Resmi indirin ve Numpy dizisine dönüştürün
        response = requests.get(url)
        arr = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        # Yüz algılama sınıflandırıcısını yükleyin
        face_cascade = cv2.CascadeClassifier(pathFaceCascade)

        # Gri tonlamalı görüntü elde edin
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Yüzleri algıla
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # En az bir yüz algılandıysa resmi kaydedin
        if len(faces) > 0:
            # İlk yüzü seçin ve kırpın
            (x, y, w, h) = faces[0]
            crop_img = img[y:y + h, x:x + w]

            if isThereTurkishChar:
                file_list = getJpgFileList(asciiFolder)
                filename = asciiName + "_" + str(len(file_list) + 1) + ".jpg"
                filename = checkJpgFileOfTheHaveNumber(asciiFolder, filename)
                outputPath = asciiFolder + "/" + filename
            else:
                file_list = getJpgFileList(originalFolder)
                filename = inputName + "_" + str(len(file_list) + 1) + ".jpg"
                filename = checkJpgFileOfTheHaveNumber(originalFolder, filename)
                outputPath = originalFolder + "/" + filename

            crop_img = cv2.resize(crop_img, (512, 512))
            cv2.imwrite(outputPath, crop_img)
            if isThereTurkishChar:
                print("Yüz tespit edildi, " + str(filename).replace(asciiName,
                                                                    inputName) + " olarak kaydedildi. Toplam Resim : " + str(
                    len(file_list) + 1))
            else:
                print("Yüz tespit edildi, " + str(filename) + " olarak kaydedildi. Toplam Resim : " + str(
                    len(file_list) + 1))
        else:
            print("Yüz tespit edilemedi.")

        if isThereTurkishChar:
            for i, file in enumerate(os.listdir(asciiFolder)):
                os.rename(os.path.join(asciiFolder, file),
                          os.path.join(asciiFolder, inputName + "_" + file.split("_")[1]))

            switchFiles(asciiFolder, originalFolder)
            os.rmdir(asciiFolder)

        return True
    except Exception as e:
        print(e)
        if isThereTurkishChar:
            for i, file in enumerate(os.listdir(asciiFolder)):
                os.rename(os.path.join(asciiFolder, file),
                          os.path.join(asciiFolder, inputName + "_" + file.split("_")[1]))

            switchFiles(asciiFolder, originalFolder)
            os.rmdir(asciiFolder)
