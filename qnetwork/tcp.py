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

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtNetwork import QTcpSocket, QTcpServer, QAbstractSocket


class TcpClient(QObject):
    '''
    TCP/IP client class.

    Usage:
        import sys
        import tcp
        from PyQt4.QtCore import QCoreApplication
        from PyQt4.QtNetwork.QAbstractSocket import QAbstractSocket


        def main():
            application = QCoreApplication(sys.argv)

            def onConnected():
                print("Connected")

            def onDisconnected():
                print("Disconnected")

            def onError(error):
                print("Error: ", error)
                if error[0] == QAbstractSocket.ConnectionRefusedError:  # if connection refused
                    sys.exit(1)  # close the program

            def onRead(data):
                print("Read %s byte(s): %s" % (len(data), data))

            tcpClient = tcp.TcpClient()
            tcpClient.onConnected = onConnected
            tcpClient.onDisconnected = onDisconnected
            tcpClient.onError = onError
            tcpClient.onRead = onRead

            tcpClient.connectToHost("localhost", 9000)
            tcpClient.write("Hello there")

            sys.exit(application.exec_())

        if __name__ == "__main__":
            main()
    '''

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.__socket = QTcpSocket(parent)

        # Callbacks
        self.__on_connected = None
        self.__on_disconnected = None
        self.__on_error = None
        self.__on_read = None

        # Signals and slots connections
        self.__socket.connected.connect(self.__onConnected)
        self.__socket.disconnected.connect(self.__onDisconnected)
        self.__socket.error.connect(self.__onError)
        self.__socket.readyRead.connect(self.__onReadyRead)

    # Slots
    @pyqtSlot()
    def __onConnected(self):
        '''
        The slot is called when a connection to the specified host has been successfully established. Then,
        __on_connected callback is executed.
        :return: None
        '''

        if self.__on_connected:
            self.__on_connected()

    @pyqtSlot()
    def __onDisconnected(self):
        '''
        The slot is called when the connection to the host is closed. Then, __on_disconnected callback is executed.
        :return: None
        '''

        if self.__on_disconnected:
            self.__on_disconnected()

    def __onError(self, socketError):
        '''
        The slot is called when an error(PyQt4.QtNetwork.SocketError) <socketError> occurs. Then, error code(int)
        <errorCode> and error description(str) <errorDescription> are defined and passed to __on_error callback.
        :param error(PyQt4.QtNetwork.SocketError): error code;
        :return: None
        '''

        errorCode = int(socketError)
        errorDescription = str(self.__socket.errorString())
        error = (errorCode, errorDescription)
        if self.__on_error:
            self.__on_error(error)

    @pyqtSlot()
    def __onReadyRead(self):
        '''
        The slot is called when new data is available for reading from the host. Then, all available data(str) is read
        and passed to __on_read callback.
        :return: None
        '''

        if self.__on_read:
            self.__on_read(self.__socket.readAll().data())

    # Setters
    def __connected(self, callback):
        self.__on_connected = callback

    def __disconnected(self, callback):
        self.__on_disconnected = callback

    def __error(self, callback):
        self.__on_error = callback

    def __read(self, callback):
        self.__on_read = callback

    # Properties
    onConnected = property(fset=__connected)
    onDisconnected = property(fset=__disconnected)
    onError = property(fset=__error)
    onRead = property(fset=__read)

    # Interface
    def connectToHost(self, host, port):
        '''
        Attempt to make a connection to host(str) <host> on the given port(int) <port>.
        :param host(str), remote host;
        :param port(int), remote port;
        :return: None
        '''

        self.__socket.connectToHost(host, port)

    def disconnectFromHost(self):
        '''
        Attempt to close the connection.
        :return: None
        '''

        self.__socket.disconnectFromHost()

    def close(self):
        '''
        Close the connection with the host, and reset the name, address, port number and underlying socket descriptor.
        :return: None
        '''

        self.__socket.close()

    def state(self):
        '''
        Return the state of the connection.
        :return: QAbstractSocket.SocketState, socket state
        '''

        return self.__socket.state()

    def write(self, data):
        '''
        Write data(str) <data> to the host.
        :param data(str): outgoing data;
        :return: int, the number of bytes that were actually written, or -1 if an error occurred
        '''

        return self.__socket.write(data)


class TcpServer(QObject):
    '''
    TCP/IP server class.

    Usage:
        import sys
        import tcp
        from PyQt4.QtCore import QCoreApplication
        from PyQt4.QtNetwork import QHostAddress


        def main():
            application = QCoreApplication(sys.argv)

            tcpServer = tcp.TcpServer()

            def onConnected(descriptor):
                print("Client [%s] connected. Now total: %s" % (descriptor, len(tcpServer.descriptors())))
                tcpServer.write(descriptor, "Hello dude")

            def onDisconnected(descriptor):
                print("Client [%s] disconnected. Now total: %s" % (descriptor, len(tcpServer.descriptors())))

            def onError(descriptor, error):
                print("Error [%s]: ", descriptor, error)

            def onRead(descriptor, data):
                print("Read from [%s] %s byte(s): %s" % (descriptor, len(data), data))

            tcpServer.onConnected = onConnected
            tcpServer.onDisconnected = onDisconnected
            tcpServer.onError = onError
            tcpServer.onRead = onRead
            tcpServer.listen(QHostAddress.Any, 9000)

            sys.exit(application.exec_())

        if __name__ == "__main__":
            main()
    '''

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.__server = QTcpServer(parent)
        self.__clients = dict()  # All active clients

        # Callbacks
        self.__on_connected = None
        self.__on_disconnected = None
        self.__on_error = None
        self.__on_read = None

        # Signals and slots connections
        self.__server.newConnection.connect(self.__onNewConnection)

    # Slots
    @pyqtSlot()
    def __onNewConnection(self):
        '''
        The slot is called every time a client connects to the server. The client's socket(QTcpSocket) <socket> and
        descriptor(int) <descriptor> are defined. The socket is appended to the dictionary of connected
        clients(key=client's descriptor, value=client's socket). Then, socket's descriptor is passed to
        __onConnected method.
        :return: None
        '''

        socket = self.__server.nextPendingConnection()
        socket.disconnected.connect(self.__onDisconnected)
        socket.error.connect(self.__onError)
        socket.readyRead.connect(self.__onReadyRead)
        descriptor = id(socket)
        self.__clients[descriptor] = socket
        self.__onConnected(descriptor)

    @pyqtSlot()
    def __onConnected(self, descriptor):
        '''
        The method is called by __onNewConnection every time a client connects to the server. If __on_connected callback
        is set, it is executed with socket's descriptor(int) <descriptor> argument.
        :param descriptor(int): a newly connected client's socket descriptor, the socket itself is in self.__clients
        dictionary(key=client's descriptor, value=client's socket);
        :return: None
        '''

        if self.__on_connected:
            self.__on_connected(descriptor)

    @pyqtSlot()
    def __onDisconnected(self):
        '''
        The slot is called when the connected client disconnects from the server. The client's socket(QTcpSocket)
        <socket> and its descriptor(int) <descriptor> are defined, and then the descriptor is passed to
        __on_disconnected callback.
        :return: None
        '''

        if self.__on_disconnected:
            socket = self.sender()
            descriptor = id(socket)
            self.__clients.pop(descriptor, None)
            self.__on_disconnected(descriptor)

    @pyqtSlot()
    def __onError(self, socketError):
        '''
        The slot is called when an error(PyQt4.QtNetwork.SocketError) <socketError> occurs. The socket's descriptor(int)
        <descriptor> with error code(int) <errorCode> and description(str) <errorDescription> are defined and passed
        to __on_error callback.
        :param error(QAbstractSocket.SocketError): socket error;
        :return: None
        '''

        if self.__on_error:
            socket = self.__server.sender()
            descriptor = id(socket)
            errorCode = int(socketError)
            errorDescription = str(self.__server.errorString())
            error = (errorCode, errorDescription)

            self.__on_error(descriptor, error)

    @pyqtSlot()
    def __onReadyRead(self):
        '''
        The slot is called when new data is available for reading from the client. The client's socket descriptor(int)
        <descriptor> is defined, and all available data(str) <data> is read. Then, the socket descriptor and the data
        are passed to __on_read callback.
        :return: None
        '''

        if self.__on_read:
            socket = self.sender()
            descriptor = id(socket)
            data = socket.readAll().data()
            self.__on_read(descriptor, data)

    # Setters
    def __connected(self, callback):
        self.__on_connected = callback

    def __disconnected(self, callback):
        self.__on_disconnected = callback

    def __error(self, callback):
        self.__on_error = callback

    def __read(self, callback):
        self.__on_read = callback

    # Methods
    def isListening(self):
        '''
        Return True if the server is currently listening for incoming connections, otherwise returns False.
        :return: bool
        '''

        return self.__server.isListening()

    def listen(self, address=None, port=0):
        '''
        Tell the server to listen for incoming connections on address(QHostAddress) <address> and port(int) <port>. If
        port is 0, a port is chosen automatically. If address is QHostAddress.Any, the server will listen on all network
        interfaces.
        :param address(QHosAddress): address to listen to;
        :param port(int): the port to listen to;
        :return: bool, return True on success, otherwise return False
        '''
        self.__server.listen(address, port)

    def socket(self, descriptor):
        '''
        Return socket(QTcpSocket) with the given descriptor(int) <descriptor> or None if it is not found.
        :param descriptor(int): socket descriptor;
        :return: socket(QTcpSocket) or None
        '''

        return self.__clients.get(descriptor, None)

    def descriptors(self):
        '''
        Return all sockets' descriptors available.
        :return list of int
        '''

        return sorted(self.__clients.keys())

    def write(self, descriptor, data):
        '''
        Write data(str) <data> to the client's socket with the given descriptor(int) <descriptor>.
        :param descriptor(int): client's socket descriptor;
        :param data(str), data to be written;
        :return: int, the number of bytes that were actually written, or -1 if an error occurred
        '''

        socket = self.socket(descriptor)
        if socket:
            return socket.write(data)
        else:
            return -1

    def disconnect(self, descriptor):
        '''
        Disconnect the client socket with the given descriptor(int) <descriptor>.
        :param descriptor(int): client's socket descriptor;
        :return: None
        '''

        socket = self.socket(descriptor)
        if socket:
            socket.close()

    def close(self):
        '''
        Close the server.
        :return: None
        '''
        for socket in self.__clients.values():
            socket.close()

        self.__server.close()

    # Properties
    onConnected = property(fset=__connected)
    onDisconnected = property(fset=__disconnected)
    onError = property(fset=__error)
    onRead = property(fset=__read)