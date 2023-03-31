#  E  N  V  S  #

# Environments
datasetName = "RealOrFake"
inputSize = int(128 * 2)
epochSize = 30
batchSize = 64
# For Test
modelName = "RorF_hyuu.h5"

#  P  A  T  H  S  #
pathProject = "C:/Project/Proje-2/face_recognition/"
pathMain = "tests/main/"
pathResources = "tests/resources/"

# Models
pathModels = pathProject + pathMain + "models/"

# Datasets
pathDatasets = pathProject + pathMain + "datasets/"
pathTrain = pathDatasets + datasetName + "/train/"
pathValidation = pathDatasets + datasetName + "/validation/"
pathTest = pathDatasets + datasetName + "/test/"
