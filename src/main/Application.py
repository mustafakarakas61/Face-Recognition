import os
import re

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, \
    QMessageBox

from src.main.python.services.DatabaseService import listModels, compareUser, findUser, insertUser, findUserMail, \
    getUserPass, updateUserPass
from src.main.python.services.FeaturesService import getMsgBoxFeatures, getLabelFeatures, \
    getButtonFeatures, getComboBoxFeatures, getTextBoxSuccessRateFeatures, fontTextBox, fontLabel, \
    getButtonFeaturesLogin, getButtonFeaturesForget
from src.main.python.gui.faceScreens.DeleteDataScreen import DeleteFace
from src.main.python.gui.faceScreens.InfoDataScreen import InfoFace
from src.main.python.gui.faceScreens.addDataScreens.CameraScreen import Camera
from src.main.python.gui.faceScreens.addDataScreens.ImageScreen import Image
from src.main.python.gui.faceScreens.addDataScreens.LocalFileScreen import LocalFile
from src.main.python.gui.faceScreens.addDataScreens.NewDatasetDataScreen import NewDatasetData
from src.main.python.gui.faceScreens.addDataScreens.NewDatasetScreen import NewDataset
from src.main.python.gui.faceScreens.addDataScreens.YoutubeScreen import Youtube
from src.main.python.gui.modelScreens.DeleteModelScreen import DeleteModel
from src.main.python.gui.modelScreens.InfoModelScreen import InfoModel
from src.main.python.gui.modelScreens.TrainModelScreen import TrainModel
from src.main.python.gui.testScreens.TestCameraScreen import TestCamera
from src.main.python.gui.testScreens.TestLocalFileScreen import TestLocalFile
from src.main.python.gui.testScreens.webScreens.TestImageScreen import TestImage
from src.main.python.gui.testScreens.webScreens.TestYoutubeScreen import TestYoutube
from src.main.python.services.MailService import newUser, renewPassword, forgetPassword
from src.main.python.services.SecurityService import check_password
from src.resources.Environments import pngAdd, pngDelete, pngInfo, pngTrain, pngCamera, pngUrl, pngMustafa, \
    pngFolder, pngImageUrl, pngYoutube, pathTempFolder, pngInfoBox, pngWarningBox, pathDatasets, pathClippedVideos, \
    pathControlFolder
from utils.Utils import getLine, deleteJpgAndMp4FilesOnFolder, deleteFoldersOnFolder


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # started
        self.closeEvent = None
        self.line_long_security_code = None
        self.controlAcceptLongCodeWindow = None
        self.line_reset_password = None
        self.line_user_username = None
        self.forgetMyPassWindow = None
        self.line_re_new_confirm_password = None
        self.line_re_new_password = None
        self.line_old_password = None
        self.line_renew_username = None
        self.renewPassWindow = None
        self.line_security_code = None
        self.controlAcceptCodeWindow = None
        self.line_new_mail = None
        self.line_new_confirm_password = None
        self.line_new_password = None
        self.line_new_surname = None
        self.line_new_name = None
        self.line_new_username = None
        self.registerWindow = None
        self.id = None
        self.role = None
        self.surname = None
        self.name = None
        self.line_edit_password = None
        self.line_edit_username = None
        self.applicationWindow = None
        self.faceAddWindow = None
        self.comboDatasetsData = None
        self.comboDatasets = None
        self.window = None
        self.selectedDatasetDataName = None
        self.selectedDatasetName = None
        self.comboModel = None
        self.control = False
        self.controlOpenGoogle = True
        self.selectedModel = "Model Seçiniz"
        self.textBoxSuccessRate = getTextBoxSuccessRateFeatures(QLineEdit(self), "90", isEnabled=True, isVisible=False)
        self.isMainScreenClosing = False
        self.isApplicationQuit = False

        # another classes
        # Data
        self.newDatasetWidget = NewDataset(self)
        self.newDatasetDataWidget = NewDatasetData(self)
        self.faceAddLocalFileWidget = LocalFile(self)
        self.faceAddCameraWidget = Camera(self)
        self.faceAddImageWidget = Image(self)
        self.faceAddYoutubeWidget = Youtube(self)
        self.faceDeleteWidget = DeleteFace(self)
        self.faceInfoWidget = InfoFace(self)

        # model
        self.modelTrainWidget = TrainModel(self)
        self.modelDeleteWidget = DeleteModel(self)
        self.modelInfoWidget = InfoModel(self)

        # test
        self.testLocalFileWidget = TestLocalFile(self)
        self.testCameraWidget = TestCamera(self)
        self.testImageWidget = TestImage(self)
        self.testYoutubeWidget = TestYoutube(self)

        # init
        self.initUI()

    def initUI(self):
        mainWidth = 300
        mainHeight = 250
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)), int(screenHeight / 2 - int(mainHeight / 2)),
                         mainWidth, mainHeight)
        self.setWindowIcon(QIcon(pngMustafa))

        label_username = QLabel('Kullanıcı Adı:')
        label_username.setFont(fontLabel)
        self.line_edit_username = QLineEdit()
        self.line_edit_username.setFont(fontLabel)

        label_password = QLabel('Şifre:')
        label_password.setFont(fontLabel)
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setFont(fontLabel)

        button_login: QPushButton = getButtonFeaturesLogin(QPushButton('Giriş Yap'), "#06c267")
        button_login.clicked.connect(self.login)

        button_forget: QPushButton = getButtonFeaturesLogin(QPushButton('Şifre Yenile'), "#eb6631")
        button_forget.clicked.connect(self.renewPasswordScreen)

        button_register: QPushButton = getButtonFeaturesLogin(QPushButton('Kayıt Ol'), "#06b8c2")
        button_register.clicked.connect(self.registerScreen)

        button_test: QPushButton = getButtonFeaturesLogin(QPushButton('Test Ortamı'), "#dbbd58")
        button_test.clicked.connect(self.testEnvironment)

        layout = QVBoxLayout()
        layout.addWidget(label_username)
        layout.addWidget(self.line_edit_username)
        layout.addWidget(label_password)
        layout.addWidget(self.line_edit_password)
        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(button_login)
        layoutH1.addWidget(button_register)
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(button_forget)
        layoutH2.addWidget(button_test)
        layoutH1.setAlignment(button_login, Qt.AlignCenter)
        layoutH1.setAlignment(button_register, Qt.AlignCenter)
        layoutH2.setAlignment(button_forget, Qt.AlignCenter)
        layoutH2.setAlignment(button_test, Qt.AlignCenter)
        layout.addLayout(layoutH1)
        layout.addLayout(layoutH2)

        self.setWindowTitle('Yüz Tanıma Projesi')
        self.setStyleSheet("background-color: white;")
        self.setLayout(layout)
        self.show()
        self.closeEvent = self.closeTopWidgets

    def login(self):
        username: str = self.line_edit_username.text()
        password: str = self.line_edit_password.text()

        if len(username) > 5 and len(password) > 5:
            self.id, self.name, self.surname, self.role = compareUser(username, password)
            if self.id is None or self.name is None or self.surname is None or self.role is None:
                QMessageBox.critical(self, 'Hata', 'Kullanıcı adı veya şifre hatalı.')
            else:
                self.close()
                self.application()
        else:
            if len(username) < 6 and len(password) < 6:
                QMessageBox.critical(self, 'Hata', '<b>Kullanıcı Adı</b> ve <b>Şifre</b> en az 6 karakterli olmalıdır.')
            elif len(username) < 6:
                QMessageBox.critical(self, 'Hata', '<b>Kullanıcı Adı</b> en az 6 karakterli olmalıdır.')
            elif len(password) < 6:
                QMessageBox.critical(self, 'Hata', '<b>Şifre</b> en az 6 karakterli olmalıdır.')
            else:
                QMessageBox.critical(self, 'Hata', 'Geçersiz <b>Kullanıcı Adı</b> ve <b>Şifre</b> formatı.')

    def renewPasswordScreen(self):
        self.renewPassWindow = QWidget()
        mainWidth = 300
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.renewPassWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                         int(screenHeight / 2 - int(mainHeight / 2)),
                                         mainWidth, mainHeight)
        self.renewPassWindow.setWindowIcon(QIcon(pngMustafa))

        label_renew_username = QLabel('Kullanıcı Adı:')
        label_renew_username.setFont(fontLabel)
        self.line_renew_username = QLineEdit()
        self.line_renew_username.setPlaceholderText('Kullanıcı adınızı girin.')
        self.line_renew_username.textChanged.connect(lambda: self.setOldStyle(self.line_renew_username))
        self.line_renew_username.setFont(fontLabel)

        label_oldPassword = QLabel('Eski Şifre:')
        label_oldPassword.setFont(fontLabel)
        self.line_old_password = QLineEdit()
        self.line_old_password.setEchoMode(QLineEdit.Password)
        self.line_old_password.setPlaceholderText('Eski şifrenizi girin.')
        self.line_old_password.textChanged.connect(lambda: self.setOldStyle(self.line_old_password))
        self.line_old_password.setFont(fontLabel)

        label_newPassword = QLabel('Yeni Şifre:')
        label_newPassword.setFont(fontLabel)
        self.line_re_new_password = QLineEdit()
        self.line_re_new_password.setEchoMode(QLineEdit.Password)
        self.line_re_new_password.setPlaceholderText('Yeni şifrenizi girin.')
        self.line_re_new_password.textChanged.connect(lambda: self.setOldStyle(self.line_re_new_password))
        self.line_re_new_password.setFont(fontLabel)

        label_reConfirm_password = QLabel('Yeni Şifreyi Onayla:')
        label_reConfirm_password.setFont(fontLabel)
        self.line_re_new_confirm_password = QLineEdit()
        self.line_re_new_confirm_password.setEchoMode(QLineEdit.Password)
        self.line_re_new_confirm_password.setPlaceholderText('Şifrenizi onaylayın.')
        self.line_re_new_confirm_password.textChanged.connect(
            lambda: self.setOldStyle(self.line_re_new_confirm_password))
        self.line_re_new_confirm_password.setFont(fontLabel)

        button_re_new_password = getButtonFeaturesForget(QPushButton('Şifreyi Yenile'), "#eb6631")
        button_re_new_password.clicked.connect(self.reNewPass)
        button_forget_password = getButtonFeaturesForget(QPushButton('Şifremi Unuttum'), "#d40035")
        button_forget_password.clicked.connect(self.forgetMyPassScreen)

        layout = QVBoxLayout()

        layoutH1 = QHBoxLayout()
        layoutV1_1 = QVBoxLayout()
        layoutV1_2 = QVBoxLayout()

        layoutH2 = QHBoxLayout()
        layoutV2_1 = QVBoxLayout()
        layoutV2_2 = QVBoxLayout()

        layoutV1_1.addWidget(label_renew_username)
        layoutV1_1.setAlignment(label_renew_username, Qt.AlignLeft)
        layoutV1_1.addWidget(self.line_renew_username)
        layoutV1_1.setAlignment(self.line_renew_username, Qt.AlignLeft)
        layoutV1_2.addWidget(label_oldPassword)
        layoutV1_2.setAlignment(label_oldPassword, Qt.AlignLeft)
        layoutV1_2.addWidget(self.line_old_password)
        layoutV1_2.setAlignment(self.line_old_password, Qt.AlignLeft)
        layoutH1.addLayout(layoutV1_1)
        layoutH1.addLayout(layoutV1_2)

        layoutV2_1.addWidget(label_newPassword)
        layoutV2_1.setAlignment(label_newPassword, Qt.AlignLeft)
        layoutV2_1.addWidget(self.line_re_new_password)
        layoutV2_1.setAlignment(self.line_re_new_password, Qt.AlignLeft)
        layoutV2_2.addWidget(label_reConfirm_password)
        layoutV2_2.setAlignment(label_reConfirm_password, Qt.AlignLeft)
        layoutV2_2.addWidget(self.line_re_new_confirm_password)
        layoutV2_2.setAlignment(self.line_re_new_confirm_password, Qt.AlignLeft)
        layoutH2.addLayout(layoutV2_1)
        layoutH2.addLayout(layoutV2_2)

        layout.addLayout(layoutH1)
        layout.addLayout(layoutH2)
        layout.addWidget(button_re_new_password)
        layout.setAlignment(button_re_new_password, Qt.AlignCenter)
        layout.addWidget(button_forget_password)
        layout.setAlignment(button_forget_password, Qt.AlignCenter)

        self.renewPassWindow.setWindowTitle('Şifre Yenile')
        self.renewPassWindow.setStyleSheet("background-color: white;")
        self.renewPassWindow.setLayout(layout)
        self.renewPassWindow.show()

    def registerScreen(self):
        self.registerWindow = QWidget()

        mainWidth = 300
        mainHeight = 250
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.registerWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                        int(screenHeight / 2 - int(mainHeight / 2)),
                                        mainWidth, mainHeight)
        self.registerWindow.setWindowIcon(QIcon(pngMustafa))

        label_username = QLabel('Kullanıcı Adı:')
        label_username.setFont(fontLabel)
        self.line_new_username = QLineEdit()
        self.line_new_username.setPlaceholderText('Kullanıcı adınızı girin.')
        self.line_new_username.textChanged.connect(lambda: self.setOldStyle(self.line_new_username))
        self.line_new_username.setFont(fontLabel)

        label_mail = QLabel('Mail Adresi:')
        label_mail.setFont(fontLabel)
        self.line_new_mail = QLineEdit()
        self.line_new_mail.setPlaceholderText('Mail adresinizi girin.')
        self.line_new_mail.textChanged.connect(self.validate_email)
        self.line_new_mail.setFont(fontLabel)

        label_name = QLabel('Ad:')
        label_name.setFont(fontLabel)
        self.line_new_name = QLineEdit()
        self.line_new_name.setPlaceholderText('Adınızı girin.')
        self.line_new_name.textChanged.connect(lambda: self.setOldStyle(self.line_new_name))
        self.line_new_name.setFont(fontLabel)

        label_surname = QLabel('Soyad:')
        label_surname.setFont(fontLabel)
        self.line_new_surname = QLineEdit()
        self.line_new_surname.setPlaceholderText('Soyadınızı girin.')
        self.line_new_surname.textChanged.connect(lambda: self.setOldStyle(self.line_new_surname))
        self.line_new_surname.setFont(fontLabel)

        label_password = QLabel('Şifre:')
        label_password.setFont(fontLabel)
        self.line_new_password = QLineEdit()
        self.line_new_password.setEchoMode(QLineEdit.Password)
        self.line_new_password.setPlaceholderText('Şifrenizi girin.')
        self.line_new_password.textChanged.connect(lambda: self.setOldStyle(self.line_new_password))
        self.line_new_password.setFont(fontLabel)

        label_confirm_password = QLabel('Şifreyi Onayla:')
        label_confirm_password.setFont(fontLabel)
        self.line_new_confirm_password = QLineEdit()
        self.line_new_confirm_password.setEchoMode(QLineEdit.Password)
        self.line_new_confirm_password.setPlaceholderText('Şifrenizi tekrar girin.')
        self.line_new_confirm_password.textChanged.connect(lambda: self.setOldStyle(self.line_new_confirm_password))
        self.line_new_confirm_password.setFont(fontLabel)

        button_registerScreen = getButtonFeaturesLogin(QPushButton('Kayıt Ol'), "#06b8c2")
        button_registerScreen.clicked.connect(self.register)

        layout = QVBoxLayout()

        layoutH1 = QHBoxLayout()
        layoutV1_1 = QVBoxLayout()
        layoutV1_2 = QVBoxLayout()

        layoutH2 = QHBoxLayout()
        layoutV2_1 = QVBoxLayout()
        layoutV2_2 = QVBoxLayout()

        layoutH3 = QHBoxLayout()
        layoutV3_1 = QVBoxLayout()
        layoutV3_2 = QVBoxLayout()

        layoutV1_1.addWidget(label_username)
        layoutV1_1.setAlignment(label_username, Qt.AlignLeft)
        layoutV1_1.addWidget(self.line_new_username)
        layoutV1_1.setAlignment(self.line_new_username, Qt.AlignLeft)
        layoutV1_2.addWidget(label_mail)
        layoutV1_2.setAlignment(label_mail, Qt.AlignLeft)
        layoutV1_2.addWidget(self.line_new_mail)
        layoutV1_2.setAlignment(self.line_new_mail, Qt.AlignLeft)
        layoutH1.addLayout(layoutV1_1)
        layoutH1.addLayout(layoutV1_2)

        layoutV2_1.addWidget(label_name)
        layoutV2_1.setAlignment(label_name, Qt.AlignLeft)
        layoutV2_1.addWidget(self.line_new_name)
        layoutV2_1.setAlignment(self.line_new_name, Qt.AlignLeft)
        layoutV2_2.addWidget(label_surname)
        layoutV2_2.setAlignment(label_surname, Qt.AlignLeft)
        layoutV2_2.addWidget(self.line_new_surname)
        layoutV2_2.setAlignment(self.line_new_surname, Qt.AlignLeft)
        layoutH2.addLayout(layoutV2_1)
        layoutH2.addLayout(layoutV2_2)

        layoutV3_1.addWidget(label_password)
        layoutV3_1.setAlignment(label_password, Qt.AlignLeft)
        layoutV3_1.addWidget(self.line_new_password)
        layoutV3_1.setAlignment(self.line_new_password, Qt.AlignLeft)
        layoutV3_2.addWidget(label_confirm_password)
        layoutV3_2.setAlignment(label_confirm_password, Qt.AlignLeft)
        layoutV3_2.addWidget(self.line_new_confirm_password)
        layoutV3_2.setAlignment(self.line_new_confirm_password, Qt.AlignLeft)
        layoutH3.addLayout(layoutV3_1)
        layoutH3.addLayout(layoutV3_2)

        layout.addLayout(layoutH1)
        layout.addLayout(layoutH2)
        layout.addLayout(layoutH3)
        layout.addWidget(button_registerScreen)
        layout.setAlignment(button_registerScreen, Qt.AlignCenter)

        self.registerWindow.setWindowTitle('Kayıt Ol')
        self.registerWindow.setStyleSheet("background-color: white;")
        self.registerWindow.setLayout(layout)
        self.registerWindow.show()

    def reNewPass(self):
        username: str = self.line_renew_username.text()
        old_password: str = self.line_old_password.text()
        new_password: str = self.line_re_new_password.text()
        confirm_new_password: str = self.line_re_new_confirm_password.text()

        if username == '' or old_password == '' or new_password == '' or confirm_new_password == '':
            QMessageBox.critical(self.registerWindow, 'Hata', 'Tüm bilgileri doldurunuz.')
            if username == '':
                self.line_renew_username.setStyleSheet('QLineEdit { background-color: red; }')
            if old_password == '':
                self.line_old_password.setStyleSheet('QLineEdit { background-color: red; }')
            if new_password == '':
                self.line_re_new_password.setStyleSheet('QLineEdit { background-color: red; }')
            if confirm_new_password == '':
                self.line_re_new_confirm_password.setStyleSheet('QLineEdit { background-color: red; }')
        else:
            if len(username) < 6 or len(old_password) < 6 or len(new_password) < 6:
                QMessageBox.critical(self.renewPassWindow, 'Hata',
                                     '<b>Kullanıcı Adı</b> ve <b>Şifre</b> en az 6 karakterli olmalıdır.')
                if len(username) < 6:
                    self.line_renew_username.setStyleSheet('QLineEdit { background-color: red; }')
                if len(old_password) < 6:
                    self.line_old_password.setStyleSheet('QLineEdit { background-color: red; }')
                if len(new_password) < 6:
                    self.line_re_new_password.setStyleSheet('QLineEdit { background-color: red; }')
            elif new_password != confirm_new_password:
                QMessageBox.critical(self.renewPassWindow, 'Hata', '<b>Yeni Şifreler</b> eşleşmiyor.')
            else:
                user_id, hashed_password, user_mail, user_name, user_surname, user_role = getUserPass(username)
                if user_id is None:
                    QMessageBox.warning(self.renewPassWindow, 'Uyarı', '<b>Kullanıcı Adı</b> bulunamadı.')
                    self.line_renew_username.setStyleSheet('QLineEdit { background-color: orange; }')
                else:
                    if not check_password(old_password, hashed_password):
                        QMessageBox.critical(self.renewPassWindow, 'Hata', '<b>Eski Şifreniz</b> uyuşmuyor.')
                    else:
                        if old_password == new_password:
                            QMessageBox.critical(self.renewPassWindow, 'Uyarı',
                                                 'Yeni şifreniz eski şifrenizden farklı olmalıdır.')
                        else:
                            controlCode = renewPassword(username)
                            if controlCode is not None:
                                QMessageBox.information(self.renewPassWindow, 'Bilgi',
                                                        'Mail adresinize gelen kodu giriniz.')
                                self.controlAcceptCodeScreen(controlCode, None, username, new_password, None, None)

                            else:
                                QMessageBox.critical(self.registerWindow, 'Hata', 'Bir hata oluştu.')

    def forgetMyPassScreen(self):
        self.forgetMyPassWindow = QWidget()
        mainWidth = 250
        mainHeight = 100
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.forgetMyPassWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                            int(screenHeight / 2 - int(mainHeight / 2)),
                                            mainWidth, mainHeight)
        self.forgetMyPassWindow.setWindowIcon(QIcon(pngMustafa))

        self.line_user_username = QLineEdit()
        self.line_user_username.setPlaceholderText('Kullanıcı adınızı girin.')
        self.line_user_username.textChanged.connect(lambda: self.setOldStyle(self.line_user_username))
        self.line_user_username.setFont(fontLabel)

        button_reset_password = getButtonFeaturesForget(QPushButton('Şifremi Sıfırla'), "#5c7578")
        button_reset_password.clicked.connect(self.resetPass)

        layout = QVBoxLayout()
        layout.addWidget(self.line_user_username)
        layout.setAlignment(self.line_user_username, Qt.AlignCenter)
        layout.addWidget(button_reset_password)
        layout.setAlignment(button_reset_password, Qt.AlignCenter)

        self.forgetMyPassWindow.setWindowTitle('Şifre Sıfırla')
        self.forgetMyPassWindow.setStyleSheet("background-color: white;")
        self.forgetMyPassWindow.setLayout(layout)
        self.forgetMyPassWindow.show()

    def resetPass(self):
        username: str = self.line_user_username.text()
        if username == '':
            QMessageBox.critical(self.forgetMyPassWindow, 'Uyarı', 'Kullanıcı adınızı giriniz.')
        else:
            if len(username) < 6:
                self.line_new_username.setStyleSheet('QLineEdit { background-color: red; }')
            else:
                user_id, user_mail, user_name, user_surname, user_role = findUser(username)
                if user_id is None:
                    QMessageBox.critical(self.forgetMyPassWindow, 'Uyarı', '<b>Kullanıcı Adı</b> sistemde bulunamadı.')
                else:
                    longControlCode = forgetPassword(username)
                    if longControlCode is not None:
                        QMessageBox.information(self.forgetMyPassWindow, 'Bilgi',
                                                'Mail adresinize gelen kodu giriniz.')
                        self.controlAcceptLongCodeScreen(longControlCode, username)

                    else:
                        QMessageBox.critical(self.forgetMyPassWindow, 'Hata', 'Bir hata oluştu.')

    def register(self):
        username: str = self.line_new_username.text()
        mail: str = self.line_new_mail.text()
        name: str = self.line_new_name.text()
        surname: str = self.line_new_surname.text()
        password: str = self.line_new_password.text()
        confirm_password: str = self.line_new_confirm_password.text()

        if username == '' or mail == '' or name == '' or surname == '' or password == '' or confirm_password == '':
            QMessageBox.critical(self.registerWindow, 'Hata', 'Tüm bilgileri doldurunuz.')
            if username == '':
                self.line_new_username.setStyleSheet('QLineEdit { background-color: red; }')
            if mail == '':
                self.line_new_mail.setStyleSheet('QLineEdit { background-color: red; }')
            if name == '':
                self.line_new_name.setStyleSheet('QLineEdit { background-color: red; }')
            if surname == '':
                self.line_new_surname.setStyleSheet('QLineEdit { background-color: red; }')
            if password == '':
                self.line_new_password.setStyleSheet('QLineEdit { background-color: red; }')
            if confirm_password == '':
                self.line_new_confirm_password.setStyleSheet('QLineEdit { background-color: red; }')
        else:
            if len(username) < 6 or len(password) < 6:
                QMessageBox.critical(self.registerWindow, 'Hata',
                                     '<b>Kullanıcı Adı</b> ve <b>Şifre</b> en az 6 karakterli olmalıdır.')
                if len(username) < 6:
                    self.line_new_username.setStyleSheet('QLineEdit { background-color: red; }')
                if len(password) < 6:
                    self.line_new_password.setStyleSheet('QLineEdit { background-color: red; }')
            elif password != confirm_password:
                QMessageBox.critical(self.registerWindow, 'Hata', '<b>Şifreler</b> eşleşmiyor.')
            else:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                is_valid = re.match(email_pattern, mail) is not None
                if is_valid:
                    user_id, user_mail, user_name, user_surname, user_role = findUser(username)
                    if user_id is not None:
                        QMessageBox.critical(self.registerWindow, 'Uyarı', 'Bu <b>Kullanıcı Adı</b> sistemde mevcut.')
                        self.line_new_username.setStyleSheet('QLineEdit { background-color: orange; }')
                    else:
                        userMail_id, userMail_mail, userMail_name, userMail_surname, userMail_role = findUserMail(mail)
                        if userMail_id is not None:
                            QMessageBox.critical(self.registerWindow, 'Uyarı', 'Bu <b>Mail Adresi</b> sistemde mevcut.')
                            self.line_new_mail.setStyleSheet('QLineEdit { background-color: orange; }')
                        else:
                            controlCode = newUser(username, mail, name, surname)
                            if controlCode is not None:
                                QMessageBox.information(self.registerWindow, 'Bilgi',
                                                        'Mail adresinize gelen kodu giriniz.')
                                self.controlAcceptCodeScreen(controlCode, mail, username, password, name, surname)

                            else:
                                QMessageBox.critical(self.registerWindow, 'Hata', 'Bir hata oluştu.')
                else:
                    QMessageBox.critical(self.registerWindow, 'Hata', 'Geçerli bir <b>mail</b> adresi giriniz.')
                    self.line_new_mail.setStyleSheet('QLineEdit { background-color: red; }')

    def testEnvironment(self):
        QMessageBox.information(self, 'Test Ortamı', 'Kayıt olmadan sadece test denemesi yapabilirsiniz.')
        self.close()
        self.application()

    def application(self):
        self.applicationWindow = QWidget()
        mainWidth = 500
        mainHeight = 500
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.applicationWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                           int(screenHeight / 2 - int(mainHeight / 2)),
                                           mainWidth, mainHeight)
        if self.role is None:
            self.applicationWindow.setWindowTitle('Test Ortamı')
        else:
            self.applicationWindow.setWindowTitle(
                'Hoşgeldiniz ' + self.name + " " + self.surname + " [" + (
                    "Standard Kullanıcı" if self.role.__eq__("USER") else self.role) + "]")
        self.applicationWindow.setStyleSheet("background-color: white;")
        self.applicationWindow.setWindowIcon(QIcon(pngMustafa))

        ###########
        # D A T A #
        ###########
        labelFace = getLabelFeatures(QLabel('Veri'), isUseFont=True, isUseSecondFont=False)
        btnFaceAdd = getButtonFeatures(QPushButton(self), pngAdd)
        btnFaceAdd.clicked.connect(self.faceAddScreen)
        btnFaceDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnFaceDelete.clicked.connect(self.faceDeleteWidget.faceDeleteScreen)
        btnFaceInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnFaceInfo.clicked.connect(self.faceInfoWidget.faceInfoScreen)
        layoutFace = QHBoxLayout()
        layoutFace.addWidget(btnFaceAdd)
        layoutFace.addWidget(btnFaceDelete)
        layoutFace.addWidget(btnFaceInfo)

        ############
        # M O D E L#
        ############
        labelModel = getLabelFeatures(QLabel('Model'), isUseFont=True, isUseSecondFont=False)
        btnModelTrain = getButtonFeatures(QPushButton(self), pngTrain)
        btnModelTrain.clicked.connect(self.modelTrainWidget.modelTrainScreen)
        btnModelDelete = getButtonFeatures(QPushButton(self), pngDelete)
        btnModelDelete.clicked.connect(self.modelDeleteWidget.modelDeleteScreen)
        btnModelInfo = getButtonFeatures(QPushButton(self), pngInfo)
        btnModelInfo.clicked.connect(self.modelInfoWidget.modelInfoScreen)
        layoutModel = QHBoxLayout()
        layoutModel.addWidget(btnModelTrain)
        layoutModel.addWidget(btnModelDelete)
        layoutModel.addWidget(btnModelInfo)

        ###########
        # T E S T #
        ###########
        labelTest = getLabelFeatures(QLabel('Test'), isUseFont=True, isUseSecondFont=False)

        self.comboModel = getComboBoxFeatures(QComboBox(self))
        self.updateModelList()
        self.comboModel.currentIndexChanged.connect(
            lambda index: self.onComboboxSelection(self.comboModel.itemText(index)))
        btnTestCamera = getButtonFeatures(QPushButton(self), pngCamera)
        btnTestCamera.clicked.connect(self.testCameraWidget.testCameraScreen)
        btnTestLocal = getButtonFeatures(QPushButton(self), pngFolder)
        btnTestLocal.clicked.connect(self.testLocalFileWidget.testLocalFileScreen)
        btnTestUrl = getButtonFeatures(QPushButton(self), pngUrl)
        btnTestUrl.clicked.connect(self.testUrlScreen)
        layoutTest = QHBoxLayout()
        layoutTest.addWidget(btnTestCamera)
        layoutTest.addWidget(btnTestLocal)
        layoutTest.addWidget(btnTestUrl)

        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutV.addWidget(labelFace)
        layoutV.addLayout(layoutFace)
        layoutV.addWidget(getLine())
        layoutV.addWidget(labelModel)
        layoutV.addLayout(layoutModel)
        layoutV.addWidget(getLine())
        layoutV.addWidget(labelTest)
        self.textBoxSuccessRate.setVisible(True)
        layoutH.addWidget(self.textBoxSuccessRate)
        labelSuccessRate = QLineEdit()
        labelSuccessRate.setText("% Başarı Oranı")
        labelSuccessRate.setEnabled(False)
        labelSuccessRate.setFont(fontTextBox)
        labelSuccessRate.setStyleSheet("background-color: white; color: black;")

        labelSuccessRate.setAlignment(Qt.AlignLeft)
        layoutH.addWidget(labelSuccessRate)
        layoutV.addWidget(self.comboModel)
        layoutV.addLayout(layoutH)
        layoutV.addLayout(layoutTest)
        self.applicationWindow.setLayout(layoutV)
        self.applicationWindow.show()
        self.applicationWindow.closeEvent = self.closeApplicationEvent

    # Main Screens
    def faceAddScreen(self):
        if not self.getIsMainScreenClosing():
            if self.role is not None:
                mainWidth = 330
                mainHeight = 420
                screen = QtWidgets.QApplication.desktop().screenGeometry()
                screenWidth, screenHeight = screen.width(), screen.height()

                self.faceAddWindow = QWidget()
                self.faceAddWindow.setWindowTitle('Yüz Verisi Ekle')
                self.faceAddWindow.setStyleSheet("background-color: white;")
                self.faceAddWindow.setWindowIcon(QIcon(pngAdd))

                #############
                #  D A T A  #
                #############
                # Combobox
                labelDataset: QLabel = getLabelFeatures(QLabel("<b>Veriseti:</b>"), False, True)
                self.comboDatasets: QComboBox = getComboBoxFeatures(QComboBox(self))
                self.comboDatasets.setFixedSize(150, 30)
                self.updateDatasetList()

                self.comboDatasetsData: QComboBox = getComboBoxFeatures(QComboBox(self))
                self.comboDatasetsData.setFixedSize(150, 30)
                self.comboDatasets.currentIndexChanged.connect(
                    lambda index: self.onComboDatasetsSelection(self.comboDatasets.itemText(index),
                                                                self.comboDatasetsData))

                layoutHDataset = QHBoxLayout()
                layoutHDataset.addWidget(labelDataset, alignment=Qt.AlignLeft)
                layoutHDataset.addWidget(self.comboDatasets, alignment=Qt.AlignRight)

                labelDatasetData: QLabel = getLabelFeatures(QLabel("<b>Veri:</b>"), False, True)
                layoutHDatasetData = QHBoxLayout()
                layoutHDatasetData.addWidget(labelDatasetData, alignment=Qt.AlignLeft)
                layoutHDatasetData.addWidget(self.comboDatasetsData, alignment=Qt.AlignRight)

                layoutHNew = QHBoxLayout()
                # Button
                fontButton = QtGui.QFont("Times New Roman", 15)
                buttonSizes = (150, 50)

                btnNewDataset = QPushButton(self)
                btnNewDataset.setText("Veriseti Oluştur")
                btnNewDataset.setFont(fontButton)
                btnNewDataset.setFixedSize(*buttonSizes)
                btnNewDataset.setStyleSheet(
                    "background-color: gray; color: white; border-radius: 5px; font-weight: bold;")
                btnNewDataset.clicked.connect(self.newDatasetWidget.newDatasetScreen)
                layoutHNew.addWidget(btnNewDataset)

                btnNewDatasetData = QPushButton(self)
                btnNewDatasetData.setText("Veri Oluştur")
                btnNewDatasetData.setFont(fontButton)
                btnNewDatasetData.setFixedSize(*buttonSizes)
                btnNewDatasetData.setStyleSheet(
                    "background-color: gray; color: white; border-radius: 5px; font-weight: bold;")
                btnNewDatasetData.clicked.connect(
                    lambda: self.newDatasetDataWidget.newDatasetDataScreen() if not str(
                        self.selectedDatasetName).__eq__(
                        "Veriseti Seçiniz") and self.selectedDatasetName is not None else getMsgBoxFeatures(
                        QMessageBox(), pngWarningBox, "Uyarı", "Lütfen bir <b>veriseti</b> seçin.",
                        QMessageBox.Warning,
                        QMessageBox.Ok, isQuestion=False).exec_())
                layoutHNew.addWidget(btnNewDatasetData)

                #############
                # Y E R E L #
                #############
                labelLocal = getLabelFeatures(QLabel('Yerel'), isUseFont=True, isUseSecondFont=False)
                btnVideoCamera = getButtonFeatures(QPushButton(self), pngCamera)
                btnVideoCamera.clicked.connect(self.faceAddCameraWidget.faceAddVideoCameraScreen)
                btnLocalFile = getButtonFeatures(QPushButton(self), pngFolder)
                btnLocalFile.clicked.connect(self.faceAddLocalFileWidget.faceAddLocalFileScreen)
                layoutLocal = QHBoxLayout()
                layoutLocal.addWidget(btnVideoCamera)
                layoutLocal.addWidget(btnLocalFile)

                #########
                # W E B #
                #########
                labelWeb = getLabelFeatures(QLabel('Web'), isUseFont=True, isUseSecondFont=False)
                btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
                btnImageUrl.clicked.connect(self.faceAddImageWidget.faceAddImageUrlScreen)
                btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
                btnVideoYoutube.clicked.connect(self.faceAddYoutubeWidget.faceAddVideoYoutubeScreen)
                layoutWeb = QHBoxLayout()
                layoutWeb.addWidget(btnImageUrl)
                layoutWeb.addWidget(btnVideoYoutube)

                layout = QVBoxLayout()

                layoutV = QVBoxLayout()
                layoutV.addLayout(layoutHDataset)
                layoutV.addLayout(layoutHDatasetData)

                layoutV.addLayout(layoutHNew)

                layout.addLayout(layoutV)
                layout.addWidget(getLine())
                layout.addWidget(labelLocal)
                layout.addLayout(layoutLocal)
                layout.addWidget(getLine())
                layout.addWidget(labelWeb)
                layout.addLayout(layoutWeb)

                self.faceAddWindow.setLayout(layout)
                self.faceAddWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                               int(screenHeight / 2 - int(mainHeight / 2)),
                                               mainWidth, mainHeight)
                self.faceAddWindow.setAttribute(Qt.WA_DeleteOnClose)
                self.faceAddWindow.closeEvent = self.onClosedFaceAddScreen
                self.faceAddWindow.show()
            else:
                QMessageBox.critical(self.applicationWindow, 'Dikkat', 'Bu işlem için lütfen kayıt olunuz.')

    def testUrlScreen(self):
        if not self.getIsMainScreenClosing():
            modelName = self.selectedModel
            sRate = self.textBoxSuccessRate.text()
            if str(sRate).__len__() == 0:
                sRate = "0"
            rateLimit = 35
            if modelName.__eq__("Model Seçiniz") or int(sRate) < int(rateLimit):
                if modelName.__eq__("Model Seçiniz"):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı", "Lütfen bir model seçin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
                if int(sRate) < int(rateLimit):
                    getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Uyarı",
                                      "Lütfen " + str(rateLimit) + "'in üstünde tanımlı bir değer girin.",
                                      QMessageBox.Warning,
                                      QMessageBox.Ok, isQuestion=False).exec_()
            else:
                mainWidth = 300
                mainHeight = 150
                screen = QtWidgets.QApplication.desktop().screenGeometry()
                screenWidth, screenHeight = screen.width(), screen.height()

                self.TestWindow = QWidget()
                self.TestWindow.setWindowTitle('Test Web')
                self.TestWindow.setStyleSheet("background-color: white;")
                self.TestWindow.setWindowIcon(QIcon(pngUrl))

                #############
                # R E S İ M #
                #############
                btnImageUrl = getButtonFeatures(QPushButton(self), pngImageUrl)
                btnImageUrl.clicked.connect(self.testImageWidget.testUrlImageScreen)
                layoutImage = QHBoxLayout()
                layoutImage.addWidget(btnImageUrl)

                #################
                # Y O U T U B E #
                #################
                btnVideoYoutube = getButtonFeatures(QPushButton(self), pngYoutube)
                btnVideoYoutube.clicked.connect(self.testYoutubeWidget.testUrlYoutubeScreen)
                layoutYoutube = QHBoxLayout()
                layoutYoutube.addWidget(btnVideoYoutube)

                # Ana düzenleyici
                layout = QHBoxLayout()
                layout.addLayout(layoutImage)
                layout.addLayout(layoutYoutube)

                self.TestWindow.setLayout(layout)
                self.TestWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                            int(screenHeight / 2 - int(mainHeight / 2)),
                                            mainWidth, mainHeight)
                self.TestWindow.setObjectName("testUrlScreen")
                self.TestWindow.show()

    def closeTopWidgets(self, event):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            widget.close()
        event.accept()

    def closeApplicationEvent(self, event):
        if not self.isApplicationQuit:
            reply = getMsgBoxFeatures(QMessageBox(self), pngWarningBox, "Dikkat!", 'Programdan çıkmak istiyor musun?',
                                      QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                      isQuestion=True).exec_()

            if reply == QtWidgets.QMessageBox.Yes:
                self.setIsMainScreenClosing(True)
                for widget in QtWidgets.QApplication.topLevelWidgets():
                    widget.close()
                deleteJpgAndMp4FilesOnFolder(pathClippedVideos)
                deleteJpgAndMp4FilesOnFolder(pathControlFolder)
                deleteJpgAndMp4FilesOnFolder(pathTempFolder)
                deleteFoldersOnFolder(pathTempFolder)

                event.accept()
                MainWidget()
                self.isApplicationQuit = True
            else:
                event.ignore()

    def controlAcceptCodeScreen(self, securityCode, mail, username, password, name, surname):
        self.controlAcceptCodeWindow = QWidget()
        mainWidth = 200
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.controlAcceptCodeWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                               int(screenHeight / 2 - int(mainHeight / 2)),
                                               mainWidth, mainHeight)

        self.controlAcceptCodeWindow.setWindowTitle(
            'Güvenlik Kodu')
        self.controlAcceptCodeWindow.setStyleSheet("background-color: white;")
        self.controlAcceptCodeWindow.setWindowIcon(QIcon(pngMustafa))

        self.line_security_code = QLineEdit()
        self.line_security_code.setPlaceholderText('Güvenlik kodunu girin.')
        self.line_security_code.setFont(fontLabel)

        button_Accept = getButtonFeaturesLogin(QPushButton('Onayla'), "#6bf2d0")
        if mail is not None and name is not None and surname is not None:
            button_Accept.clicked.connect(
                lambda: self.acceptRegister(securityCode, mail, username, password, name, surname))
        else:
            button_Accept.clicked.connect(
                lambda: self.acceptReNewPass(securityCode, username, password))

        layout = QVBoxLayout()
        layout.addWidget(self.line_security_code)
        layout.addWidget(button_Accept)
        layout.setAlignment(self.line_security_code, Qt.AlignCenter)
        layout.setAlignment(button_Accept, Qt.AlignCenter)
        self.controlAcceptCodeWindow.setLayout(layout)
        self.controlAcceptCodeWindow.show()

    def controlAcceptLongCodeScreen(self, longControlCode, username):
        self.controlAcceptLongCodeWindow = QWidget()
        mainWidth = 200
        mainHeight = 150
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screenWidth, screenHeight = screen.width(), screen.height()
        self.controlAcceptLongCodeWindow.setGeometry(int(screenWidth / 2 - int(mainWidth / 2)),
                                                     int(screenHeight / 2 - int(mainHeight / 2)),
                                                     mainWidth, mainHeight)

        self.controlAcceptLongCodeWindow.setWindowTitle(
            'Şifre Sıfırla')
        self.controlAcceptLongCodeWindow.setStyleSheet("background-color: white;")
        self.controlAcceptLongCodeWindow.setWindowIcon(QIcon(pngMustafa))

        label_reset_password = QLabel('Yeni Şifre:')
        label_reset_password.setFont(fontLabel)
        self.line_reset_password = QLineEdit()
        self.line_reset_password.setPlaceholderText('Yeni şifrenizi girin.')
        self.line_reset_password.setEchoMode(QLineEdit.Password)
        self.line_reset_password.setFont(fontLabel)

        label_long_security_code = QLabel('Güvenlik Kodu:')
        label_long_security_code.setFont(fontLabel)
        self.line_long_security_code = QLineEdit()
        self.line_long_security_code.setPlaceholderText('Güvenlik kodunu girin.')
        self.line_long_security_code.setFont(fontLabel)

        button_reset_Accept = getButtonFeaturesLogin(QPushButton('Onayla'), "#6bf2d0")

        button_reset_Accept.clicked.connect(
            lambda: self.acceptResetPass(longControlCode, username))

        layout = QVBoxLayout()
        layout.addWidget(label_reset_password)
        layout.addWidget(self.line_reset_password)
        layout.addWidget(label_long_security_code)
        layout.addWidget(self.line_long_security_code)
        layout.addWidget(button_reset_Accept)

        # layout.setAlignment(self.line_long_security_code, Qt.AlignCenter)
        layout.setAlignment(button_reset_Accept, Qt.AlignCenter)
        self.controlAcceptLongCodeWindow.setLayout(layout)
        self.controlAcceptLongCodeWindow.show()

    def acceptRegister(self, security: str, mail: str, username: str, password: str, name: str, surname: str):
        if str(security) == str(self.line_security_code.text()):
            lastId = insertUser(username, password, name, surname, mail)
            QMessageBox.information(self.controlAcceptCodeWindow, 'Bilgi', 'Kayıt işlemi başarılı.')
            self.controlAcceptCodeWindow.close()
            self.registerWindow.close()
        else:
            QMessageBox.critical(self.controlAcceptCodeWindow, 'Hata', 'Girdiğiniz kod geçersiz.')

    def acceptResetPass(self, security: str, username: str):
        if str(security) == str(self.line_long_security_code.text()):
            if len(self.line_reset_password.text()) > 5:
                lastId = updateUserPass(username, self.line_reset_password.text())
                QMessageBox.information(self.controlAcceptLongCodeWindow, 'Bilgi', 'Şifreniz başarıyla güncellendi.')
                self.controlAcceptLongCodeWindow.close()
                self.renewPassWindow.close()
            else:
                QMessageBox.warning(self.controlAcceptLongCodeWindow, 'Uyarı',
                                    '<b>Yeni şifreniz</b> en az 6 karakter uzunluğunda olmalıdır.')
        else:
            QMessageBox.critical(self.controlAcceptLongCodeWindow, 'Hata', 'Girdiğiniz kod geçersiz.')

    def acceptReNewPass(self, security: str, username: str, password: str):
        if str(security) == str(self.line_security_code.text()):
            lastId = updateUserPass(username, password)
            QMessageBox.information(self.controlAcceptCodeWindow, 'Bilgi', 'Şifreniz başarıyla güncellendi.')
            self.controlAcceptCodeWindow.close()
            self.renewPassWindow.close()
        else:
            QMessageBox.critical(self.controlAcceptCodeWindow, 'Hata', 'Girdiğiniz kod geçersiz.')

    def onClosedFaceAddScreen(self, event):
        if not self.getIsMainScreenClosing():
            if self.selectedDatasetName is not None or self.selectedDatasetDataName is not None:
                reply = getMsgBoxFeatures(QMessageBox(), pngWarningBox, "Dikkat!",
                                          'Veri Ekle ekranından çıkış yapılsın mı?',
                                          QMessageBox.Question, (QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                          isQuestion=True).exec_()
                if reply == QtWidgets.QMessageBox.Yes:
                    self.selectedDatasetName = None
                    self.selectedDatasetDataName = None
                    if self.newDatasetWidget and self.newDatasetWidget.window and self.newDatasetWidget.window.isVisible():
                        self.newDatasetWidget.window.close()
                    if self.newDatasetDataWidget and self.newDatasetDataWidget.window and self.newDatasetDataWidget.window.isVisible():
                        self.newDatasetDataWidget.window.close()
                    event.accept()
                else:
                    event.ignore()
            self.closeSubScreens()

    def closeSubScreens(self):
        if self.faceAddCameraWidget is not None:
            self.faceAddCameraWidget.closeScreen()

        if self.faceAddLocalFileWidget is not None:
            self.faceAddLocalFileWidget.closeScreen()

        if self.faceAddImageWidget is not None:
            self.faceAddImageWidget.closeScreen()

        if self.faceAddYoutubeWidget is not None:
            self.faceAddYoutubeWidget.closeScreen()

    def updateDatasetList(self):
        if self.comboDatasets is not None:
            datasetFolders = [f for f in os.listdir(pathDatasets) if os.path.isdir(os.path.join(pathDatasets, f))]
            datasetNames = ['Veriseti Seçiniz'] + datasetFolders
            self.comboDatasets.clear()
            self.comboDatasets.addItems(datasetNames)

    def updateModelList(self):
        if self.comboModel is not None:
            models = listModels()
            modelNames = ["Model Seçiniz"] + [model["model_name"] for model in models]
            self.comboModel.clear()
            self.comboModel.addItems(modelNames)

    def showWarn(self):
        getMsgBoxFeatures(QMessageBox(self), pngInfoBox, "Kullanılacak Model ve Başarı Oranı",
                          self.selectedModel + "\nBaşarı oranı " + str(
                              self.textBoxSuccessRate.text()) + " olarak belirlenmiştir.",
                          QMessageBox.Information, QMessageBox.Ok, isQuestion=False).exec_()

    def getIsMainScreenClosing(self):
        return self.isMainScreenClosing

    def setIsMainScreenClosing(self, value):
        self.isMainScreenClosing = value

    def onComboboxSelection(self, newName):
        self.selectedModel = newName

    def onComboDatasetsSelection(self, newName, comboDatasetsData: QComboBox):
        self.selectedDatasetName = newName
        if self.selectedDatasetName is not None and len(
                self.selectedDatasetName) > 0 and not self.selectedDatasetName.__eq__("Veriseti Seçiniz"):
            datasetDataFolders = [f for f in os.listdir(pathDatasets + self.selectedDatasetName) if
                                  os.path.isdir(os.path.join(pathDatasets + self.selectedDatasetName, f))]
            datasetDataNames = ['Veri Seçiniz'] + datasetDataFolders
            comboDatasetsData.clear()
            comboDatasetsData.addItems(datasetDataNames)
            comboDatasetsData.currentIndexChanged.connect(
                lambda index: self.onComboDatasetsDataSelection(comboDatasetsData.itemText(index)))
        else:
            comboDatasetsData.clear()

    def onComboDatasetsDataSelection(self, newName):
        self.selectedDatasetDataName = newName

    def validate_email(self, text):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(email_pattern, text) is not None

        if is_valid:
            self.line_new_mail.setStyleSheet('QLineEdit { color: green; }')
        else:
            self.line_new_mail.setStyleSheet('QLineEdit { color: red; }')

    def setOldStyle(self, param):
        param.setStyleSheet('')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec_())
