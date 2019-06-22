# -*- coding: utf-8 -*-

# Copyright (C) 2015-2019 Alexey Naumov <rocketbuzzz@gmail.com>
#
# This file is part of qnetwork.
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
import re
from distutils.util import strtobool

from PyQt5.QtCore import Qt, QTime, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWidgets import QDialog

from qnetwork.tcp import TcpServer
from qnetwork.utils import History, bytesToString, stringToBytes
from debuggers.tcp.server.ui_Dialog import Ui_Dialog

ICON_SERVER = os.path.dirname(__file__) + "/icons/server.svg"


class TcpServerDebugger(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.__initialize()

    def __initialize(self):
        self.setWindowIcon(QIcon(ICON_SERVER))

        self.__tcpServer = TcpServer()
        self.__tcpServer.onConnected = self.onConnected
        self.__tcpServer.onDisconnected = self.onDisconnected
        self.__tcpServer.onError = self.onError
        self.__tcpServer.onRead = self.onRead

        self.pushButtonStartStop.clicked.connect(self.onPushButtonStartStopClicked)
        self.pushButtonSend.clicked.connect(self.onPushButtonSendClicked)
        self.checkBoxRawText.stateChanged.connect(self.onCheckBoxRawTextStateChanged)
        self.listWidgetClients.itemClicked.connect(self.onListWidgetClientsItemClicked)
        self.lineEditData.keyPressed.connect(self.__onKeyPressed)

        self.__history = History()
        self.__loadSettings()

    def __onKeyPressed(self, key):
        if key in [Qt.Key_Enter, Qt.Key_Return]:
            self.onPushButtonSendClicked()

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
        settings = QSettings("Rocket Labs", "tcp-server-debugger")
        settings.setValue("port", self.spinBoxPort.value())
        settings.setValue("format", self.comboBoxFormat.currentIndex())
        settings.setValue("leadingZeroes", self.checkBoxLeadingZeroes.isChecked())
        settings.setValue("timestamp", self.checkBoxTimestamp.isChecked())
        settings.setValue("rawText", self.checkBoxRawText.isChecked())

    def __loadSettings(self):
        settings = QSettings("Rocket Labs", "tcp-server-debugger")
        self.spinBoxPort.setValue(int(settings.value("port", 80)))
        self.comboBoxFormat.setCurrentIndex(int(settings.value("format", 0)))
        self.checkBoxLeadingZeroes.setChecked(strtobool(settings.value("leadingZeroes", "False")))
        self.checkBoxTimestamp.setChecked(strtobool(settings.value("timestamp", "False")))
        self.checkBoxRawText.setChecked(strtobool(settings.value("rawText", "False")))

    def closeEvent(self, event):
        self.__tcpServer.close()
        self.__saveSettings()
        super(TcpServerDebugger, self).closeEvent(event)

    def onConnected(self, descriptor):
        self.listWidgetClients.addItem(str(descriptor))

    def onDisconnected(self, descriptor):
        searchString = str(descriptor)
        matchFlags = Qt.MatchExactly
        items = self.listWidgetClients.findItems(searchString, matchFlags)

        if not items:
            self.__postText("E[?]: Disconnected descriptor was not found.")

        for item in items:
            row = self.listWidgetClients.row(item)
            self.listWidgetClients.takeItem(row)

    def onError(self, descriptor, error):
        self.__postText("E[%s#%s]: %s." % (error[0], descriptor, error[1]))

    def onRead(self, descriptor, data):
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

        self.__postText("R[%s:%s#%s]: %s" % (dataFormat, len(data), descriptor, text))

    def onCheckBoxRawTextStateChanged(self, state):
        if state == Qt.Checked:
            self.labelFormat.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)
            self.checkBoxLeadingZeroes.setEnabled(False)
        else:
            self.labelFormat.setEnabled(True)
            self.comboBoxFormat.setEnabled(True)
            self.checkBoxLeadingZeroes.setEnabled(True)

    def onListWidgetClientsItemClicked(self):
        item = self.listWidgetClients.currentItem()
        descriptor = int(item.text())
        socket = self.__tcpServer.socket(descriptor)

        if socket:
            raw = str(socket.peerAddress().toString())
            match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", raw)
            if match:
                address = match.group()
                self.lineEditPeerAddress.setText(address)

    def onPushButtonStartStopClicked(self):
        if self.__tcpServer.isListening():
            self.__tcpServer.close()
            self.pushButtonStartStop.setText("Start")
            self.textEditTraffic.setEnabled(False)
            self.lineEditData.setEnabled(False)
            self.pushButtonSend.setEnabled(False)
            self.listWidgetClients.clear()
        else:
            port = self.spinBoxPort.value()
            self.__tcpServer.listen(QHostAddress.Any, port)
            self.pushButtonStartStop.setText("Stop")
            self.textEditTraffic.setEnabled(True)
            self.lineEditData.setEnabled(True)
            self.pushButtonSend.setEnabled(True)

    def onPushButtonSendClicked(self):
        selectedSockets = self.listWidgetClients.selectedItems()
        if 0 == len(selectedSockets):
            self.__postText("E[?#?]: No socket(s) selected.")
            return

        text = self.lineEditData.text().strip()
        if not text:
            self.__postText("E[?]: No input provided.")
            return

        self.__history.add(text)

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

        for item in selectedSockets:
            descriptor = int(item.text())
            self.__postText("T[%s:%s#%s]: %s" % (dataFormat, len(data), descriptor, text))
            self.__tcpServer.write(descriptor, data)

        self.lineEditData.clear()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QDialog, QApplication

    application = QApplication(sys.argv)

    server = TcpServerDebugger()
    server.show()

    sys.exit(application.exec_())