import glob
import os
import string
import random


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
