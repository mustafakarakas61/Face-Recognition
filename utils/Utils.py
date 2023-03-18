import glob
import os
import shutil
import string
import random

from Environments import pathControlFolder


def useEnviron():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def changeNameToASCII(name):
    return name.translate(str.maketrans("ğüşöçĞÜŞÖÇıİ", "gusocGUSOCii"))


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


def controlFilesNumbers(sourceFolder):
    deleteJpgFilesOnFolder(pathControlFolder)
    switchFiles(sourceFolder, pathControlFolder)
    for file in os.listdir(pathControlFolder):
        file_list = getJpgFileList(sourceFolder)
        lenFileList = len(file_list)

        oldPath = pathControlFolder + file
        newPath = sourceFolder + "/" + file.split("_")[0] + "_" + str(lenFileList + 1) + ".jpg"
        os.rename(oldPath, newPath)


def deleteJpgFilesOnFolder(sourceFolder):
    for file_name in os.listdir(sourceFolder):
        if file_name.endswith(".jpg"):
            os.remove(os.path.join(sourceFolder, file_name))


def checkURLsDublicates(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines) == len(set(lines)):
            return True
        else:
            return False


def checkFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def getFolderList(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    print(folders)


def getJpgFileList(folder):
    jpgFiles = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(".jpg"):
                jpgFiles.append(os.path.join(folder, file))
    return jpgFiles


def getFileList(path, extension):
    fileList = glob.glob(os.path.join(path, '*' + extension))
    print("Mevcut dosyalar:")
    for filePath in fileList:
        fileName = os.path.basename(filePath)
        print(fileName)


def randomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def randomInt(length):
    return int(''.join(str(random.randint(0, 9)) for _ in range(length)))
