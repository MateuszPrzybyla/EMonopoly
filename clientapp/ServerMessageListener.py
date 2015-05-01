from EMonopolySocketListener import EMonopolySocketListener
from clientapp.ServerMessageDispatcher import ServerMessageDispatcher

__author__ = 'mateusz'


class ServerMessageListener(EMonopolySocketListener):
    def __init__(self, socket):
        EMonopolySocketListener.__init__(self, socket)
        self.responseHandlerDispatcher = ServerMessageDispatcher()

    def handle(self, msg):
        print "Got message from game server: %d bytes %s" % (len(msg), msg)
        return self.responseHandlerDispatcher.handle(msg, self.socket)

    def handleError(self, error):
        print "ERROR %s" % error