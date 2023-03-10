import os
import io
import shutil
import requests
from PIL import Image

from utils.Utils import randomInt, getFolderList

getFolderList("C:/Project/Proje-2/face_recognition/datasets/myset/train")
# SETS
personName = input("Lütfen ismi girin: ")
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")
datasetName = "myset"
countTrainImage = 10
countValidationImage = 10

# PATHS
pathTxt = "C:/Project/Proje-2/face_recognition/txt/"
pathSuccess = pathTxt + "success/"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
URLsTrain = pathTxt + "URLsTrain.txt"
URLsValidation = pathTxt + "URLsValidation.txt"
URLsTest = pathTxt + "URLsTest.txt"
folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
folderNameFolderInTest = pathDatasets + datasetName + "/test/"


# Download Images
def downloadImages(type, URLs, name, count, folder, status):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # URLs
    with open(URLs) as f:
        urls = f.readlines()

    # Dosyadaki satır sayısını kontrol edelim
    if len(urls) == count:
        failedUrls = []
        for i, url in enumerate(urls):
            try:
                if status:
                    filePath = folder + "/test_" + str(randomInt(6)) + ".jpg"
                else:
                    filePath = folder + "/" + name + "_" + str(i + 1) + ".jpg"
                filePath = filePath.replace("//", "/")
                response = requests.get(url.strip())

                img = Image.open(io.BytesIO(response.content))
                img = img.resize((640, 480))
                img.save(filePath)

                # with open(fileName, "wb") as f:
                #     f.write(response.content)

                print(filePath + " indirildi.")
            except:
                print(url.strip() + " indirilemedi.")
                failedUrls.append(i + 1)
        if len(failedUrls) > 0:
            print("Toplam " + str(
                str(len(
                    failedUrls))) + " adet URL'den resim indirilemedi. İnen görseller silinecektir. \nAşağıda verilen satır numaralarında bulunan url'Leri değiştirin: \nDosya : " + URLs)
            print(failedUrls)
            for i in range(1, count + 1):
                if i not in failedUrls:
                    if status:
                        filePath = folder + "/test_" + str(randomInt(6)) + ".jpg"
                    else:
                        filePath = folder + "/" + name + "_" + str(i) + ".jpg"
                    if not os.path.exists(filePath):
                        break
                    os.remove(filePath)
        else:
            if status:
                print("Test resmi başarıyla indirildi.\n")
            else:
                print("Tüm resimler başarıyla indirildi.\n")
            successURLsFileName = pathSuccess + name + "_" + type + "_" + str(count) + ".txt"
            shutil.move(URLs, successURLsFileName)
            open(URLs, 'w').close()
    else:
        print("Dosyadaki satır sayısı (" + str(len(urls)) + ")," + str(count) + " sayısı kadar olmalıdır.")


# Eğitim seti için
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    downloadImages("train", URLsTrain, personName, countTrainImage, folderNameFolderInTrain, False)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    downloadImages("validation", URLsValidation, personName, countValidationImage, folderNameFolderInValidation, False)

# Test seti için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    downloadImages("test", URLsTest, personName, 1, folderNameFolderInTest, True)
