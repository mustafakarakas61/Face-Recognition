import pickle
import os
import time
import numpy as np
from keras import layers, models, optimizers
from keras.api.keras.preprocessing import image

from utils.Utils import randomString

# SETS
datasetName = "myset"
# testImageName = "test_1.jpg"

# PATHS
modelName = datasetName + "_" + randomString(6)
pathModels = "C:/Project/Proje-2/face_recognition/models/"
pathTxts = pathModels + "txts/"
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
trainSource = pathDatasets + datasetName + "/train"
validationSource = pathDatasets + datasetName + "/validation"
# testImagePath = pathDatasets + datasetName + "/test/" + testImageName

trainDatagen = image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)
validationDatagen = image.ImageDataGenerator()

trainGenerator = trainDatagen.flow_from_directory(
    trainSource,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)
validationGenerator = validationDatagen.flow_from_directory(
    validationSource,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

trainClasses = trainGenerator.class_indices
validationClasses = validationGenerator.class_indices

ResultMap = {}
for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
    ResultMap[faceValue] = faceName

with open("../ResultsMap.pkl", 'wb') as fileWriteStream:
    pickle.dump(ResultMap, fileWriteStream)

print("Yüzün ve ID'nin Haritalanması : \n", ResultMap)

# outputNeurons = len(ResultMap)
# print("Çıkış nöronlarının sayısı : ", outputNeurons)

# MODEL OLUŞTURMA - CNN BAŞLATILMASI
inputShape = (150, 150, 3)
model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), input_shape=inputShape))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(32, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Flatten())
model.add(layers.Dense(64))
model.add(layers.Activation('relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(4))  # sınıf sayısı
model.add(layers.Activation('sigmoid'))
# MODEL ÖZETİ
model.summary()
# GRAFİK KARTI UYARISINDAN KURTULMAK İÇİN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# MODEL DERLEME
model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.RMSprop(learning_rate=1e-4),
    metrics=['acc']
)
# MODELİN EĞİTİM İÇİN HARCADIĞI SÜREYİ ÖLÇME
startTime = time.time()

model.fit(
    trainGenerator,
    steps_per_epoch=len(trainGenerator),
    epochs=100,
    validation_data=validationGenerator,
    validation_steps=len(validationGenerator)
)

endTime = time.time()

print("Toplam geçen süre : ", round(endTime - startTime) / 60, "minutes")

x_train, y_train = trainGenerator.next()
x_val, y_val = validationGenerator.next()

with open(pathTxts + modelName + '.txt', 'w') as file:
    file.write('Epoch\tLoss\tAccuracy\tVal_Loss\tVal_Accuracy\n')
    for epoch in range(100):
        loss, accuracy = model.train_on_batch(x_train, y_train)
        val_loss, val_accuracy = model.test_on_batch(x_val, y_val)
        file.write('{}\t{}\t{}\t{}\t{}\n'.format(epoch + 1, loss, accuracy, val_loss, val_accuracy))

# # TAHMİNLERİ YAPMA
# testImage = image.load_img(testImagePath, target_size=(150, 150))
# testImage = image.img_to_array(testImage)
# testImage = np.expand_dims(testImage, axis=0)
# result = model.predict(testImage, verbose=0)
#
# print("Tahmin şu şekildedir : ", ResultMap[np.argmax(result)])

# MODEL KAYDET
model.save(pathModels + modelName + '.h5')

print('Model {} ismiyle başarıyla kaydedildi.'.format(modelName + '.h5'))
