import os
import io
import requests
from PIL import Image

# SETS
personName = input("Lütfen isminizi giriniz: ")
isUseTrain = input("Train? (y,n): ")
isUseValidation = input("Validation? (y,n): ")
isUseTest = input("Test? (y,n): ")
datasetName = "myset"
countTrainImage = 10
countValidationImage = 10

# PATHS
pathTxt = "C:/Project/Proje-2/face_recognition/txt/"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
URLsTrain = pathTxt + "URLsTrain.txt"
URLsValidation = pathTxt + "URLsValidation.txt"
URLsTest = pathTxt + "URLsTest.txt"
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
        failedUrls = []
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
                failedUrls.append(i + 1)
        if len(failedUrls) > 0:
            print("Toplam " + str(
                len(failedUrls)) + " adet URL'den resim indirilemedi. İnen görseller silinecektir. \nAşağıda verilen satır numaralarında bulunan url'Leri değiştirin: \nDosya : " + URLs)
            print(failedUrls)
            for i in range(1, count + 1):
                if i not in failedUrls:
                    filePath = folder + "/" + name + "_" + str(i) + ".jpg"
                    if not os.path.exists(filePath):
                        break
                    os.remove(filePath)
        else:
            print("Tüm resimler başarıyla indirildi.")
    else:
        print("Dosyadaki satır sayısı (" + len(urls) + ")," + count + " sayısı kadar olmalıdır.")


# Eğitim seti için
if isUseTrain.__eq__("y") | isUseTrain.__eq__("Y"):
    downloadImages(URLsTrain, personName, countTrainImage, folderNameFolderInTrain)

# Doğrulama seti için
if isUseValidation.__eq__("y") | isUseValidation.__eq__("Y"):
    downloadImages(URLsValidation, personName, countValidationImage, folderNameFolderInValidation)

# Test seti için
if isUseTest.__eq__("y") | isUseTest.__eq__("Y"):
    downloadImages(URLsTest, personName, 1, folderNameFolderInTest)
