from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QHBoxLayout

from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngPicture, pngUrl, pngMustafa


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        butonSizes = (70, 70)
        mainWith = 500
        mainHeight = 500
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                         mainWith, mainHeight)
        self.setWindowTitle('Yüz Tanıma Projesi created by Mustafa Karakaş')
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon(pngMustafa))

        # Label
        fontLabel = QtGui.QFont("Times New Roman", 25)
        fontLabel.setBold(True)
        labelStyleSheet = "border-top: 1px solid black;"

        # Button
        def getButton(buttonName, pngName):
            fontButton = QtGui.QFont("Times New Roman", 15)
            buttonName.setFont(fontButton)
            buttonName.setFixedSize(*butonSizes)
            buttonName.setIcon(QtGui.QIcon(pngName))
            buttonName.setIconSize(QtCore.QSize(*butonSizes))
            buttonName.setStyleSheet("background-color: transparent;")
            return buttonName

        #
        # Y Ü Z
        #
        faceLabel = QLabel('Yüz')
        faceLabel.setFont(fontLabel)
        # yuzLabel.setStyleSheet(labelStyleSheet)
        faceLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Yüzler için butonlar
        faceAdd = QPushButton(self)
        faceAdd = getButton(faceAdd, pngAdd)
        faceAdd.clicked.connect(self.yuz_tanima)

        faceDelete = QPushButton(self)
        faceDelete = getButton(faceDelete, pngDelete)

        faceInfo = QPushButton(self)
        faceInfo = getButton(faceInfo, pngInfo)

        # Yüzler için düzenleyici
        yuzLayout = QHBoxLayout()
        yuzLayout.addWidget(faceAdd)
        yuzLayout.addWidget(faceDelete)
        yuzLayout.addWidget(faceInfo)

        #
        # M O D E L
        #

        # Modeller etiketi
        modelLabel = QLabel('Model')
        modelLabel.setFont(fontLabel)
        modelLabel.setStyleSheet(labelStyleSheet)
        modelLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Modeller için butonlar
        modelBtn1 = QPushButton(self)
        modelBtn1 = getButton(modelBtn1, pngTrain)

        modelBtn2 = QPushButton(self)
        modelBtn2 = getButton(modelBtn2, pngDelete)

        modelBtn3 = QPushButton(self)
        modelBtn3 = getButton(modelBtn3, pngInfo)

        # Modeller için düzenleyici
        modelLayout = QHBoxLayout()
        modelLayout.addWidget(modelBtn1)
        modelLayout.addWidget(modelBtn2)
        modelLayout.addWidget(modelBtn3)

        #
        # T E S T
        #

        # Test etiketi
        testLabel = QLabel('Test')
        testLabel.setFont(fontLabel)
        testLabel.setStyleSheet(labelStyleSheet)
        testLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Test için butonlar
        testBtn1 = QPushButton(self)
        testBtn1 = getButton(testBtn1, pngCamera)

        testBtn2 = QPushButton(self)
        testBtn2 = getButton(testBtn2, pngPicture)

        testBtn3 = QPushButton(self)
        testBtn3 = getButton(testBtn3, pngUrl)

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

    def yuz_tanima(self):
        mainWith = 250
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()

        self.window = QWidget()
        self.window.setWindowTitle('Yüz Tanıma')

        # Yeni bir etiket ve metin kutusu oluşturuluyor
        label = QLabel('Yüz Tanıma Metodu', self.window)
        label.move(50, 50)
        self.textbox = QLineEdit(self.window)
        self.textbox.move(50, 80)

        # Yeni bir düğme oluşturuluyor ve tıklama işlemi belirleniyor
        btn = QPushButton('Metodu Çalıştır', self.window)
        btn.move(50, 110)
        btn.clicked.connect(self.run_yuz_tanima)

        self.window.setGeometry(int(screenWidth / 2 - int(mainWith / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                                mainWith, mainHeight)
        self.window.show()

    def run_yuz_tanima(self):
        # Burada yüz tanıma metodunu çalıştıracak kodlarınızı yazabilirsiniz
        print("Yüz Tanıma Metodu Çalıştırıldı!")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
