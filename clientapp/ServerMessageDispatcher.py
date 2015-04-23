import json
from clientapp.responseHandlers.JoinServerResponseHandler import JoinServerResponseHandler
from clientapp.responseHandlers.UnknownMessageHandler import UnknownMessageHandler

__author__ = 'mateusz'

class ServerMessageDispatcher(object):
    def __init__(self, clientApp):
        self.clientApp = clientApp
        self.handlersMap = {
            'JOIN_SERVER': JoinServerResponseHandler(self.clientApp, self.clientApp.joinServerScreen)
        }
        self.defaultHandler = UnknownMessageHandler()

    def handle(self, jsonMsg, gameServerSocket):
        msg = None
        try:
            msg = json.loads(jsonMsg)
        except ValueError:
            handler = UnknownMessageHandler()
        else:
            if msg['action'] in self.handlersMap:
                handler = self.handlersMap[msg['action']]
            else:
                handler = self.defaultHandler
            return handler.handleRequest(msg, jsonMsg, gameServerSocket)