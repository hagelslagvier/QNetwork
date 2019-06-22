# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 600)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEditTraffic = QtWidgets.QTextEdit(Dialog)
        self.textEditTraffic.setEnabled(False)
        self.textEditTraffic.setObjectName("textEditTraffic")
        self.verticalLayout_2.addWidget(self.textEditTraffic)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditData = LineEdit(Dialog)
        self.lineEditData.setEnabled(False)
        self.lineEditData.setObjectName("lineEditData")
        self.horizontalLayout.addWidget(self.lineEditData)
        self.pushButtonSend = QtWidgets.QPushButton(Dialog)
        self.pushButtonSend.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonSend.setFont(font)
        self.pushButtonSend.setAutoDefault(False)
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.horizontalLayout.addWidget(self.pushButtonSend)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 11, 1)
        self.labelHost = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelHost.setFont(font)
        self.labelHost.setObjectName("labelHost")
        self.gridLayout.addWidget(self.labelHost, 0, 1, 1, 1)
        self.lineEditHost = QtWidgets.QLineEdit(Dialog)
        self.lineEditHost.setMinimumSize(QtCore.QSize(160, 0))
        self.lineEditHost.setMaximumSize(QtCore.QSize(160, 16777215))
        self.lineEditHost.setObjectName("lineEditHost")
        self.gridLayout.addWidget(self.lineEditHost, 1, 1, 1, 1)
        self.labelPort = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelPort.setFont(font)
        self.labelPort.setObjectName("labelPort")
        self.gridLayout.addWidget(self.labelPort, 2, 1, 1, 1)
        self.spinBoxPort = QtWidgets.QSpinBox(Dialog)
        self.spinBoxPort.setMinimumSize(QtCore.QSize(160, 0))
        self.spinBoxPort.setMaximumSize(QtCore.QSize(160, 16777215))
        self.spinBoxPort.setMinimum(1)
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setProperty("value", 80)
        self.spinBoxPort.setObjectName("spinBoxPort")
        self.gridLayout.addWidget(self.spinBoxPort, 3, 1, 1, 1)
        self.pushButtonConnectDisconnect = QtWidgets.QPushButton(Dialog)
        self.pushButtonConnectDisconnect.setMinimumSize(QtCore.QSize(160, 0))
        self.pushButtonConnectDisconnect.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonConnectDisconnect.setFont(font)
        self.pushButtonConnectDisconnect.setAutoDefault(False)
        self.pushButtonConnectDisconnect.setFlat(False)
        self.pushButtonConnectDisconnect.setObjectName("pushButtonConnectDisconnect")
        self.gridLayout.addWidget(self.pushButtonConnectDisconnect, 4, 1, 1, 1)
        self.labelFormat = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelFormat.setFont(font)
        self.labelFormat.setObjectName("labelFormat")
        self.gridLayout.addWidget(self.labelFormat, 5, 1, 1, 1)
        self.comboBoxFormat = QtWidgets.QComboBox(Dialog)
        self.comboBoxFormat.setMinimumSize(QtCore.QSize(160, 0))
        self.comboBoxFormat.setMaximumSize(QtCore.QSize(160, 16777215))
        self.comboBoxFormat.setObjectName("comboBoxFormat")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.gridLayout.addWidget(self.comboBoxFormat, 6, 1, 1, 1)
        self.checkBoxLeadingZeroes = QtWidgets.QCheckBox(Dialog)
        self.checkBoxLeadingZeroes.setObjectName("checkBoxLeadingZeroes")
        self.gridLayout.addWidget(self.checkBoxLeadingZeroes, 7, 1, 1, 1)
        self.checkBoxRawText = QtWidgets.QCheckBox(Dialog)
        self.checkBoxRawText.setObjectName("checkBoxRawText")
        self.gridLayout.addWidget(self.checkBoxRawText, 8, 1, 1, 1)
        self.checkBoxTimestamp = QtWidgets.QCheckBox(Dialog)
        self.checkBoxTimestamp.setObjectName("checkBoxTimestamp")
        self.gridLayout.addWidget(self.checkBoxTimestamp, 9, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(17, 237, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.comboBoxFormat.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditHost, self.spinBoxPort)
        Dialog.setTabOrder(self.spinBoxPort, self.pushButtonConnectDisconnect)
        Dialog.setTabOrder(self.pushButtonConnectDisconnect, self.lineEditData)
        Dialog.setTabOrder(self.lineEditData, self.pushButtonSend)
        Dialog.setTabOrder(self.pushButtonSend, self.comboBoxFormat)
        Dialog.setTabOrder(self.comboBoxFormat, self.checkBoxTimestamp)
        Dialog.setTabOrder(self.checkBoxTimestamp, self.textEditTraffic)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TCP debugger (client) - 1.1.1"))
        self.pushButtonSend.setText(_translate("Dialog", "Send"))
        self.labelHost.setText(_translate("Dialog", "Host:"))
        self.lineEditHost.setText(_translate("Dialog", "localhost"))
        self.labelPort.setText(_translate("Dialog", "Port:"))
        self.pushButtonConnectDisconnect.setText(_translate("Dialog", "Connect"))
        self.labelFormat.setText(_translate("Dialog", "Format:"))
        self.comboBoxFormat.setItemText(0, _translate("Dialog", "Bin"))
        self.comboBoxFormat.setItemText(1, _translate("Dialog", "Oct"))
        self.comboBoxFormat.setItemText(2, _translate("Dialog", "Dec"))
        self.comboBoxFormat.setItemText(3, _translate("Dialog", "Hex"))
        self.checkBoxLeadingZeroes.setText(_translate("Dialog", "Leading zeroes"))
        self.checkBoxRawText.setText(_translate("Dialog", "Raw text"))
        self.checkBoxTimestamp.setText(_translate("Dialog", "Timestamp"))


from debuggers.widgets import LineEdit
