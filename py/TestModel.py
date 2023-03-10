import os
import numpy as np
from keras.models import load_model
from keras.api.keras.preprocessing import image

from utils.Utils import getFileList

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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
testImageName = input("Lütfen test için bir resim ismi giriniz: ")

testModel = load_model(pathModels + modelName)
testImage = image.load_img(pathTestImage + testImageName, target_size=(150, 150))
testImage = image.img_to_array(testImage)
testImage = np.expand_dims(testImage, axis=0)
result = testModel.predict(testImage, verbose=0)

trainDatagen = image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

trainSet = trainDatagen.flow_from_directory(
    trainSource,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

trainClasses = trainSet.class_indices

ResultMap = {}
for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
    ResultMap[faceValue] = faceName

print('####' * 10)
print("Tahmin şu şekildedir : ", ResultMap[np.argmax(result)])
