from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response


__author__ = 'mateusz'


class JoinServerResponse(Response):
    def __init__(self, success, msg, nick):
        super(JoinServerResponse, self).__init__("JOIN_SERVER", success, msg, {'nick': nick})


class JoinServerRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(JoinServerRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, msg, rawMsg, clientSocket, clientPlayer):
        with self.gameServer.playersLock:
            if clientPlayer:
                return JoinServerResponse(False, "Already joined as a %s" % clientPlayer.name, msg['nick'])
            if len(msg['nick']) < 2:
                return JoinServerResponse(False, "Nick must have at least 2 characters", msg['nick'])
            if msg['nick'] in self.gameServer.players:
                return JoinServerResponse(False, "Nick is already used by another player", msg['nick'])
            self.gameServer.notifyNewPlayer(msg['nick'], clientSocket)
            return JoinServerResponse(True, "Welcome to the server!", msg['nick'])