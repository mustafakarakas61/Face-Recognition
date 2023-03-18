# ENVS
minFaceSize = 300
minTestFaceSize = 128
skipFrames = 6
countTrainImage = 160  # Toplam Resmin %80
countValidationImage = 40  # Toplam Resmin %20
countTestImage = 1
timeSleep = 0 # 1 veya 2
datasetName = "myset"
successRate = 90

# MODEL ENVS
countEpochs = 30
inputSize = 128  # 64

# RabbitMQ ENVS
queueYoutubeVideoTest = "py_youtube_video_test"
queueYoutube = "py_youtube"
queueTrain = "py_train"
queueTest = "py_test"
queueValidation = "py_validation"

# PostgreSQL ENVS
dbName = "student-list"
dbUser = "postgres"
dbPass = "180200"
dbHost = "localhost"
dbPort = "5432"

# PATHS
pathProject = "C:/Project/Proje-2/face_recognition/"
pathModels = pathProject + "models/"
pathOutputs = pathModels + "outputs/"
pathMaps = pathModels + "maps/"
pathDatasets = pathProject + "datasets/"
pathUtils = pathProject + "utils/"
pathTrain = pathDatasets + datasetName + "/train/"
pathValidation = pathDatasets + datasetName + "/validation/"
pathTest = pathDatasets + datasetName + "/test/"
pathResultsMap = pathMaps + "ResultsMap-"
pathFaceCascade = pathProject + "haarcascade_frontalface_default.xml"
pathTempFolder = pathUtils + "tempFolder/"
pathControlFolder = pathUtils + "controlFolder/"
pathNoFace = pathUtils + "NoFace.txt"
