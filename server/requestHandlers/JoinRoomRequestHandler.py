from threading import Lock
from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import NotAPlayerResponse, Response

__author__ = 'mateusz'


class JoinRoomResponse(Response):
    def __init__(self, success, msg="", room=None):
        super(JoinRoomResponse, self).__init__("JOIN_ROOM", success, msg, room.toDict() if room is not None else {})


class JoinRoomRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(JoinRoomRequestHandler, self).__init__()
        self.gameServer = gameServer
        self.joinRoomLock = Lock()

    def handle(self, msg, rawMsg, clientSocket, clientPlayer):
        if clientPlayer:
            if not msg['roomId']:
                return JoinRoomResponse(False, msg="roomId cannot be empty")
            with self.joinRoomLock:
                if clientPlayer.joinedRoom:
                    if clientPlayer.joinedRoom.id != msg['roomId']:
                        return JoinRoomResponse(False, msg="You already joined room %d" % clientPlayer.joinedRoom.id)
                    else:
                        return JoinRoomResponse(False, msg="You already are in this room")
                room = self.gameServer.getRoom(msg['roomId'])
                if not room:
                    return JoinRoomResponse(False, msg="Room not found")
                room.players.append(clientPlayer)
                clientPlayer.joinedRoom = room
                return JoinRoomResponse(True, room=room)
        else:
            return NotAPlayerResponse()