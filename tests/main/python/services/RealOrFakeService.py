import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Dropout
import numpy as np
from keras.api.keras.preprocessing import image
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.models import load_model

from tests.resources.Environments import pathModels, pathTrain, pathValidation, pathTest

from utils.Utils import randomString, useEnviron

# Uyarı engelleme
useEnviron()
try:
    from tensorflow.python.util import module_wrapper as deprecation
except ImportError:
    from tensorflow.python.util import deprecation_wrapper as deprecation
deprecation._PER_MODULE_WARNING_LIMIT = 0

newModelName = "RorF_" + randomString(4) + ".h5"


def trainModel():
    batchSize = 128
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,  # yeni eklenen veri augmentasyonu
        fill_mode='constant')  # yeni eklenen veri augmentasyonu

    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

    training_set = train_datagen.flow_from_directory(pathTrain,
                                                     target_size=(128, 128),
                                                     batch_size=batchSize,
                                                     class_mode='binary')

    validation_set = validation_datagen.flow_from_directory(pathValidation,
                                                            target_size=(128, 128),
                                                            batch_size=batchSize,
                                                            class_mode='binary')

    h1 = plt.hist(training_set.classes, bins=range(0, 3), alpha=0.8, color='blue', edgecolor='black')
    h2 = plt.hist(validation_set.classes, bins=range(0, 3), alpha=0.8, color='red', edgecolor='black')
    plt.ylabel('# of instances')
    plt.xlabel('Class')

    for X, y in training_set:
        print(X.shape, y.shape)
        plt.figure(figsize=(16, 16))
        for i in range(16):
            plt.subplot(4, 4, i + 1)
            plt.axis('off')
            plt.title('Label: ')
            img = np.uint8(255 * X[i, :, :, 0])
            plt.imshow(img, cmap='gray')
        break

    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(128, 128, 3)))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, kernel_size=(3, 3),
                     activation='relu'))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3),
                     activation='relu'))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    model.add(Dense(units=256,
                    activation="relu"))

    model.add(Dropout(rate=0.25))  # dropout layer eklendi

    model.add(Dense(units=1,
                    activation="sigmoid"))

    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),  # optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(filepath=pathModels + newModelName, monitor='val_loss', save_best_only=True, mode='max'),
    ]

    history = model.fit(
        training_set,
        steps_per_epoch=len(training_set),
        epochs=50,  # epoch sayısı arttırıldı
        validation_data=validation_set,
        validation_steps=len(validation_set),
        callbacks=callbacks_list
    )
    printInfo(history)

    training_set.class_indices  # {'fake': 0, 'real': 1}

    model.save(pathModels + newModelName)


def printInfo(history):
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    nepochs = len(history.history['loss'])
    plt.plot(range(nepochs), history.history['loss'], 'r-', label='train')
    plt.plot(range(nepochs), history.history['val_loss'], 'b-', label='test')
    plt.legend(prop={'size': 20})
    plt.ylabel('loss')
    plt.xlabel('# of epochs')
    plt.subplot(1, 2, 2)
    plt.plot(range(nepochs), history.history['accuracy'], 'r-', label='train')
    plt.plot(range(nepochs), history.history['val_accuracy'], 'b-', label='test')
    plt.legend(prop={'size': 20})
    plt.ylabel('accuracy')
    plt.xlabel('# of epochs')


def testImage(testImageName, modelName):
    model = load_model(pathModels + modelName)
    pathImage = pathTest + testImageName

    test_image = image.load_img(pathImage, target_size=(128, 128))
    plt.axis('off')
    plt.imshow(test_image)
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    if result[0][0] == 1:
        predictions = 'Gerçek'
    else:
        predictions = 'Sahte'
    print('Sonuç: ', predictions)
