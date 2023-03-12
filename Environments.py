# ENVS
countTrainImage = 30
countValidationImage = 15
countTestImage = 1
datasetName = "myset"
successRate = 98.5

# MODEL ENVS
countEpochs = 50
inputSize = 64

# RabbitMQ ENVS
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
pathTempFolder = pathUtils + "tempFolder"
pathNoFace = pathUtils + "NoFace.txt"
