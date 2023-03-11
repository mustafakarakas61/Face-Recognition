import os
import io
import shutil
import requests
from PIL import Image

from py.ExtractFaces import extractFaces
from utils.Utils import randomInt, getFolderList, checkURLsDublicates

# SETS
countTrainImage = 30
countValidationImage = 10
countTestImage = 1
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")
datasetName = "myset"

# PATHS
pathTxt = "C:/Project/Proje-2/face_recognition/txt/"
pathSuccess = pathTxt + "success/"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
URLsTrain = pathTxt + "URLsTrain.txt"
URLsValidation = pathTxt + "URLsValidation.txt"
URLsTest = pathTxt + "URLsTest.txt"

if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y") | isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    getFolderList("C:/Project/Proje-2/face_recognition/datasets/myset/train")
    personName = input("Lütfen bir isim girin ya da bir isim seçin: ")
    folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + personName
    if not os.path.exists(folderNameFolderInTrain):
        os.makedirs(folderNameFolderInTrain)
    folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + personName
    if not os.path.exists(folderNameFolderInValidation):
        os.makedirs(folderNameFolderInValidation)
folderNameFolderInTest = pathDatasets + datasetName + "/test/"


# Download Images
def downloadImages(type, URLs, name, count, folder, status):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if checkURLsDublicates(URLs):
        # URLs
        with open(URLs) as f:
            urls = f.readlines()

        # Dosyadaki satır sayısını kontrol edelim
        if len(urls) == count:
            failedUrls = []
            print(type + " için indirme başlatılıyor:")
            for i, url in enumerate(urls):
                try:
                    if status:
                        filePath = folder + "/test_" + str(randomInt(6)) + ".jpg"
                    else:
                        filePath = folder + "/" + name + "_" + str(i + 1) + ".jpg"
                    filePath = filePath.replace("//", "/")
                    response = requests.get(url.strip())

                    img = Image.open(io.BytesIO(response.content))
                    # img = img.resize((640, 480))
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
                print([str(i) for i in failedUrls])
                print("\n")
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
                    print("Tüm " + type + " resimler başarıyla indirildi.\n")

                folderSuccessText = pathSuccess + name + "/"
                if not os.path.exists(folderSuccessText):
                    os.makedirs(folderSuccessText)
                successURLsFileName = folderSuccessText + name + "_" + type + "_" + str(count) + ".txt"
                shutil.move(URLs, successURLsFileName)
                open(URLs, 'w').close()
        else:
            print("Hata : " + type + " için " + URLs + " dosyasındaki URL satır sayısı (" + str(len(urls)) + ")," + str(
                count) + " sayısı kadar olmalıdır.")
    else:
        print("Hata : " + URLs + " dosyasında tekrarlayan URL adresleri mevcut.")
        urls = set()
        duplicates = []
        with open(URLs) as f:
            for line in f:
                if line.strip() in urls:
                    duplicates.append(line.strip())
                else:
                    urls.add(line.strip())
        if duplicates:
            print("Tekrar eden URL adresleri:")
            for url in duplicates:
                print(url)
            print("\n")


# Eğitim seti için
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    downloadImages("Train", URLsTrain, personName, countTrainImage, folderNameFolderInTrain, False)
    extractFaces(personName, folderNameFolderInTrain)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    downloadImages("Validation", URLsValidation, personName, countValidationImage, folderNameFolderInValidation, False)
    extractFaces(personName, folderNameFolderInValidation)

# Test seti için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    downloadImages("Test", URLsTest, personName, countTestImage, folderNameFolderInTest, True)
