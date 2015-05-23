import json
from clientapp.responseHandlers.CreateRoomHandler import CreateRoomHandler
from clientapp.responseHandlers.GetRoomsResponseHandler import GetRoomsResponseHandler
from clientapp.responseHandlers.JoinRoomHandler import JoinRoomHandler
from clientapp.responseHandlers.JoinServerResponseHandler import JoinServerResponseHandler
from clientapp.responseHandlers.LeaveServerResponseHandler import LeaveServerResponseHandler
from clientapp.responseHandlers.ChatMsgHandler import ChatMsgHandler
from clientapp.responseHandlers.UnknownMessageHandler import UnknownMessageHandler

__author__ = 'mateusz'


class ServerMessageDispatcher(object):
    def __init__(self):
        self.handlersMap = {
            'JOIN_SERVER': JoinServerResponseHandler(),
            'LEAVE_SERVER': LeaveServerResponseHandler(),
            'CHAT_MSG': ChatMsgHandler(),
            'CREATE_ROOM': CreateRoomHandler(),
            'GET_ROOMS': GetRoomsResponseHandler(),
            'JOIN_ROOM': JoinRoomHandler(),
            'QUIT_ROOM': UnknownMessageHandler()
        }
        self.defaultHandler = UnknownMessageHandler()

    def handle(self, jsonMsg, gameServerSocket):
        msg = None
        try:
            msg = json.loads(jsonMsg)
        except ValueError:
            self.defaultHandler.handleRequest(msg, jsonMsg, gameServerSocket)
        else:
            if msg['action'] in self.handlersMap:
                handler = self.handlersMap[msg['action']]
            else:
                handler = self.defaultHandler
            return handler.handleRequest(msg, jsonMsg, gameServerSocket)