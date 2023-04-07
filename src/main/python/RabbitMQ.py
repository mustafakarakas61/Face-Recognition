import time

import pika
import json

from src.main.python.services.ImageDownloaderService import downloadImageFaceJson, \
    downloadImageFaceString
from src.resources.Environments import pathTrain, queueYoutubeVideoTest, imageLimit, queueFaceFromYoutube, \
    queueFaceFromVideo, queueFaceFromImage
from src.main.python.services.ExtractImageService import extractImageFromVideo, extractFaces

from utils.Utils import checkFolder, controlFilesNumbers

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

print("RabbitMQ başlatıldı.")


def consumeYoutubeVideoTest(ch, method, properties, body):
    # {"video":"c:/","model":"myset_10_30_128_ryc.h5"}
    msg = json.loads(body.decode())

    # findFacesFromVideo(msg['video'], msg['model'], successRate)


def consumeFaceFromImage(ch, method, properties, body):
    try:
        # {"name":"Name Surname","url":"https://img"}
        msg = json.loads(body.decode())

        downloadImageFaceJson(msg['name'], msg['url'])
    except ValueError:
        msg = body.decode()
        downloadImageFaceString(msg)


def consumeFaceFromVideo(ch, method, properties, body):
    # {"name":"Name Surname","video":"c:/"}
    msg = json.loads(body.decode())

    folderName = pathTrain + msg['name']
    checkFolder(folderName)

    controlFilesNumbers(folderName)
    if extractImageFromVideo(msg['video'], msg['name'], imageLimit):
        extractFaces(msg['name'], folderName)

        # os.remove(pathVideo)
        time.sleep(20)
        controlFilesNumbers(folderName)
        print(str(msg['name']) + " için işlem tamamlandı.\n")


channel.basic_consume(
    queue=queueYoutubeVideoTest, on_message_callback=consumeYoutubeVideoTest, auto_ack=True)

channel.basic_consume(
    queue=queueFaceFromImage, on_message_callback=consumeFaceFromImage, auto_ack=True)

channel.basic_consume(
    queue=queueFaceFromVideo, on_message_callback=consumeFaceFromVideo, auto_ack=True)

channel.start_consuming()
