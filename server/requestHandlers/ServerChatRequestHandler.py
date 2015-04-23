from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import Response

__author__ = 'mateusz'


class ServerChatMessageResponse(Response):
    def __init__(self, success, msg, author, content, timestamp):
        super(ServerChatMessageResponse, self).__init__("SERVER_CHAT_MSG", success, msg, {
            'author': author,
            'content': content
        })


class ServerChatRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(ServerChatRequestHandler, self).__init__()
        self.gameServer = gameServer

    def handle(self, message, rawMsg, clientSocket, clientPlayer):
        if not message['msg'] or not message['msg'].strip() or not clientPlayer:
            return
        with self.gameServer.playersLock:
            self.gameServer.broadcastAllPlayers(
                ServerChatMessageResponse(True, "", clientPlayer.name, message['msg'].strip(), 12345))