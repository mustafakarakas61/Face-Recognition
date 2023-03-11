import pickle
import os
import time
from keras.api.keras import Sequential
from keras.api.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.api.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras import layers, models, optimizers

from utils.Utils import randomString

# GRAFİK KARTI UYARISINDAN KURTULMAK İÇİN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# SETS
datasetName = "myset"
countEpochs = 30
size = 64
# testImageName = "test_1.jpg"

# PATHS
pathModels = "C:/Project/Proje-2/face_recognition/models/"
pathTxts = pathModels + "txts/"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
trainDir = pathDatasets + datasetName + "/train"
validationDir = pathDatasets + datasetName + "/validation"

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(size, size, 3)))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(16, activation='softmax'))

# MODEL ÖZETİ
model.summary()

# MODEL DERLEME
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(rescale=1. / 255)

trainGenerator = train_datagen.flow_from_directory(
    trainDir,
    target_size=(size, size),
    batch_size=32,
    class_mode='categorical')

validation_generator = ImageDataGenerator(rescale=1. / 255).flow_from_directory(
    validationDir,
    target_size=(size, size),
    batch_size=32,
    class_mode='categorical')

trainClasses = trainGenerator.class_indices

ResultMap = {}
for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
    ResultMap[faceValue] = faceName

with open("../ResultsMap.pkl", 'wb') as fileWriteStream:
    pickle.dump(ResultMap, fileWriteStream)

print("Yüzün ve ID'nin Haritalanması : \n", ResultMap)

startTime = time.time()

history = model.fit(
    trainGenerator,
    steps_per_epoch=len(trainGenerator),
    epochs=countEpochs,
    validation_data=validation_generator,
    validation_steps=len(validation_generator),
    verbose=1)

endTime = time.time()

print("Toplam geçen süre : ", round(endTime - startTime) / 60, "dakika")

x_train, y_train = trainGenerator.next()
x_val, y_val = validation_generator.next()

modelName = datasetName + "_" + str(len(trainClasses)) + "_" + str(countEpochs) + "_" + str(size) + "_" + randomString(
    3)

with open(pathTxts + modelName + '.txt', 'w') as file:
    file.write('Epoch\tLoss\tAccuracy\tVal_Loss\tVal_Accuracy\n')
    for epoch in range(countEpochs):
        loss, accuracy = model.train_on_batch(x_train, y_train)
        val_loss, val_accuracy = model.test_on_batch(x_val, y_val)
        file.write('{}\t{}\t{}\t{}\t{}\n'.format(epoch + 1, loss, accuracy, val_loss, val_accuracy))

# MODEL KAYDET
model.save(pathModels + modelName + '.h5')

print('Model {} ismiyle başarıyla kaydedildi.'.format(modelName + '.h5'))
