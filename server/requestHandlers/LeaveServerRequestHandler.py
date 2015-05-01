from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'

class LeaveServerResponse(Response):
    def __init__(self, success, msg):
        super(LeaveServerResponse, self).__init__("LEAVE_SERVER", success, msg)

class LeaveServerRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(LeaveServerRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, msg, rawMsg, clientSocket, clientPlayer):
        with self.gameServer.playersLock:
            if clientPlayer:
                return LeaveServerResponse(self.gameServer.notifyPlayerLeaveServer(clientSocket), "")
            else:
                return LeaveServerResponse(False, "Unknown player")