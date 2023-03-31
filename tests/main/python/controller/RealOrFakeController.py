from tests.main.python.services.RealOrFakeService import testImage, trainModel
from tests.resources.Environments import modelName

# trainModel()

testImage("check.jpg", modelName)
testImage("check2.jpg", modelName)
testImage("check3.jpg", modelName)
testImage("check4.jpg", modelName)
