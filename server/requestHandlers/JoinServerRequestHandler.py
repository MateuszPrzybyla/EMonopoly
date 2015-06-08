from threading import Lock
from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response


__author__ = 'mateusz'


class JoinServerResponse(Response):
    def __init__(self, success, msg, identifier, nick):
        super(JoinServerResponse, self).__init__("JOIN_SERVER", success, msg, {'id': identifier, 'nick': nick})


class JoinServerRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(JoinServerRequestHandler, self).__init__()
        self.gameServer = gameServer
        self.newPlayerLock = Lock()

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if clientPlayer:
            return JoinServerResponse(False, "Already joined as a %s" % clientPlayer.name, 0, msg['nick'])
        if len(msg['nick']) < 2:
            return JoinServerResponse(False, "Nick must have at least 2 characters", 0, msg['nick'])
        with self.newPlayerLock:
            if msg['nick'] in self.gameServer.players:
                return JoinServerResponse(False, "Nick is already used by another player", 0, msg['nick'])
            identifier = self.gameServer.notifyNewPlayer(msg['nick'], clientSocket)
            return JoinServerResponse(True, "Welcome to the server!", identifier, msg['nick'])