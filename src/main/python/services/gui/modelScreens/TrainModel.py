import pickle
import os
import time
from keras.api.keras import Sequential
from keras.api.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.api.keras.preprocessing.image import ImageDataGenerator

from src.resources.Environments import datasetName, countEpochs, inputSize, pathTrain, pathValidation, pathFaceOutputs, pathModels, \
    pathFaceResultsMap, countTrainImage, countValidationImage
from src.main.python.PostgreSQL import createTable
from utils.Utils import randomString, useEnviron

useEnviron()

# input
size = inputSize


# todo : veri seti arttırılmalı, Eskisi gibi çeşit çeşit resimler olmalı.

def createFaceModel():
    trainDirCount = len([f for f in os.listdir(pathTrain) if os.path.isdir(os.path.join(pathTrain, f))])

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
    model.add(Dense(trainDirCount, activation='softmax'))

    # MODEL ÖZETİ
    model.summary()

    # MODEL DERLEME
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    trainDatagen = ImageDataGenerator(rescale=1. / 255)
    validationDatagen = ImageDataGenerator(rescale=1. / 255)

    trainGenerator = trainDatagen.flow_from_directory(
        pathTrain,
        target_size=(size, size),
        batch_size=32,
        color_mode='rgb',  # grayscale girdi boyutu 1 ise
        class_mode='categorical')

    validationGenerator = validationDatagen.flow_from_directory(
        pathValidation,
        target_size=(size, size),
        batch_size=32,
        color_mode='rgb',
        class_mode='categorical')

    trainClasses = trainGenerator.class_indices

    ResultMap = {}
    for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
        ResultMap[faceValue] = faceName

    modelName = "face_" + datasetName + "_" + str(len(trainClasses)) + "_" + str(countEpochs) + "_" + str(
        size) + "_" + randomString(
        3)

    with open(pathFaceResultsMap + modelName + ".pkl", 'wb') as f:
        pickle.dump(ResultMap, f)

    print("Yüzün ve ID'nin Haritalanması : \n", ResultMap)
    print("Train setindeki bir veride bulunan resim sayısı : " + str(countTrainImage) +
          "\nValidation setindeki bir veride bulunan resim sayısı : " + str(countValidationImage))

    startTime = time.time()

    history = model.fit(
        trainGenerator,
        steps_per_epoch=len(trainGenerator),
        epochs=countEpochs,
        validation_data=validationGenerator,
        validation_steps=len(validationGenerator),
        verbose=1)

    endTime = time.time()

    print("Toplam geçen süre : ", round(endTime - startTime) / 60, "dakika")

    xTrain, yTrain = trainGenerator.next()
    xVal, yVal = validationGenerator.next()

    with open(pathFaceOutputs + modelName + '.txt', 'w') as f:
        f.write('Epoch\tLoss\tAccuracy\tVal_Loss\tVal_Accuracy\n')
        for epoch in range(countEpochs):
            loss, accuracy = model.train_on_batch(xTrain, yTrain)
            valLoss, valAccuracy = model.test_on_batch(xVal, yVal)
            f.write('{}\t{}\t{}\t{}\t{}\n'.format(epoch + 1, loss, accuracy, valLoss, valAccuracy))

    # MODEL KAYDET
    model.save(pathModels + modelName + '.h5')
    createTable(modelName + '.h5')

    print('Model {} ismiyle başarıyla kaydedildi.'.format(modelName + '.h5'))


createFaceModel()
