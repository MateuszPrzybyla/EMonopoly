from EMonopolySocketListener import EMonopolySocketListener
from clientapp.ServerMessageDispatcher import ServerMessageDispatcher

__author__ = 'mateusz'

class ServerMessageListener(EMonopolySocketListener):
    def __init__(self, gameServerClient, socket, clientApp):
        EMonopolySocketListener.__init__(self, socket)
        self.responseHandlerDispatcher = ServerMessageDispatcher(clientApp)

    def handle(self, msg):
        print "Got message from game server: %d bytes %s" % (len(msg), msg)
        return self.responseHandlerDispatcher.handle(msg, self.socket)
