from threading import Thread

__author__ = 'mateusz'


class ClientDisconnectedException(Exception):
    pass


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
                if not response:
                    continue
                self.send(response)
        except ClientDisconnectedException:
            pass
        except Exception as e:
            self.handleError(e)

    def receive(self):
        try:
            msg = self.socket.recv(2048)
        except Exception as e:
            self.handleReceiveError(e)
        else:
            if msg == '':
                exception = ClientDisconnectedException()
                self.handleError(exception)
                raise exception
            return msg.strip()


    def send(self, msg):
        self.socket.send(msg)

    def handle(self, msg):
        raise NotImplementedError("handle method must be implemented by SocketListener subclass")

    def handleError(self, error):
        pass

    def handleReceiveError(self, error):
        pass