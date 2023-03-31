from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QHBoxLayout

from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngPicture, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube


# Label
def getLabelFeatures(labelName, isUseFont, isUseStyleSheet):
    if isUseFont:
        fontLabel = QtGui.QFont("Times New Roman", 25)
        fontLabel.setBold(True)
        labelName.setFont(fontLabel)
    if isUseStyleSheet:
        labelName.setStyleSheet("border-top: 1px solid black;")
    labelName.setAlignment(QtCore.Qt.AlignCenter)
    return labelName


# Button
def getButtonFeatures(buttonName, pngName):
    butonSizes = (70, 70)
    fontButton = QtGui.QFont("Times New Roman", 15)
    buttonName.setFont(fontButton)
    buttonName.setFixedSize(*butonSizes)
    buttonName.setIcon(QtGui.QIcon(pngName))
    buttonName.setIconSize(QtCore.QSize(*butonSizes))
    buttonName.setStyleSheet("background-color: transparent;")
    return buttonName


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainWith = 500
        mainHeight = 500
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                         mainWith, mainHeight)
        self.setWindowTitle('Yüz Tanıma Projesi created by Mustafa Karakaş')
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon(pngMustafa))

        #########
        # Y Ü Z #
        #########
        faceLabel = getLabelFeatures(QLabel('Yüz'), isUseFont=True, isUseStyleSheet=False)
        # Yüzler için butonlar
        faceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        faceAdd.clicked.connect(self.faceAddScreen)
        faceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        faceDelete.clicked.connect(self.faceDeleteScreen)
        faceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        faceInfo.clicked.connect(self.faceInfoScreen)

        # Yüzler için düzenleyici
        yuzLayout = QHBoxLayout()
        yuzLayout.addWidget(faceAdd)
        yuzLayout.addWidget(faceDelete)
        yuzLayout.addWidget(faceInfo)

        ############
        # M O D E L#
        ############
        # Modeller etiketi
        modelLabel = getLabelFeatures(QLabel('Model'), isUseFont=True, isUseStyleSheet=True)
        # Modeller için butonlar
        modelBtn1 = getButtonFeatures(QPushButton(self), pngTrain)
        modelBtn1.clicked.connect(self.modelTrainScreen)
        modelBtn2 = getButtonFeatures(QPushButton(self), pngDelete)
        modelBtn2.clicked.connect(self.modelDeleteScreen)
        modelBtn3 = getButtonFeatures(QPushButton(self), pngInfo)
        modelBtn3.clicked.connect(self.modelInfoScreen)
        # Modeller için düzenleyici
        modelLayout = QHBoxLayout()
        modelLayout.addWidget(modelBtn1)
        modelLayout.addWidget(modelBtn2)
        modelLayout.addWidget(modelBtn3)

        ###########
        # T E S T #
        ###########
        # Test etiketi
        testLabel = getLabelFeatures(QLabel('Test'), isUseFont=True, isUseStyleSheet=True)
        # Test için butonlar
        testBtn1 = getButtonFeatures(QPushButton(self), pngCamera)
        testBtn1.clicked.connect(self.testCameraScreen)
        testBtn2 = getButtonFeatures(QPushButton(self), pngPicture)
        testBtn2.clicked.connect(self.testImageScreen)
        testBtn3 = getButtonFeatures(QPushButton(self), pngUrl)
        testBtn3.clicked.connect(self.testUrlScreen)
        # Test için düzenleyici
        testLayout = QHBoxLayout()
        testLayout.addWidget(testBtn1)
        testLayout.addWidget(testBtn2)
        testLayout.addWidget(testBtn3)

        # Ana düzenleyici
        layout = QVBoxLayout()
        layout.addWidget(faceLabel)
        layout.addLayout(yuzLayout)
        layout.addWidget(modelLabel)
        layout.addLayout(modelLayout)
        layout.addWidget(testLabel)
        layout.addLayout(testLayout)

        self.setLayout(layout)
        self.show()

    # SCREENS
    def faceAddScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngAdd))

        #############
        # R E S İ M #
        #############
        # Resim etiketi
        imageLabel = getLabelFeatures(QLabel('Resimden'), isUseFont=True, isUseStyleSheet=False)
        # Resim için butonlar
        imageBtn1 = getButtonFeatures(QPushButton(self), pngFolder)
        imageBtn2 = getButtonFeatures(QPushButton(self), pngImageUrl)
        # Resim için düzenleyici
        imageLayout = QHBoxLayout()
        imageLayout.addWidget(imageBtn1)
        imageLayout.addWidget(imageBtn2)

        #############
        # V İ D E O #
        #############
        # Video etiketi
        videoLabel = getLabelFeatures(QLabel('Videodan'), isUseFont=True, isUseStyleSheet=True)
        # Video için butonlar
        videoBtn1 = getButtonFeatures(QPushButton(self), pngCamera)
        videoBtn2 = getButtonFeatures(QPushButton(self), pngYoutube)
        # Video için düzenleyici
        videoLayout = QHBoxLayout()
        videoLayout.addWidget(videoBtn1)
        videoLayout.addWidget(videoBtn2)

        # # Yeni bir etiket ve metin kutusu oluşturuluyor
        # dataName = QLabel('Ad Soyad :', self.window)
        # dataName.move(50, 50)
        # self.textbox = QLineEdit(self.window)
        # self.textbox.move(50, 80)
        #
        # # Yeni bir düğme oluşturuluyor ve tıklama işlemi belirleniyor
        # btn = QPushButton('Ekle', self.window)
        # btn.move(50, 110)
        # btn.clicked.connect(self.runFaceAdd)

        # Ana düzenleyici
        layout = QVBoxLayout()
        layout.addWidget(imageLabel)
        layout.addLayout(imageLayout)
        layout.addWidget(videoLabel)
        layout.addLayout(videoLayout)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceDeleteScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceInfoScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelTrainScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Eğitimi')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngTrain))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelDeleteScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Sil')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngDelete))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def modelInfoScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Model Bilgileri')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngInfo))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testCameraScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Kamera')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngCamera))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testImageScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Resim')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngPicture))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testUrlScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Url')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngUrl))

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    # RUNS
    def runFaceAdd(self):
        print("Yüz Ekle Metodu Çalıştırıldı!")

    def runFaceDelete(self):
        print("Yüz Sil Metodu Çalıştırıldı!")

    def runFaceInfo(self):
        print("Yüz Bilgi Metodu Çalıştırıldı!")

    def runModelTrain(self):
        print("Model Eğitim Metodu Çalıştırıldı!")

    def runModelDelete(self):
        print("Model Sil Metodu Çalıştırıldı!")

    def runModelInfo(self):
        print("Model Bilgi Metodu Çalıştırıldı!")

    def runTestCamera(self):
        print("Test Kamera Metodu Çalıştırıldı!")

    def runTestImage(self):
        print("Test Resim Metodu Çalıştırıldı!")

    def runTestUrl(self):
        print("Test Url Metodu Çalıştırıldı!")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
