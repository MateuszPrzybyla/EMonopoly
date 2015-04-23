from EMonopolySocketListener import EMonopolySocketListener

from server.requestHandlers.RequestHandlerDispatcher import RequestHandlerDispatcher


__author__ = 'mateusz'


class GameClient(EMonopolySocketListener):
    def __init__(self, gameServer, socket, address):
        EMonopolySocketListener.__init__(self, socket)
        self.gameServer = gameServer
        self.address = address
        self.messageHandlerDispatcher = RequestHandlerDispatcher(self.gameServer)

    def handle(self, msg):
        print "Received %d bytes %s" % (len(msg), msg)
        return self.messageHandlerDispatcher.handle(msg, self.socket)

    def handleError(self, error):
        self.gameServer.notifyClientDisconnected(self)

    def handleReceiveError(self, error):
        self.gameServer.notifyClientDisconnected(self)
