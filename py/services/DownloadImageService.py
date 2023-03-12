import os
import io

import requests
from PIL import Image

from py.services.ExtractFaceService import extractFace
from utils.Utils import randomInt


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
