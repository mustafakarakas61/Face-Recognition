from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QFont, QIntValidator, QIcon
from PyQt5.QtWidgets import QMessageBox

fontTextBox = QtGui.QFont("Times New Roman", 15)


def getLabelFeatures(lbl, isUseFont, isUseSecondFont):
    if isUseFont:
        fontLabel = QtGui.QFont("Times New Roman", 25)
        fontLabel.setBold(True)
        lbl.setFont(fontLabel)
    if isUseSecondFont:
        fontLabel = QtGui.QFont("Times New Roman", 15)
        # fontLabel.setBold(True)
        lbl.setFont(fontLabel)
    lbl.setAlignment(QtCore.Qt.AlignCenter)
    return lbl


def getFaceButtonFeatures(btn, pngName, isVisible):
    butonSizes = (70, 70)
    fontButton = QtGui.QFont("Times New Roman", 15)
    btn.setFont(fontButton)
    btn.setFixedSize(*butonSizes)
    btn.setIcon(QtGui.QIcon(pngName))
    btn.setIconSize(QtCore.QSize(*butonSizes))
    btn.setStyleSheet("background-color: transparent;")
    btn.setVisible(False)
    if isVisible:
        btn.setVisible(True)
    return btn


def getButtonFeatures(btn, pngName):
    butonSizes = (70, 70)
    fontButton = QtGui.QFont("Times New Roman", 15)
    btn.setFont(fontButton)
    btn.setFixedSize(*butonSizes)
    btn.setIcon(QtGui.QIcon(pngName))
    btn.setIconSize(QtCore.QSize(*butonSizes))
    btn.setStyleSheet("background-color: transparent;")
    return btn


def getButtonFeaturesDelete(btn, text):
    butonSizes = (70, 50)
    fontButton = QtGui.QFont("Times New Roman", 15)
    btn.setFont(fontButton)
    btn.setFixedSize(*butonSizes)
    btn.setText(text)
    btn.setIconSize(QtCore.QSize(*butonSizes))
    btn.setStyleSheet("background-color: #DC143C; color: white; border-radius: 5px; font-weight: bold;")
    return btn

def getButtonFeaturesTrain(btn, text):
    butonSizes = (70, 50)
    fontButton = QtGui.QFont("Times New Roman", 15)
    btn.setFont(fontButton)
    btn.setFixedSize(*butonSizes)
    btn.setText(text)
    btn.setIconSize(QtCore.QSize(*butonSizes))
    btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold;")
    return btn


def getComboBoxFeatures(cmbBox):
    fontComboBox = QtGui.QFont("Times New Roman", 15)
    cmbBox.setFont(fontComboBox)
    cmbBox.setStyleSheet("background-color: white; color: black;")
    return cmbBox


def getExceptionMsgBox(msgBox, e):
    font = QFont()
    font.setFamily("Times New Roman")
    font.setPointSize(12)
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(e)
    msgBox.setFont(font)
    msgBox.setWindowTitle("Exception")
    msgBox.setStandardButtons(QMessageBox.Ok)
    return msgBox


def getMsgBoxFeatures(msgBox, windowIconType, title, txt, iconType, btnType, isQuestion):
    font = QFont()
    font.setFamily("Times New Roman")
    font.setPointSize(12)
    msgBox.setWindowIcon(QIcon(windowIconType))
    msgBox.setIcon(iconType)  # QMessageBox.Information
    msgBox.setText(txt)
    msgBox.setFont(font)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(btnType)  # QMessageBox.Ok
    if isQuestion:
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
    return msgBox


def getTextBoxSuccessRateFeatures(textBox, text, isEnabled, isVisible):
    textBox.setFont(fontTextBox)
    textBox.setVisible(False)
    if isVisible:
        textBox.setVisible(True)

    if isEnabled:
        textBox.setFixedSize(30, 30)
        validator = QIntValidator(0, 99)
        textBox.setValidator(validator)
        textBox.setMaxLength(2)
        textBox.setStyleSheet("background-color: white; color: black;")
        textBox.setEnabled(True)
    else:
        textBox.setStyleSheet("background-color: white; color: black;")
        textBox.setEnabled(False)
    textBox.setText(text)
    return textBox
