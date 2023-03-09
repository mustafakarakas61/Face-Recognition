import os
import numpy as np
from keras.models import load_model
from keras.api.keras.preprocessing import image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# PATHS
pathModel = "C:/Project/Proje-2/face_recognition/model/"
# trainImages = "C:/Project/Proje-2/face_recognition/dataset/train_images"
trainImages = "C:/Project/Proje-2/face_recognition/dataset/train_1/Image_Train"

# SETS
testImagePath = "C:/Project/Proje-2/face_recognition/dataset/test_1/Image_Test/MEGHANA/MEGHANA_17.jpeg"
modelName = "rxnezn.h5"

testModel = load_model(pathModel + modelName)
testImage = image.load_img(testImagePath, target_size=(150, 150))
testImage = image.img_to_array(testImage)
testImage = np.expand_dims(testImage, axis=0)
result = testModel.predict(testImage, verbose=0)

trainDatagen = image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

trainSet = trainDatagen.flow_from_directory(
    trainImages,
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
