from threading import Lock
from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import NotAPlayerResponse, Response

__author__ = 'mateusz'


class JoinRoomResponse(Response):
    def __init__(self, success, msg="", player=None, room=None):
        if success:
            super(JoinRoomResponse, self).__init__("JOIN_ROOM", True, msg, {
                'room': room.toDict(),
                'player': player.name
            })
        else:
            super(JoinRoomResponse, self).__init__("JOIN_ROOM", False, msg, {})


class JoinRoomRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(JoinRoomRequestHandler, self).__init__()
        self.gameServer = gameServer
        self.joinRoomLock = Lock()

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if clientPlayer:
            if not msg['roomId']:
                return JoinRoomResponse(False, msg="roomId cannot be empty")
            with self.joinRoomLock:
                if joinedRoom:
                    if joinedRoom.id != msg['roomId']:
                        return JoinRoomResponse(False, msg="You already joined room %d" % joinedRoom.id)
                    else:
                        return JoinRoomResponse(False, msg="You already are in this room")
                room = self.gameServer.getRoom(msg['roomId'])
                if not room:
                    return JoinRoomResponse(False, msg="Room not found")
                room.players.append(clientPlayer)
                room.game.allPlayers.append(clientPlayer)
                clientPlayer.joinedRoom = room
                self.gameServer.broadcastAllRoom(room, JoinRoomResponse(True, player=clientPlayer, room=room))
        else:
            return NotAPlayerResponse()