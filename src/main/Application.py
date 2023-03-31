import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QHBoxLayout, QComboBox, \
    QMessageBox, QFrame

from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube, pngPicture, pathModels


def getLine():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet("background-color: black;")
    return line


# Label
def getLabelFeatures(lbl, isUseFont):
    if isUseFont:
        fontLabel = QtGui.QFont("Times New Roman", 25)
        fontLabel.setBold(True)
        lbl.setFont(fontLabel)
    lbl.setAlignment(QtCore.Qt.AlignCenter)
    return lbl


# Button
def getButtonFeatures(btn, pngName):
    butonSizes = (70, 70)
    fontButton = QtGui.QFont("Times New Roman", 15)
    btn.setFont(fontButton)
    btn.setFixedSize(*butonSizes)
    btn.setIcon(QtGui.QIcon(pngName))
    btn.setIconSize(QtCore.QSize(*butonSizes))
    btn.setStyleSheet("background-color: transparent;")
    return btn


# ComboBox
def getComboBoxFeatures(cmbBox):
    fontComboBox = QtGui.QFont("Times New Roman", 15)
    cmbBox.setFont(fontComboBox)
    cmbBox.setStyleSheet("background-color: black; color: white;")
    return cmbBox


def getMsgBoxFeatures(msgBox, title, txt, iconType, btnType):
    font = QFont()
    font.setFamily("Times New Roman")
    font.setPointSize(12)
    msgBox.setIcon(iconType)  # QMessageBox.Information
    msgBox.setText(txt)
    msgBox.setFont(font)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(btnType)  # QMessageBox.Ok
    return msgBox


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.selectedModel = "Model Seçiniz"
        self.initUI()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Uyarı', 'Programdan çıkmak istiyor musunuz?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for widget in QtWidgets.QApplication.topLevelWidgets():
                widget.close()
            event.accept()
        else:
            event.ignore()

    def initUI(self):
        mainWith = 500
        mainHeight = 450
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
        labelFace = getLabelFeatures(QLabel('Yüz'), isUseFont=True)
        # Yüzler için butonlar
        btnFaceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        btnFaceAdd.clicked.connect(self.faceAddScreen)
        btnFaceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnFaceDelete.clicked.connect(self.faceDeleteScreen)
        btnFaceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnFaceInfo.clicked.connect(self.faceInfoScreen)

        # Yüzler için düzenleyici
        layoutFace = QHBoxLayout()
        layoutFace.addWidget(btnFaceAdd)
        layoutFace.addWidget(btnFaceDelete)
        layoutFace.addWidget(btnFaceInfo)

        ############
        # M O D E L#
        ############
        # Modeller etiketi
        labelModel = getLabelFeatures(QLabel('Model'), isUseFont=True)
        # Modeller için butonlar
        btnModelTrain = getButtonFeatures(QPushButton(self), pngTrain)
        btnModelTrain.clicked.connect(self.modelTrainScreen)
        btnModelDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnModelDelete.clicked.connect(self.modelDeleteScreen)
        btnModelInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnModelInfo.clicked.connect(self.modelInfoScreen)
        # Modeller için düzenleyici
        layoutModel = QHBoxLayout()
        layoutModel.addWidget(btnModelTrain)
        layoutModel.addWidget(btnModelDelete)
        layoutModel.addWidget(btnModelInfo)

        ###########
        # T E S T #
        ###########
        # Test etiketi
        labelTest = getLabelFeatures(QLabel('Test'), isUseFont=True)

        # ComboBox ayarı
        # Dizin içindeki .h5 uzantılı dosyaları bulma
        modelFiles = [f for f in os.listdir(pathModels) if f.endswith('.h5')]
        # Dosya isimlerinden model adlarını ayırma
        modelNames = ['Model Seçiniz'] + [os.path.splitext(f)[0] + ".h5" for f in modelFiles]
        # ComboBox oluşturma ve model isimlerini ekleme
        comboModel = getComboBoxFeatures(QComboBox(self))
        comboModel.addItems(modelNames)

        # Seçili olan modelin adını alma
        def on_combobox_selection(modelName):
            self.selectedModel = modelName

        comboModel.currentIndexChanged.connect(lambda index: on_combobox_selection(comboModel.itemText(index)))

        # Test için butonlar
        btnTestCamera = getButtonFeatures(QPushButton(self), pngCamera)
        btnTestCamera.clicked.connect(self.testCameraScreen)
        btnTestPicture = getButtonFeatures(QPushButton(self), pngPicture)
        btnTestPicture.clicked.connect(self.testImageScreen)
        btnTestUrl = getButtonFeatures(QPushButton(self), pngUrl)
        btnTestUrl.clicked.connect(self.testUrlScreen)
        # Test için düzenleyici
        layoutTest = QHBoxLayout()

        # Düzenleyiciye ekleme
        layoutTest.addWidget(btnTestCamera)
        layoutTest.addWidget(btnTestPicture)
        layoutTest.addWidget(btnTestUrl)

        # Ana düzenleyici
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        layoutV.addWidget(labelFace)
        layoutV.addLayout(layoutFace)
        layoutV.addWidget(getLine())
        layoutV.addWidget(labelModel)
        layoutV.addLayout(layoutModel)
        layoutH.addWidget(labelTest)
        layoutV.addWidget(getLine())
        layoutH.addWidget(comboModel)
        layoutV.addLayout(layoutH)
        layoutV.addLayout(layoutTest)
        self.setLayout(layoutV)
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
        labelImage = getLabelFeatures(QLabel('Resimden'), isUseFont=True)
        # Resim için butonlar
        btnImageFolder = getButtonFeatures(QPushButton(self), pngFolder)
        btnImageFolder.clicked.connect(self.faceAddImageFolderScreen)
        btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
        btnImageUrl.clicked.connect(self.faceAddImageUrlScreen)
        # Resim için düzenleyici
        layoutImage = QHBoxLayout()
        layoutImage.addWidget(btnImageFolder)
        layoutImage.addWidget(btnImageUrl)

        #############
        # V İ D E O #
        #############
        # Video etiketi
        labelVideo = getLabelFeatures(QLabel('Videodan'), isUseFont=True)
        # Video için butonlar
        btnVideoCamera = getButtonFeatures(QPushButton(self), pngCamera)
        btnVideoCamera.clicked.connect(self.faceAddVideoCameraScreen)
        btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
        btnVideoYoutube.clicked.connect(self.faceAddVideoYoutubeScreen)
        # Video için düzenleyici
        layoutVideo = QHBoxLayout()
        layoutVideo.addWidget(btnVideoCamera)
        layoutVideo.addWidget(btnVideoYoutube)

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
        layout.addWidget(labelImage)
        layout.addLayout(layoutImage)
        layout.addWidget(getLine())
        layout.addWidget(labelVideo)
        layout.addLayout(layoutVideo)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddImageFolderScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yerelden Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngFolder))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddImageUrlScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('URL\'den Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngImageUrl))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddVideoCameraScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Kameradan Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngCamera))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def faceAddVideoYoutubeScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Youtube\'dan Ekle')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngYoutube))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.faceAddScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

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
        modelName = self.selectedModel
        # Model seçilmemişse uyarı verme
        if modelName == 'Model Seçiniz':
            getMsgBoxFeatures(QMessageBox(self), "Uyarı", "Lütfen bir model seçin", QMessageBox.Warning,
                              QMessageBox.Ok).exec_()
        else:
            # Mesaj kutusunu gösterme
            getMsgBoxFeatures(QMessageBox(self), "Kullanılacak Model", modelName,
                              QMessageBox.Information, QMessageBox.Ok).exec_()
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
            self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)),
                                    int(screenHeight / 2 - int(mainHeight / 2)),
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
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Url')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngUrl))

        #############
        # R E S İ M #
        #############
        btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
        btnImageUrl.clicked.connect(self.testUrlImageScreen)
        layoutImage = QHBoxLayout()
        layoutImage.addWidget(btnImageUrl)

        #################
        # Y O U T U B E #
        #################
        btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
        btnVideoYoutube.clicked.connect(self.testUrlYoutubeScreen)
        layoutYoutube = QHBoxLayout()
        layoutYoutube.addWidget(btnVideoYoutube)

        # Ana düzenleyici
        layout = QHBoxLayout()
        layout.addLayout(layoutImage)
        layout.addLayout(layoutYoutube)

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testUrlImageScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Url')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngImageUrl))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.testUrlScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def testUrlYoutubeScreen(self):
        mainWith = 300
        mainHeight = 300
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Test Youtube')
        self.window.setStyleSheet("background-color: white;")
        self.window.setWindowIcon(QIcon(pngYoutube))

        # Çarpı işaretine basıldığında eski pencere açılsın
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.destroyed.connect(self.testUrlScreen)

        # Ana düzenleyici
        layout = QVBoxLayout()

        self.window.setLayout(layout)
        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    # RUNS
    def runFaceAdd(self):
        print("Yüz Ekle Metodu Çalıştırıldı!")

    def runFaceAddImageFolder(self):
        print("Yerelden Yüz Ekle Metodu Çalıştırıldı!")

    def runFaceAddImageUrl(self):
        print("Url'den Yüz Ekle Metodu Çalıştırıldı!")

    def runFaceAddVideoCamera(self):
        print("Kameradan Yüz Ekle Metodu Çalıştırıldı!")

    def runFaceAddVideoYoutube(self):
        print("Youtube'dan Yüz Ekle Metodu Çalıştırıldı!")

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

    def runTestUrlImage(self):
        print("Test Url Resim Metodu Çalıştırıldı!")

    def runTestUrlYoutube(self):
        print("Test Url Youtube Metodu Çalıştırıldı!")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
