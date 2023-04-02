from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox


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


def getMsgBoxFeatures(msgBox, title, txt, iconType, btnType, isQuestion):
    font = QFont()
    font.setFamily("Times New Roman")
    font.setPointSize(12)
    msgBox.setIcon(iconType)  # QMessageBox.Information
    msgBox.setText(txt)
    msgBox.setFont(font)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(btnType)  # QMessageBox.Ok
    if isQuestion:
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
    return msgBox


def getTextBoxFeatures(textBox, text, isVisible):
    fontTextBox = QtGui.QFont("Times New Roman", 15)
    textBox.setFont(fontTextBox)
    textBox.setText(text)
    textBox.setVisible(False)
    if isVisible:
        textBox.setVisible(True)
    return textBox


def getTextBoxSuccessRateFeatures(textBox, text, isEnabled, isVisible):
    fontTextBox = QtGui.QFont("Times New Roman", 15)
    textBox.setFont(fontTextBox)
    textBox.setVisible(False)
    if isVisible:
        textBox.setVisible(True)

    if isEnabled:
        textBox.setFixedSize(30, 30)
        textBox.setMaxLength(2)
        textBox.setStyleSheet("background-color: white; color: black;")
        textBox.setEnabled(True)
    else:
        textBox.setStyleSheet("background-color: white; color: black;")
        textBox.setEnabled(False)
    textBox.setText(text)
    return textBox
