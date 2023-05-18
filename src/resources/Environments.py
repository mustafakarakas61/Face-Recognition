#  E  N  V  S  #
# Environments
minFaceSize = 128
inputSize = 128  # 64

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

# Cascades
pathFaceCascade = pathProject + pathResources + "haarcascade_frontalface_default.xml"
pathEyeCascade = pathProject + pathResources + "haarcascade_eye.xml"

# Utils
pathUtils = pathProject + "utils/"
pathClippedVideos = pathUtils + "clippedVideos/"
pathTempFolder = pathUtils + "tempFolder/"
pathControlFolder = pathUtils + "controlFolder/"
pathNoFace = pathUtils + "NoFace.txt"


#  I  C  O  N  S  #
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
pngMainGraphic = pathIcons + "mainGraphic.png"
pngGraphic = pathIcons + "graphic.png"
pngSaved = pathIcons + "saved.png"
pngSaveImage0 = pathIcons + "saveImage0.png"
pngSaveImage1 = pathIcons + "saveImage1.png"
pngSaveYoutubeImage0 = pathIcons + "saveYoutubeImage0.png"
pngSaveYoutubeImage1 = pathIcons + "saveYoutubeImage1.png"
pngClearText = pathIcons + "clearText.png"
pngDeleteImage0 = pathIcons + "deleteImage0.png"
pngDeleteImage1 = pathIcons + "deleteImage1.png"
