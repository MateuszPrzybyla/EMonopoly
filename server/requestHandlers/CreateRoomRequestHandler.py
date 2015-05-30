from threading import Lock
from server.GameRoom import GameRoom
from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'

class CreateRoomResponse(Response):
    def __init__(self, success, msg="", room=None):
        super(CreateRoomResponse, self).__init__("CREATE_ROOM", success, msg, room.toDict() if room is not None else {})

class CreateRoomRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(CreateRoomRequestHandler, self).__init__()
        self.gameServer = gameServer
        self.createRoomLock = Lock()

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if clientPlayer:
            if not msg['roomName']:
                return CreateRoomResponse(False, msg="Room name cannot be empty")
            with self.createRoomLock:
                if clientPlayer in self.gameServer.rooms:
                    return CreateRoomResponse(False, msg="You already own a room")
                for room in self.gameServer.rooms.values():
                    if room.name == msg['roomName']:
                        return CreateRoomResponse(False, msg="Room with such name already exists")
                room = GameRoom(clientPlayer, msg['roomName'], msg['playersNumber'], [clientPlayer], msg['password'])
                clientPlayer.joinedRoom = room
                self.gameServer.notifyNewRoom(clientPlayer, room)
                return CreateRoomResponse(True, room=room)
        else:
            return CreateRoomResponse(False, msg="Unknown player")