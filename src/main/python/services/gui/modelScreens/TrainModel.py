import pickle
import os
import random
import shutil
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton
from keras.api.keras import Sequential
from keras.api.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.api.keras.preprocessing.image import ImageDataGenerator

from src.main.python.services.FeaturesService import getComboBoxFeatures, getLabelFeatures, \
    fontTextBox, getButtonFeaturesTrain
from src.resources.Environments import pathFaceOutputs, \
    pathModels, \
    pathFaceResultsMap, countTrainImage, countValidationImage, pngTrain, pathDatasets, pathDatasetsSplit
from src.main.python.PostgreSQL import createTable
from utils.Utils import randomString, useEnviron

useEnviron()


# todo : Eskisi gibi çeşit çeşit resimler olmalı.
class TrainModel(QWidget):
    def __init__(self, mainWidget):
        super(TrainModel, self).__init__()
        self.mainWidget = mainWidget

    def modelTrainScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Eğitimi')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngTrain))

        # Combobox
        labelDataset = getLabelFeatures(QLabel("Veriseti:"), False, True)
        datasetFolders = [f for f in os.listdir(pathDatasets) if os.path.isdir(os.path.join(pathDatasets, f))]
        datasetNames = [''] + datasetFolders
        comboDatasets = getComboBoxFeatures(QComboBox(self))
        comboDatasets.addItems(datasetNames)
        layoutHDataset = QHBoxLayout()
        layoutHDataset.addWidget(labelDataset, alignment=Qt.AlignLeft)
        layoutHDataset.addWidget(comboDatasets, alignment=Qt.AlignRight)

        labelTrain = getLabelFeatures(QLabel("Eğitim%:"), False, True)
        trainPercentage = [''] + ['70%'] + ['80%']
        comboTrain = getComboBoxFeatures(QComboBox(self))
        comboTrain.addItems(trainPercentage)
        layoutHTrain = QHBoxLayout()
        layoutHTrain.addWidget(labelTrain, alignment=Qt.AlignLeft)
        layoutHTrain.addWidget(comboTrain, alignment=Qt.AlignRight)

        labelDropout = getLabelFeatures(QLabel("Dropout:"), False, True)
        dropoutRate = [''] + ['0.3'] + ['0.4'] + ['0.5']
        comboDropout = getComboBoxFeatures(QComboBox(self))
        comboDropout.addItems(dropoutRate)
        layoutHDropout = QHBoxLayout()
        layoutHDropout.addWidget(labelDropout, alignment=Qt.AlignLeft)
        layoutHDropout.addWidget(comboDropout, alignment=Qt.AlignRight)

        labelBatchSize = getLabelFeatures(QLabel("Batch Boyutu:"), False, True)
        batchSizes = [''] + ['4'] + ['8'] + ['16'] + ['32'] + ['64'] + ['128']
        comboBatch = getComboBoxFeatures(QComboBox(self))
        comboBatch.addItems(batchSizes)
        layoutHBatchSize = QHBoxLayout()
        layoutHBatchSize.addWidget(labelBatchSize, alignment=Qt.AlignLeft)
        layoutHBatchSize.addWidget(comboBatch, alignment=Qt.AlignRight)

        # Textbox
        labelInputSize = getLabelFeatures(QLabel("Girdi boyutu:"), False, True)
        textBoxInputSize = QLineEdit()
        textBoxInputSize.setFont(fontTextBox)
        textBoxInputSize.setText("128x128")
        textBoxInputSize.setInputMask("999\\x999")
        layoutHInputSize = QHBoxLayout()
        layoutHInputSize.addWidget(labelInputSize, alignment=Qt.AlignLeft)
        layoutHInputSize.addWidget(textBoxInputSize, alignment=Qt.AlignRight)

        labelEpochsCount = getLabelFeatures(QLabel("Epoch sayısı:"), False, True)
        textBoxEpochsCount = QLineEdit()
        textBoxEpochsCount.setFont(fontTextBox)
        validator = QIntValidator(1, 999)
        textBoxEpochsCount.setValidator(validator)
        textBoxEpochsCount.setText("30")
        textBoxEpochsCount.setFixedSize(40, 30)

        textBoxEpochsCount.setMaxLength(3)
        layoutHEpochsCount = QHBoxLayout()
        layoutHEpochsCount.addWidget(labelEpochsCount, alignment=Qt.AlignLeft)
        layoutHEpochsCount.addWidget(textBoxEpochsCount, alignment=Qt.AlignRight)

        # button
        btnTrainModel = getButtonFeaturesTrain(QPushButton(self), text="Eğit")

        # Ana düzenleyici
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutV1 = QVBoxLayout()
        layoutV2 = QVBoxLayout()

        layoutV1.addLayout(layoutHDataset)
        layoutV1.addLayout(layoutHInputSize)
        layoutV1.addLayout(layoutHEpochsCount)

        layoutV2.addLayout(layoutHTrain)
        layoutV2.addLayout(layoutHBatchSize)
        layoutV2.addLayout(layoutHDropout)

        layoutH.addLayout(layoutV1)
        layoutH.addLayout(layoutV2)
        layoutV.addLayout(layoutH)
        # Add spacing and margins to the layouts
        layoutV.setSpacing(20)
        layoutV.setContentsMargins(50, 50, 50, 50)
        layoutH.setSpacing(20)
        layoutV1.setSpacing(10)
        layoutV1.setContentsMargins(0, 0, 0, 10)
        layoutV2.setSpacing(10)
        layoutV2.setContentsMargins(0, 0, 0, 10)

        # Add the button to the layout
        layoutV.addWidget(btnTrainModel, alignment=Qt.AlignCenter)

        self.window.setLayout(layoutV)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()




def createFaceModel(datasetName, batchSize, trainPercentage, inputSizeW, inputSizeH, dropoutRate, epochsCount):
    trainPercentage = int(trainPercentage / 100)
    pathSet = pathDatasets + datasetName

    # will be created if not exist
    pathSetSplit = pathDatasetsSplit + datasetName
    trainFolder = pathSetSplit + "/train"
    validationFolder = pathSetSplit + "/validation"

    # create the new folders
    if not os.path.exists(pathSetSplit):
        os.makedirs(pathSetSplit)
    if not os.path.exists(trainFolder):
        os.makedirs(trainFolder)
    else:
        shutil.rmtree(trainFolder)
        os.makedirs(trainFolder)
    if not os.path.exists(validationFolder):
        os.makedirs(validationFolder)
    else:
        shutil.rmtree(validationFolder)
        os.makedirs(validationFolder)

    # Her klasör için train ve validation klasörlerine kopyalama
    for folder in os.listdir(pathSet):
        folderPath = os.path.join(pathSet, folder)
        if os.path.isdir(folderPath):
            trainFolderPath = os.path.join(trainFolder, folder)
            validationFolderPath = os.path.join(validationFolder, folder)

            # Train ve Validation klasörlerini oluşturma
            if not os.path.exists(trainFolderPath):
                os.makedirs(trainFolderPath)
            if not os.path.exists(validationFolderPath):
                os.makedirs(validationFolderPath)

            # Dosyaları kopyalama
            files = os.listdir(folderPath)
            random.shuffle(files)
            trainFiles = files[:int(trainPercentage * len(files))]
            validationFiles = files[int(trainPercentage * len(files)):]

            for file in trainFiles:
                shutil.copy2(os.path.join(folderPath, file), os.path.join(trainFolderPath, file))
            for file in validationFiles:
                shutil.copy2(os.path.join(folderPath, file), os.path.join(validationFolderPath, file))

    dataCount = len([f for f in os.listdir(pathSet) if os.path.isdir(os.path.join(pathSet, f))])

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(inputSizeW, inputSizeH, 3)))
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(dropoutRate))
    model.add(Dense(dataCount,
                    activation='softmax'))  # İkili sınıflandırmalarda sigmoid, Dense(farklı yüz sınıf sayısı, softmax)

    # MODEL ÖZETİ
    model.summary()

    # MODEL DERLEME
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    trainGenerator = ImageDataGenerator(rescale=1. / 255).flow_from_directory(
        trainFolder,
        target_size=(inputSizeW, inputSizeH),
        batch_size=batchSize,
        color_mode='rgb',
        class_mode='categorical')

    validationGenerator = ImageDataGenerator(rescale=1. / 255).flow_from_directory(
        validationFolder,
        target_size=(inputSizeW, inputSizeH),
        batch_size=batchSize,
        color_mode='rgb',
        class_mode='categorical')

    trainClasses = trainGenerator.class_indices

    ResultMap = {}
    for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
        ResultMap[faceValue] = faceName

    modelName = "face_" + datasetName + "_" + str(len(trainClasses)) + "_" + str(batchSize) + "_" + str(
        epochsCount) + "_" + str(
        inputSizeW) + "x" + str(inputSizeH) + "_" + randomString(
        3)

    with open(pathFaceResultsMap + modelName + ".pkl", 'wb') as f:
        pickle.dump(ResultMap, f)

    startTime = time.time()

    model.fit(
        trainGenerator,
        steps_per_epoch=len(trainGenerator),
        epochs=epochsCount,
        validation_data=validationGenerator,
        validation_steps=len(validationGenerator),
        verbose=1)

    endTime = time.time()

    xTrain, yTrain = trainGenerator.next()
    xVal, yVal = validationGenerator.next()

    with open(pathFaceOutputs + modelName + '.txt', 'w') as f:
        f.write('Epoch\tLoss\tAccuracy\tVal_Loss\tVal_Accuracy\n')
        for epoch in range(epochsCount):
            loss, accuracy = model.train_on_batch(xTrain, yTrain)
            valLoss, valAccuracy = model.test_on_batch(xVal, yVal)
            f.write('{}\t{}\t{}\t{}\t{}\n'.format(epoch + 1, loss, accuracy, valLoss, valAccuracy))
        f.write('\n{} minutes'.format(int(round(endTime - startTime) / 60)))

    # save the model
    model.save(pathModels + modelName + '.h5')
    createTable(modelName + '.h5')

    return str(modelName + '.h5')
