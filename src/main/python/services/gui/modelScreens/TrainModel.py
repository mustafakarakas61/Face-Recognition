import pickle
import os
import random
import shutil
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton, QMessageBox
from keras.api.keras import Sequential
from keras.api.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.api.keras.preprocessing.image import ImageDataGenerator

from src.main.python.services.FeaturesService import getComboBoxFeatures, getLabelFeatures, \
    fontTextBox, getButtonFeaturesTrain, getMsgBoxFeatures
from src.resources.Environments import pathFaceOutputs, \
    pathModels, \
    pathFaceResultsMap, pngTrain, pathDatasets, pathDatasetsSplit, pngWarningBox, pngInfoBox
from src.main.python.PostgreSQL import createTable
from utils.Utils import randomString, useEnviron

useEnviron()


# todo : Eskisi gibi çeşit çeşit resimler olmalı.
class TrainModel(QWidget):
    def __init__(self, mainWidget):
        super(TrainModel, self).__init__()
        self.mainWidget = mainWidget

        # started
        self.selectedDatasetName = ""
        self.selectedTrainPercentage = ""
        self.selectedDropoutRate = ""
        self.selectedBatchSize = ""
        self.epochsCount = "30"
        self.inputSize = "128x128"

    def modelTrainScreen(self):
        mainWith = 500
        mainHeight = 250
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
        comboDatasets.currentIndexChanged.connect(
            lambda index: self.onComboDatasetsSelection(comboDatasets.itemText(index)))
        layoutHDataset = QHBoxLayout()
        layoutHDataset.addWidget(labelDataset, alignment=Qt.AlignLeft)
        layoutHDataset.addWidget(comboDatasets, alignment=Qt.AlignRight)

        labelTrain = getLabelFeatures(QLabel("Eğitim%:"), False, True)
        trainPercentage = [''] + ['70%'] + ['80%']
        comboTrain = getComboBoxFeatures(QComboBox(self))
        comboTrain.addItems(trainPercentage)
        comboTrain.currentIndexChanged.connect(lambda index: self.onComboTrainSelection(comboTrain.itemText(index)))
        layoutHTrain = QHBoxLayout()
        layoutHTrain.addWidget(labelTrain, alignment=Qt.AlignLeft)
        layoutHTrain.addWidget(comboTrain, alignment=Qt.AlignRight)

        labelDropout = getLabelFeatures(QLabel("Dropout:"), False, True)
        dropoutRate = [''] + ['0.3'] + ['0.4'] + ['0.5']
        comboDropout = getComboBoxFeatures(QComboBox(self))
        comboDropout.addItems(dropoutRate)
        comboDropout.currentIndexChanged.connect(
            lambda index: self.onComboDropoutSelection(comboDropout.itemText(index)))
        layoutHDropout = QHBoxLayout()
        layoutHDropout.addWidget(labelDropout, alignment=Qt.AlignLeft)
        layoutHDropout.addWidget(comboDropout, alignment=Qt.AlignRight)

        labelBatchSize = getLabelFeatures(QLabel("Batch boyutu:"), False, True)
        batchSizes = [''] + ['4'] + ['8'] + ['16'] + ['32'] + ['64'] + ['128']
        comboBatch = getComboBoxFeatures(QComboBox(self))
        comboBatch.addItems(batchSizes)
        comboBatch.currentIndexChanged.connect(lambda index: self.onComboBatchSelection(comboBatch.itemText(index)))
        layoutHBatchSize = QHBoxLayout()
        layoutHBatchSize.addWidget(labelBatchSize, alignment=Qt.AlignLeft)
        layoutHBatchSize.addWidget(comboBatch, alignment=Qt.AlignRight)

        # Textbox
        labelInputSize = getLabelFeatures(QLabel("Girdi boyutu:"), False, True)
        textBoxInputSize = QLineEdit()
        textBoxInputSize.setFont(fontTextBox)
        textBoxInputSize.setText("128x128")
        textBoxInputSize.setInputMask("999\\x999")
        textBoxInputSize.textChanged.connect(lambda index: self.onTextBoxInputSizeChange(textBoxInputSize.text()))
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
        textBoxEpochsCount.textChanged.connect(lambda index: self.onTextBoxEpochsCountChange(textBoxEpochsCount.text()))
        layoutHEpochsCount = QHBoxLayout()
        layoutHEpochsCount.addWidget(labelEpochsCount, alignment=Qt.AlignLeft)
        layoutHEpochsCount.addWidget(textBoxEpochsCount, alignment=Qt.AlignRight)

        # button
        btnTrainModel = getButtonFeaturesTrain(QPushButton(self), text="Eğit")
        btnTrainModel.clicked.connect(self.startTrain)

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

    def startTrain(self):
        datasetName = self.selectedDatasetName
        trainPercentage = self.selectedTrainPercentage
        dropoutRate = self.selectedDropoutRate
        batchSize = self.selectedBatchSize
        epochsCount = self.epochsCount
        inputSizeW, inputSizeH = self.inputSize.split("x")

        if len(str(datasetName)) > 0 and len(str(trainPercentage)) > 0 and len(str(dropoutRate)) > 0 and len(
                str(batchSize)) > 0 and len(str(epochsCount)) > 0 and len(str(inputSizeW)) > 0 and len(
            str(inputSizeH)) > 0:
            # todo : return true olduğunda güncellensin Model Seçiniz vs
            reply = getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Bilgi", '<b>Model eğitimi başlatılsın mı</b>?'
                                                                              f"<table border=1>"
                                                                              f"<tr><td><b>Veriseti</b></td><td>{datasetName}</td></tr>"
                                                                              f"<tr><td><b>Eğitim%</b></td><td>{trainPercentage}</td></tr>"
                                                                              f"<tr><td><b>Dropout</b></td><td>{dropoutRate}</td></tr>"
                                                                              f"<tr><td><b>Batch boyutu</b></td><td>{batchSize}</td></tr>"
                                                                              f"<tr><td><b>Epoch sayısı</b></td><td>{epochsCount}</td></tr>"
                                                                              f"<tr><td><b>Girdi boyutu</b></td><td>G:{inputSizeW}, Y:{inputSizeH}</td></tr>"
                                                                              f"</table>",
                                      QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                      isQuestion=True).exec_()

            if reply == QtWidgets.QMessageBox.Yes:
                print("Model eğitimi")

                trainedModelName = createFaceModel(str(datasetName), int(batchSize),
                                                   float(trainPercentage.replace("%", "")),
                                                   int(inputSizeW),
                                                   int(inputSizeH), float(dropoutRate), int(epochsCount))
                self.window.close()

                infoModelOutputs = pathFaceOutputs + trainedModelName.replace(".h5", ".txt")

                with open(infoModelOutputs, 'r') as file:
                    lines = file.readlines()
                    infoTime = lines[-1].strip().replace("\t", "").replace("minutes", "dakika")
                    epoch, trainLoss, trainAccuracy, valLoss, valAccuracy = lines[-3].strip().split("\t")

                getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Model Başarıyla Kaydedildi",
                                  f"<b>Model ismi:</b> {trainedModelName}"
                                  f"<br><b>Geçen süre:</b> {infoTime}"
                                  f"<hr>"
                                  f"<table border=1>"
                                  f"<tr><td><b>Başarı Oranı</b></td><td><b>Kayıp</b></td><td><b>Doğruluk</b></td></tr>"
                                  f"<tr><td><b>Eğitim Seti</b></td><td>{round(float(trainLoss), 4)}</td><td>{round(float(trainAccuracy), 4)}</td></tr>"
                                  f"<tr><td><b>Doğrulama Seti</b></td><td>{round(float(valLoss), 4)}</td><td>{round(float(valAccuracy), 4)}</td></tr>"
                                  f"</table>",
                                  QMessageBox.Information, QMessageBox.Ok, isQuestion=False).exec_()
                self.selectedDatasetName = ""
                self.selectedTrainPercentage = ""
                self.selectedDropoutRate = ""
                self.selectedBatchSize = ""
                self.epochsCount = "30"
                self.inputSize = "128x128"



        else:
            emptyFields = []
            if len(str(datasetName)) == 0:
                emptyFields.append("\nVeriseti")
            if len(str(trainPercentage)) == 0:
                emptyFields.append("\nEğitim%")
            if len(str(dropoutRate)) == 0:
                emptyFields.append("\nDropout")
            if len(str(batchSize)) == 0:
                emptyFields.append("\nBatch boyutu")
            if len(str(epochsCount)) == 0:
                emptyFields.append("\nEpoch sayısı")
            if len(str(inputSizeW)) == 0 or len(str(inputSizeH)) == 0:
                emptyFields.append("\nGirdi boyutu")

            emptyFieldsStr = ", ".join(emptyFields)
            getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Dikkat !",
                              f"Lütfen aşağıdaki alanları doldurunuz! {emptyFieldsStr}", QMessageBox.Warning,
                              QMessageBox.Ok, isQuestion=False).exec_()

    def onTextBoxEpochsCountChange(self, newValue):
        self.epochsCount = newValue

    def onTextBoxInputSizeChange(self, newValue):
        self.inputSize = newValue

    def onComboDatasetsSelection(self, newName):
        self.selectedDatasetName = newName

    def onComboTrainSelection(self, newName):
        self.selectedTrainPercentage = newName

    def onComboDropoutSelection(self, newName):
        self.selectedDropoutRate = newName

    def onComboBatchSelection(self, newName):
        self.selectedBatchSize = newName


def createFaceModel(datasetName, batchSize, trainPercentage, inputSizeW, inputSizeH, dropoutRate, epochsCount):
    trainPercentage = float(trainPercentage / 100)
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

    return modelName + '.h5'
