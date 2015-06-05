from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'


class GameStartResponse(Response):
    def __init__(self, success, msg="", playersLeft=0, gameStarted=False, player=None, gameData=None):
        if success:
            super(GameStartResponse, self).__init__("START_GAME", True, msg, {
                'gameStarted': gameStarted,
                'playersLeft': playersLeft,
                'player': player.name,
                'gameData': gameData.toDict() if gameData else None
            })
        else:
            super(GameStartResponse, self).__init__("START_GAME", False, msg)


class GameStartRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(GameStartRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if clientPlayer:
            if joinedRoom:
                monopolyGame = joinedRoom.game
                result, playersLeft = monopolyGame.addStartRequest(clientPlayer)
                if result:
                    if monopolyGame.isReadyToStart():
                        monopolyGame.startGame()
                        self.gameServer.broadcastAllRoom(joinedRoom,
                                                         GameStartResponse(True, "Game has started!", gameStarted=True,
                                                                           player=clientPlayer, gameData=monopolyGame))
                    else:
                        self.gameServer.broadcastAllRoom(
                            joinedRoom, GameStartResponse(True, playersLeft=playersLeft, player=clientPlayer))
            else:
                return GameStartResponse(False, "You are not in any room")
        else:
            return GameStartResponse(False, "Unknown player")