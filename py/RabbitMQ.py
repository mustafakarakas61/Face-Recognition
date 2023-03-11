import pika

from py.ImageService import downloadImage

# SETS
name = "Serenay Sarıkaya"
queueTrain = "py_train"
queueTest = "py_test"
queueValidation = "py_validation"
datasetName = "myset"

# PATHS
pathDatasets = "C:/Project/Proje-2/face_recognition/datasets/"
folderNameFolderInTrain = pathDatasets + datasetName + "/train/" + name
folderNameFolderInValidation = pathDatasets + datasetName + "/validation/" + name
folderNameFolderInTest = pathDatasets + datasetName + "/test/"

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
