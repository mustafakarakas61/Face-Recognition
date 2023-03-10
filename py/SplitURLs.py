# SETS
countTrainImage = 15
countValidationImage = 5
countTestImage = 1


def splitURLsToTxt(countTrain, countValidation, countTest):
    pathTxt = "C:/Project/Proje-2/face_recognition/txt/"
    urlsFile = pathTxt + "URLs.txt"
    urlsTrainFile = pathTxt + "URLsTrain.txt"
    urlsValidationFile = pathTxt + "URLsValidation.txt"
    urlsTestFile = pathTxt + "URLsTest.txt"

    # Open URLs.txt file
    with open(urlsFile, "r") as file:
        urls = file.readlines()

        if (countTrain + countValidation + countTest) == len(urls):
            # Clear other txt files
            with open(urlsTrainFile, "w") as fileTrain:
                fileTrain.write("")
            with open(urlsValidationFile, "w") as fileValidation:
                fileValidation.write("")
            with open(urlsTestFile, "w") as fileTest:
                fileTest.write("")

            # Write first urls to URLsTrain.txt
            with open(urlsTrainFile, "a") as fileTrain:
                fileTrain.writelines(urls[:countTrain])

            # Write next urls to URLsValidation.txt
            with open(urlsValidationFile, "a") as fileValidation:
                fileValidation.writelines(urls[countTrain:(countTrain + countValidation)])

            # Write the last url to URLsTest.txt
            with open(urlsTestFile, "a") as fileTest:
                fileTest.writelines(urls[(countTrain + countValidation):(
                        countTrain + countValidation + countTest)])

            # Clear URLs.txt file
            with open(urlsFile, "w") as fileUrl:
                fileUrl.write("")
            print("URL'ler paylaştırıldı.")
        else:
            print("Lütfen gerektiği kadar url linki yapıştırınız. \nToplam URL sayısı : " + str(len(
                urls)) + ", Gereken toplam sayı : " + str((
                    countTrain + countValidation + countTest)) + "\nTrain için : " + str(
                countTrain) + ", Validation için : " + str(countValidation) + ", Test için : " + str(countTest))


splitURLsToTxt(countTrainImage, countValidationImage, countTestImage)
