# -*- coding: utf-8 -*-

# Copyright (C) 2015-2019 Alexey Naumov <rocketbuzzz@gmail.com>
#
#
# qnetwork is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.util import strtobool

from PyQt5.QtCore import QTime, QSettings, QByteArray, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QDialog

from qnetwork.tcp import TcpClient
from qnetwork.utils import History, bytesToString, stringToBytes
from debuggers.tcp.client.ui_Dialog import Ui_Dialog

ICON_CLIENT = os.path.dirname(__file__) + "/icons/client.svg"


class TcpClientDebugger(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.__initialize()

    def __initialize(self):
        self.setWindowIcon(QIcon(ICON_CLIENT))

        self.__tcpClient = TcpClient()
        self.__tcpClient.onConnected = self.onConnected
        self.__tcpClient.onDisconnected = self.onDisconnected
        self.__tcpClient.onError = self.onError
        self.__tcpClient.onRead = self.onRead

        self.pushButtonConnectDisconnect.clicked.connect(self.onPushButtonConnectDisconnectClicked)
        self.pushButtonSend.clicked.connect(self.onPushButtonSendClicked)
        self.checkBoxRawText.stateChanged.connect(self.onCheckBoxRawTextStateChanged)
        self.lineEditData.keyPressed.connect(self.__keyPressed)

        self.__history = History()
        self.__loadSettings()

    def __keyPressed(self, key):
        if key in [Qt.Key_Enter, Qt.Key_Return]:
            self.pushButtonSend.click()

        if Qt.Key_Up == key:
            previous = self.__history.previous()
            if previous:
                self.lineEditData.setText(previous)

        if Qt.Key_Down == key:
            next = self.__history.next()
            if next:
                self.lineEditData.setText(next)

    def __postText(self, text):
        if self.checkBoxTimestamp.isChecked():
            time = QTime.currentTime().toString()
            self.textEditTraffic.append("%s - %s" % (time, text))
        else:
            self.textEditTraffic.append(text)

    def __saveSettings(self):
        settings = QSettings("Rocket Labs", "tcp-client-debugger")
        settings.setValue("host", self.lineEditHost.text())
        settings.setValue("port", self.spinBoxPort.value())
        settings.setValue("format", self.comboBoxFormat.currentIndex())
        settings.setValue("leadingZeroes", self.checkBoxLeadingZeroes.isChecked())
        settings.setValue("timestamp", self.checkBoxTimestamp.isChecked())
        settings.setValue("rawText", self.checkBoxRawText.isChecked())

    def __loadSettings(self):
        settings = QSettings("Rocket Labs", "tcp-client-debugger")
        self.lineEditHost.setText(str(settings.value("host", "localhost")))
        self.spinBoxPort.setValue(int(settings.value("port", 80)))
        self.comboBoxFormat.setCurrentIndex(int(settings.value("format", 0)))
        self.checkBoxLeadingZeroes.setChecked(strtobool(settings.value("leadingZeroes", "False")))
        self.checkBoxTimestamp.setChecked(strtobool(settings.value("timestamp", "False")))
        self.checkBoxRawText.setChecked(strtobool(settings.value("rawText", "False")))

    def closeEvent(self, event):
        self.__tcpClient.close()
        self.__saveSettings()
        super(TcpClientDebugger, self).closeEvent(event)

    def onConnected(self):
        self.textEditTraffic.setEnabled(True)
        self.lineEditData.setEnabled(True)
        self.pushButtonSend.setEnabled(True)
        self.pushButtonConnectDisconnect.setText("Disconnect")

    def onDisconnected(self):
        self.textEditTraffic.setEnabled(False)
        self.lineEditData.setEnabled(False)
        self.pushButtonSend.setEnabled(False)
        self.pushButtonConnectDisconnect.setText("Connect")

    def onError(self, error):
        self.__postText("E: [%s] %s." % (error[0], error[1]))

    def onRead(self, data):
        if self.checkBoxRawText.isChecked():
            dataFormat = "S"
            text = bytes(data).decode("utf-8")

        else:
            INDEX_BASE = {0: 2, 1: 8, 2: 10, 3: 16}
            index = self.comboBoxFormat.currentIndex()
            base = INDEX_BASE.get(index, None)
            if not base:
                self.__postText("E[?]: Invalid base of a number.")

            data = list(data)
            text = bytesToString(data, base, self.checkBoxLeadingZeroes.isChecked())

            INDEX_FORMAT = {0: "B", 1: "O", 2: "D", 3: "H"}
            dataFormat = INDEX_FORMAT.get(index, None)
            if not dataFormat:
                self.__postText("E[?]: Invalid data format.")

        self.__postText("R[%s:%s]: %s" % (dataFormat, len(data), text))

    def onCheckBoxRawTextStateChanged(self, state):
        if state == Qt.Checked:
            self.labelFormat.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)
            self.checkBoxLeadingZeroes.setEnabled(False)
        else:
            self.labelFormat.setEnabled(True)
            self.comboBoxFormat.setEnabled(True)
            self.checkBoxLeadingZeroes.setEnabled(True)

    def onPushButtonConnectDisconnectClicked(self):
        state = self.__tcpClient.state()
        if QTcpSocket.ConnectedState == state:
            self.__tcpClient.disconnectFromHost()
        elif QTcpSocket.UnconnectedState == state:
            host = self.lineEditHost.text()
            port = self.spinBoxPort.value()
            self.__tcpClient.connectToHost(host, port)

    def onPushButtonSendClicked(self):
        text = self.lineEditData.text().strip()

        if not text:
            self.__postText("E[?]: No input provided.")
            return

        if self.checkBoxRawText.isChecked():
            data = str(text).encode("utf-8")
            dataFormat = "S"

        else:
            INDEX_BASE = {0: 2, 1: 8, 2: 10, 3: 16}
            index = self.comboBoxFormat.currentIndex()
            base = INDEX_BASE.get(index, None)
            if not base:
                self.__postText("E[?]: Invalid base of a number.")

            try:
                values = stringToBytes(str(text), base)
            except ValueError as error:
                self.__postText("E[?]: Incorrect input: <%s>." % str(error).capitalize())
                return

            data = bytes(values)

            text = bytesToString(values, base, self.checkBoxLeadingZeroes.isChecked())

            INDEX_FORMAT = {0: "B", 1: "O", 2: "D", 3: "H"}
            dataFormat = INDEX_FORMAT.get(index, None)
            if not dataFormat:
                self.__postText("E[?]: Invalid data format.")

        self.__history.add(self.lineEditData.text())
        self.__postText("T[%s:%s]: %s" % (dataFormat, len(data), text))
        self.__tcpClient.write(data)
        self.lineEditData.clear()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QDialog

    application = QApplication(sys.argv)

    debugger = TcpClientDebugger()
    debugger.show()

    sys.exit(application.exec_())

