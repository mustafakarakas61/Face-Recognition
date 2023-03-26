import os
import time

import pika
import json

from Environments import pathTrain, pathValidation, pathTest, queueTrain, queueValidation, queueTest, queueYoutube, \
    queueYoutubeVideoTest, queueClipVideo
from py.model.TestModelFromVideo import findFacesFromVideo
from py.services.DownloadImageService import downloadImage
from py.services.ExtractFaceService import extractFaces
from py.services.ExtractImageService import extractImageFromVideo
from py.youtube.YoutubeDownloaderClip import createClippedVideo

from utils.Utils import checkFolder, controlFilesNumbers

# getFolderList(pathTrain)
# name = input("Lütfen bir isim girin ya da bir isim seçin: ")
name = "Deneme"

folderNameFolderInTrain = pathTrain + name
checkFolder(folderNameFolderInTrain)
folderNameFolderInValidation = pathValidation + name
checkFolder(folderNameFolderInValidation)
folderNameFolderInTest = pathTest

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

print("RabbitMQ başlatıldı.")


def consumeYoutubeVideoTest(ch, method, properties, body):
    msg = body.decode()
    print("Gelen video path : " + msg)

    findFacesFromVideo(str(msg).replace("\\", "/"), "myset_10_30_128_ryc.h5")


def consumeClipYoutube(ch, method, properties, body):
    msg = json.loads(body.decode())

    createClippedVideo(msg['url'], msg['ss'], msg['to'], msg['name'])

# TODO : consumeClipYoutube'e ayarlanacak bu metod
# def consumeYoutube(ch, method, properties, body):  # TODO : json kontrolü yapılmalı, yukarıya entegrele
#     # {"name":"Name Surname","video":"https://www.youtube.com/watch?v=JkQG2PBQ_48"}
#     msg = json.loads(body.decode())
#     print("Gelen mesaj : ", msg)
#     msgVideoPath = msg['video']
#     msgName = msg['name']
#
#     folderName = pathTrain + msgName
#     checkFolder(folderName)
#
#     pathVideo = str(msgVideoPath).replace("\\", "/")
#     controlFilesNumbers(folderName)
#     if extractImageFromVideo(pathVideo, msgName, 200):
#         extractFaces(msgName, folderName)
#
#         os.remove(pathVideo)
#         time.sleep(20)
#         controlFilesNumbers(folderName)
#         print(str(msgName) + " için işlem tamamlandı.\n")


def consumeTrain(ch, method, properties, body):
    msg = body.decode()
    print("Gelen URL : " + msg)
    downloadImage(msg, name, folderNameFolderInTrain, False)


def consumeValidation(ch, method, properties, body):
    msg = body.decode()
    print("Gelen URL : " + msg)
    downloadImage(msg, name, folderNameFolderInValidation, False)


def consumeTest(ch, method, properties, body):
    msg = body.decode()
    print("Gelen URL : " + msg)
    downloadImage(msg, name, folderNameFolderInTest, True)


channel.basic_consume(
    queue=queueYoutubeVideoTest, on_message_callback=consumeYoutubeVideoTest, auto_ack=True)

channel.basic_consume(
    queue=queueClipVideo, on_message_callback=consumeClipYoutube, auto_ack=True)

channel.basic_consume(
    queue=queueTrain, on_message_callback=consumeTrain, auto_ack=True)

channel.basic_consume(
    queue=queueValidation, on_message_callback=consumeValidation, auto_ack=True)

channel.basic_consume(
    queue=queueTest, on_message_callback=consumeTest, auto_ack=True)

channel.start_consuming()
