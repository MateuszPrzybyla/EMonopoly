from threading import Thread
from utils.socket import read, send, ClientDisconnectedException

__author__ = 'mateusz'


class EMonopolySocketListener(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        try:
            while True:
                msg = self.receive()
                if not msg:
                    continue
                response = self.handle(msg)
                if response:
                    self.send(response)
        except ClientDisconnectedException:
            pass
        except Exception as e:
            self.handleError(e)

    def receive(self):
        try:
            msg = read(self.socket)
        except Exception as e:
            self.handleReceiveError(e)
        else:
            if msg == '':
                exception = ClientDisconnectedException("Client has disconnected")
                self.handleError(exception)
                raise exception
            return msg.strip()

    def send(self, msg):
        send(self.socket, msg)

    def handle(self, msg):
        raise NotImplementedError("handle method must be implemented by SocketListener subclass")

    def handleError(self, error):
        pass

    def handleReceiveError(self, error):
        pass