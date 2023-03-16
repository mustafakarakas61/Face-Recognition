import pika
import json

from Environments import pathTrain, pathValidation, pathTest, queueTrain, queueValidation, queueTest, queueYoutube
from py.services.DownloadImageService import downloadImage
from py.services.ExtractFaceService import extractFaces
from py.services.ExtractImageService import extractImageFromVideo
from py.services.YouTubeVideoDownloaderService import downloadYouTubeVideo

from utils.Utils import getFolderList, checkFolder

getFolderList(pathTrain)
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


def consumeYoutube(ch, method, properties, body):
    # {"name":"Name Surname","url":"https://www.youtube.com/watch?v=JkQG2PBQ_48"}
    msg = json.loads(body.decode())
    print("Gelen mesaj : ", msg)
    msgUrl = msg['url']
    msgName = msg['name']

    folderName = pathTrain + msgName
    checkFolder(folderName)

    pathVideo = downloadYouTubeVideo(msgUrl, msgName)
    if extractImageFromVideo(pathVideo, msgName, 200):
        extractFaces(msgName, folderName)


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
    queue=queueYoutube, on_message_callback=consumeYoutube, auto_ack=True)

channel.basic_consume(
    queue=queueTrain, on_message_callback=consumeTrain, auto_ack=True)

channel.basic_consume(
    queue=queueValidation, on_message_callback=consumeValidation, auto_ack=True)

channel.basic_consume(
    queue=queueTest, on_message_callback=consumeTest, auto_ack=True)

channel.start_consuming()
