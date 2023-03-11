import glob
import os
import shutil
import string
import random


def switchFiles(srcFolder, destFolder):
    for item in os.listdir(srcFolder):
        # Dosya veya klasör mü kontrol et
        itemPath = os.path.join(srcFolder, item)
        if os.path.isfile(itemPath):
            if itemPath.endswith(".jpg"):
                shutil.move(itemPath, destFolder)


def switchFile(srcFolder, destFolder, fileName):
    for item in os.listdir(srcFolder):
        # Dosya veya klasör mü kontrol et
        if item.__eq__(fileName):
            itemPath = os.path.join(srcFolder, item)
            if os.path.isfile(itemPath):
                if itemPath.endswith(".jpg"):
                    shutil.move(itemPath, destFolder)


def checkURLsDublicates(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines) == len(set(lines)):
            return True
        else:
            return False


def getFolderList(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    print(folders)


def getFileList(path, extension):
    fileList = glob.glob(os.path.join(path, '*.' + extension))
    print("Mevcut dosyalar:")
    for filePath in fileList:
        fileName = os.path.basename(filePath)
        print(fileName)


def randomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def randomInt(length):
    return int(''.join(str(random.randint(0, 9)) for _ in range(length)))
