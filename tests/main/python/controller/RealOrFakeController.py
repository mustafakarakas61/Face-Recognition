from tests.main.python.services.RealOrFakeService import testImage, trainModel

# trainModel()

modelName = "RorF_qydi.h5"

testImage("check.jpg", modelName)
testImage("check2.jpg", modelName)
testImage("check3.jpg", modelName)
testImage("check4.jpg", modelName)
