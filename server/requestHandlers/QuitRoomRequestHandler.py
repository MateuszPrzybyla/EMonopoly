from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response, NotAPlayerResponse

__author__ = 'mateusz'


class QuitRoomResponse(Response):
    def __init__(self, success, msg="", player=None, isRoomDead=False):
        if success:
            super(QuitRoomResponse, self).__init__("QUIT_ROOM", True, msg, {
                'player': player.name,
                'isRoomDead': isRoomDead
            })
        else:
            super(QuitRoomResponse, self).__init__("QUIT_ROOM", False, msg, {})


class QuitRoomRequestHandler(RequestHandler):
    def __init__(self, gameServer, gameMoveHandler):
        super(QuitRoomRequestHandler, self).__init__()
        self.gameServer = gameServer
        self.gameMoveHandler = gameMoveHandler

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if clientPlayer:
            room = clientPlayer.joinedRoom
            if not room:
                return QuitRoomResponse(False, msg="You are not in any room")
            clientPlayer.joinedRoom.game.notifyPlayerLeft(
                clientPlayer.id, self.gameMoveHandler.getGameStateCallback(clientPlayer.joinedRoom))
            if room.owner == clientPlayer:
                self.gameServer.notifyCloseRoom(clientPlayer, room)
                self.gameServer.broadcastAllRoom(room, QuitRoomResponse(True, "", clientPlayer, True))
            else:
                self.gameServer.broadcastAllRoom(room, QuitRoomResponse(True, "", clientPlayer, False))
                room.players.remove(clientPlayer)
            clientPlayer.joinedRoom = None
        else:
            return NotAPlayerResponse()