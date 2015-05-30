from server.requestHandlers.Response import Response
from server.requestHandlers.RequestHandler import RequestHandler


__author__ = 'mateusz'


class UnknownMessageResponse(Response):
    def __init__(self, request):
        super(UnknownMessageResponse, self).__init__("UNKNOWN", True, "Message is invalid", {
            'request': request
        })


class UnknownRequestHandler(RequestHandler):
    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        return UnknownMessageResponse(rawMsg)