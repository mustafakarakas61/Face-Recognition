import os
import numpy as np
from keras.models import load_model
from keras.api.keras.preprocessing import image

from utils.Utils import getFileList

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

size = 150

# PATHS
datasetName = "myset"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
pathModels = "C:/Project/Proje-2/face_recognition/models/"
trainSource = pathDatasets + datasetName + "/train"
pathTestImage = pathDatasets + datasetName + "/test/"

# input 1
getFileList(pathModels, "h5")
modelName = input("Lütfen kullanılacak modeli seçiniz: ")

# input 2
getFileList(pathTestImage, "jpg")
# testImageName = input("Lütfen test için bir resim ismi giriniz: ")
testImageName = "test_532741.jpg"
print("Meral Akşener")

testModel = load_model(pathModels + modelName)
testImage = image.load_img(pathTestImage + testImageName, target_size=(size, size))
testImage = image.img_to_array(testImage)
testImage = np.expand_dims(testImage, axis=0)
result = testModel.predict(testImage, verbose=0)

print("Result : " + str(result))

trainDatagen = image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

trainSet = trainDatagen.flow_from_directory(
    trainSource,
    target_size=(size, size),
    batch_size=32,
    class_mode='categorical'
)

# trainClasses = trainSet.class_indices

ResultMap = {}
for faceValue, faceName in zip(trainSet.class_indices.values(), trainSet.class_indices.keys()):
    ResultMap[faceValue] = faceName

print('####' * 10)
print("Tahmin şu şekildedir : ", str(ResultMap[np.argmax(result)]))


print('####' * 31)
print("class indices values  : " + str(trainSet.class_indices.values()))
print("class indices keys  : " + str(trainSet.class_indices.keys()))
