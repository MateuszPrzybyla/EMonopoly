import socket
from clientapp.ServerMessageListener import ServerMessageListener

from clientapp.requests.Request import Request


__author__ = 'mateusz'


class GameServerClient(object):
    def __init__(self, host, port, clientApp):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.clientApp = clientApp

    def start(self):
        self.serverSocket.connect((self.host, self.port))
        self.serverMessageListener = ServerMessageListener(self.serverSocket)
        self.serverMessageListener.setDaemon(True)
        self.serverMessageListener.start()

    def close(self):
        self.serverSocket.close()

    def sendRaw(self, rawMsg):
        self.serverSocket.send(rawMsg)

    def send(self, msg):
        if isinstance(msg, Request):
            self.serverSocket.send(msg.toJSON())
        else:
            self.sendRaw(msg)