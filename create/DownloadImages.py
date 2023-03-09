import os
import io
import requests
from PIL import Image

# SETS
personName = input("Lütfen isminizi giriniz: ")
datasetName = "myset"
countTrainImage = 10
countValidationImage = 10

# PATHS
URLsTrain = "C:/Project/Proje-2/face_recognition/create/URLsTrain.txt"
URLsValidation = "C:/Project/Proje-2/face_recognition/create/URLsValidation.txt"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
folderNameFolderInTest = pathDatasets + datasetName + "/test"


# Download Images
def downloadImages(URLs, name, count, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # URLs
    with open(URLs) as f:
        urls = f.readlines()

    # Dosyadaki satır sayısını kontrol edelim
    if len(urls) == count:
        for i, url in enumerate(urls):
            try:
                filePath = folder + "/" + name + "_" + str(i + 1) + ".jpg"

                response = requests.get(url.strip())

                img = Image.open(io.BytesIO(response.content))
                img = img.resize((640, 480))
                img.save(filePath)

                # with open(fileName, "wb") as f:
                #     f.write(response.content)

                print(filePath + " indirildi.")
            except:
                print(url.strip() + " indirilemedi.")
    else:
        print("Dosyadaki satır sayısı (" + len(urls) + ")," + count + " sayısı kadar olmalıdır.")


# Eğitim seti için
downloadImages(URLsTrain, personName, countTrainImage, folderNameFolderInTrain)
