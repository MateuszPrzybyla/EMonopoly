import json

from server.requestHandlers.JoinServerRequestHandler import JoinServerRequestHandler
from server.requestHandlers.ServerChatRequestHandler import ServerChatRequestHandler
from server.requestHandlers.UnknownRequestHandler import UnknownRequestHandler


__author__ = 'mateusz'


class RequestHandlerDispatcher(object):
    def __init__(self, gameServer):
        self.gameServer = gameServer
        self.handlersMap = {
            'JOIN_SERVER': JoinServerRequestHandler(self.gameServer),
            'SERVER_CHAT_MSG': ServerChatRequestHandler(self.gameServer)
        }
        self.defaultHandler = UnknownRequestHandler()

    def handle(self, jsonMsg, clientSocket):
        msg = None
        try:
            msg = json.loads(jsonMsg)
        except ValueError:
            handler = self.defaultHandler
        else:
            if msg['action'] in self.handlersMap:
                handler = self.handlersMap[msg['action']]
            else:
                handler = self.defaultHandler
        clientPlayer = self.gameServer.getClientPlayer(clientSocket)
        if msg and 'requestData' in msg:
            return handler.handleRequest(msg['requestData'], jsonMsg, clientSocket, clientPlayer)
        else:
            return handler.handleRequest(msg, jsonMsg, clientSocket, clientPlayer)