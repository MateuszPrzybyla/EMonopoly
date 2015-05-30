from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'


class ChatMessageResponse(Response):
    def __init__(self, success, msg, type=None, author=None, content=None):
        if success:
            super(ChatMessageResponse, self).__init__("CHAT_MSG", True, msg, {
                'type': type,
                'author': author,
                'content': content
            })
        else:
            super(ChatMessageResponse, self).__init__("CHAT_MSG", False, msg, {})


class ChatRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(ChatRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, message, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if not message['msg'] or not message['msg'].strip() or not clientPlayer:
            return
        if 'type' not in message:
            return ChatMessageResponse(False, "type is missing")
        if message['type'] == 'SERVER':
            self.gameServer.broadcastAllPlayers(
                ChatMessageResponse(True, '', 'SERVER', clientPlayer.name, message['msg'].strip()))
        elif message['type'] == 'ROOM':
            if clientPlayer.joinedRoom:
                self.gameServer.broadcastAllRoom(clientPlayer.joinedRoom,
                    ChatMessageResponse(True, '', 'ROOM', clientPlayer.name, message['msg'].strip()))
            else:
                return ChatMessageResponse(False, "You are not a member of any room")