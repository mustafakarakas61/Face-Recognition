#  E  N  V  S  #
# Environments
minFaceSize = 128
minTestFaceSize = 128
skipFrames = 6
durationVideo = 60  # 60sn

imageLimit = 250
timeSleep = 0  # 1 veya 2
personName = "Mustafa Karakaş"
datasetName = "myset_v3"
successRate = 90

totalImage = 20
countTrainImage = int((totalImage * 70) / 100)  # Toplam Resmin %80 %70
countValidationImage = int((totalImage * 30) / 100)  # Toplam Resmin %20 %30
countTestImage = 1

# Environments_Model
countEpochs = 30
inputSize = 128  # 64

# Environments_RabbitMQ
queueYoutubeVideoTest = "py_youtube_video_test"
queueFaceFromYoutube = "py_face_from_youtube"
queueFaceFromImage = "py_face_from_image"
queueFaceFromVideo = "py_face_from_video"

# Environments_PostgreSQL
dbName = "face_recognition"
dbUser = "postgres"
dbPass = "180200"
dbHost = "localhost"
dbPort = "5432"

#  P  A  T  H  S  #
pathProject = "D:/Project/Proje-2/Face-Recognition/"
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
pathDatasetsSplit = pathProject + pathMain + "datasets-split/"
pathDatasets = pathProject + pathMain + "datasets/"
pathTrain = pathDatasets + datasetName + "/train/"
pathValidation = pathDatasets + datasetName + "/validation/"
pathTest = pathDatasets + datasetName + "/testScreens/"

# Cascades
pathFaceCascade = pathProject + pathResources + "haarcascade_frontalface_default.xml"
pathEyeCascade = pathProject + pathResources + "haarcascade_eye.xml"

# Utils
pathUtils = pathProject + "utils/"
pathClippedVideos = pathUtils + "clippedVideos/"
pathTempFolder = pathUtils + "tempFolder/"
pathControlFolder = pathUtils + "controlFolder/"
pathNoFace = pathUtils + "NoFace.txt"

# ICONS
pathIcons = pathProject + "src/resources/icons/"
pngAdd = pathIcons + "add.png"
pngCamera = pathIcons + "camera.png"
pngDelete = pathIcons + "delete.png"
pngInfo = pathIcons + "information.png"
pngPicture = pathIcons + "picture.png"
pngTrain = pathIcons + "train.png"
pngUrl = pathIcons + "url.png"
pngYoutube = pathIcons + "youtube.png"
pngMustafa = pathIcons + "mustafa.png"
pngFolder = pathIcons + "folder.png"
pngImageUrl = pathIcons + "imageUrl.png"
pngVideo = pathIcons + "video.png"
pngFaceDetection0 = pathIcons + "faceDetection0.png"
pngFaceDetection1 = pathIcons + "faceDetection1.png"
pngFaceDetection2 = pathIcons + "faceDetection2.png"
pngFaceDetectionYoutube0 = pathIcons + "faceDetectionYoutube0.png"
pngFaceDetectionYoutube1 = pathIcons + "faceDetectionYoutube1.png"
pngInfoBox = pathIcons + "boxInfo.png"
pngWarningBox = pathIcons + "boxWarning.png"
pngErrorBox = pathIcons + "boxError.png"
pngTrash = pathIcons + "trash.png"
pngChecked = pathIcons + "checked.png"
pngUnChecked = pathIcons + "unchecked.png"
