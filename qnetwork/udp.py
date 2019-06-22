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

import re
from PyQt4.QtCore import QObject
from PyQt4.QtNetwork import QUdpSocket, QHostAddress, QNetworkInterface


class UdpSocket(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.__socket = QUdpSocket(self)
        self.__socket.readyRead.connect(self.__onReadyRead)

        self.__on_read = None
        self.__port = None

        ips = []  # gel all the local IP-addresses
        addresses = QNetworkInterface.allAddresses()
        for address in addresses:

            match = re.match("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", str(address.toString()))
            if match:
                ip = match.group(0)
                if "127.0.0.1" == ip or "0.0.0.0" == ip:
                    continue

                ips.append(ip)

        self.__ips = ips

    def __onReadyRead(self):
        while self.__socket.hasPendingDatagrams():
            size = self.__socket.pendingDatagramSize()
            data, host, port = self.__socket.readDatagram(size)

            host = str(host.toString())

            if host in self.__ips:  # if the datagram comes from the local IP, we simply ignore it
                return

            source = (host, port)

            if self.__on_read:
                self.__on_read(source, data)

    def __read(self, callback):
        self.__on_read = callback

    def bind(self, port):
        self.__port = port
        self.__socket.bind(self.__port, QUdpSocket.ShareAddress)

    def write(self, data):
        if None == self.__port:
            return -1

        return self.__socket.writeDatagram(data, QHostAddress.Broadcast, self.__port)

    onRead = property(fset=__read)