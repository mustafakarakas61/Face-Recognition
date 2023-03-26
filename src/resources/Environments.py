#  E  N  V  S  #

# Environments
minFaceSize = 300
minTestFaceSize = 128
skipFrames = 6
durationVideo = 60  # 60sn
countTrainImage = 12  # Toplam Resmin %80
countValidationImage = 3  # Toplam Resmin %20
countTestImage = 1
imageLimit = 250
timeSleep = 0  # 1 veya 2
datasetName = "myset_v2"
successRate = 90

# Environments_Model
countEpochs = 30
inputSize = 64  # 64

# Environments_RabbitMQ
queueYoutubeVideoTest = "py_youtube_video_test"
queueFaceFromYoutube = "py_face_from_youtube"
queueFaceFromVideo = "py_face_from_video"

# Environments_PostgreSQL
dbName = "student-list"
dbUser = "postgres"
dbPass = "180200"
dbHost = "localhost"
dbPort = "5432"

#  P  A  T  H  S  #
pathProject = "C:/Project/Proje-2/face_recognition/"
pathMain = "src/main/"
pathResources = "src/resources/"

# Models
pathModels = pathProject + pathMain + "models/"
# Models_Eye
pathEye = pathModels + "eye/"
pathEyeOutputs = pathEye + "outputs/"
pathEyeMaps = pathEye + "maps/"
pathEyeResultsMap = pathEyeMaps + "ResultsMap-"
# Models_Face
pathFace = pathModels + "face/"
pathFaceOutputs = pathFace + "outputs/"
pathFaceMaps = pathFace + "maps/"
pathFaceResultsMap = pathFaceMaps + "ResultsMap-"

# Datasets
pathDatasets = pathProject + pathMain + "datasets/"
pathTrain = pathDatasets + datasetName + "/train/"
pathValidation = pathDatasets + datasetName + "/validation/"
pathTest = pathDatasets + datasetName + "/test/"

# Cascades
pathFaceCascade = pathProject + pathResources + "haarcascade_frontalface_default.xml"
pathEyeCascade = pathProject + pathResources + "haarcascade_eye.xml"

# Utils
pathUtils = pathProject + "utils/"
pathClippedVideos = pathUtils + "clippedVideos/"
pathTempFolder = pathUtils + "tempFolder/"
pathControlFolder = pathUtils + "controlFolder/"
pathNoFace = pathUtils + "NoFace.txt"
