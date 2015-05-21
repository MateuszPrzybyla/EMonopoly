from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'

class GetRoomsResponse(Response):
    def __init__(self, rooms):
        super(GetRoomsResponse, self).__init__("GET_ROOMS", True, "", {
            'rooms': self.prepareRoomsResponse(rooms)
        })

    def prepareRoomsResponse(self, rooms):
        return [room.toDict() for room in rooms]

class GetRoomsRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(GetRoomsRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, msg, rawMsg, clientSocket, clientPlayer):
        return GetRoomsResponse(self.gameServer.rooms.values())