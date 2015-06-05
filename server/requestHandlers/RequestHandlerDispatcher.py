import json
from server.requestHandlers.CreateRoomRequestHandler import CreateRoomRequestHandler
from server.requestHandlers.GameMoveRequestHandler import GameMoveRequestHandler
from server.requestHandlers.GameStartRequestHandler import GameStartRequestHandler
from server.requestHandlers.GetRoomsRequestHandler import GetRoomsRequestHandler
from server.requestHandlers.JoinRoomRequestHandler import JoinRoomRequestHandler

from server.requestHandlers.JoinServerRequestHandler import JoinServerRequestHandler
from server.requestHandlers.LeaveServerRequestHandler import LeaveServerRequestHandler
from server.requestHandlers.ChatRequestHandler import ChatRequestHandler
from server.requestHandlers.QuitRoomRequestHandler import QuitRoomRequestHandler
from server.requestHandlers.UnknownRequestHandler import UnknownRequestHandler


__author__ = 'mateusz'


class RequestHandlerDispatcher(object):
    def __init__(self, gameServer):
        self.gameServer = gameServer
        self.handlersMap = {
            'JOIN_SERVER': JoinServerRequestHandler(self.gameServer),
            'LEAVE_SERVER': LeaveServerRequestHandler(self.gameServer),
            'CHAT_MSG': ChatRequestHandler(self.gameServer),
            'CREATE_ROOM': CreateRoomRequestHandler(self.gameServer),
            'GET_ROOMS': GetRoomsRequestHandler(self.gameServer),
            'JOIN_ROOM': JoinRoomRequestHandler(self.gameServer),
            'QUIT_ROOM': QuitRoomRequestHandler(self.gameServer),
            'START_GAME': GameStartRequestHandler(self.gameServer)
        }
        self.gameMoveHandler = GameMoveRequestHandler(self.gameServer)
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
            elif msg['action'].startswith('GAME_'):
                handler = self.gameMoveHandler
            else:
                handler = self.defaultHandler
        clientPlayer = self.gameServer.getClientPlayer(clientSocket)
        if msg and 'requestData' in msg:
            return handler.handleRequest(msg['requestData'], jsonMsg, clientSocket, clientPlayer)
        else:
            return handler.handleRequest(msg, jsonMsg, clientSocket, clientPlayer)