import pika

from Environments import pathTrain, pathValidation, pathTest, queueTrain, queueValidation, queueTest
from py.services.DownloadImageService import downloadImage

from utils.Utils import getFolderList, checkFolder

getFolderList(pathTrain)
name = input("Lütfen bir isim girin ya da bir isim seçin: ")

folderNameFolderInTrain = pathTrain + name
checkFolder(folderNameFolderInTrain)
folderNameFolderInValidation = pathValidation + name
checkFolder(folderNameFolderInValidation)
folderNameFolderInTest = pathTest

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

print("RabbitMQ başlatıldı.")


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
    queue=queueTrain, on_message_callback=consumeTrain, auto_ack=True)

channel.basic_consume(
    queue=queueValidation, on_message_callback=consumeValidation, auto_ack=True)

channel.basic_consume(
    queue=queueTest, on_message_callback=consumeTest, auto_ack=True)

channel.start_consuming()
