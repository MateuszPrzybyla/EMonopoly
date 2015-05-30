__author__ = 'mateusz'


class RequestHandler(object):
    def handleRequest(self, msg, rawMsg, clientSocket, clientPlayer):
        response = self.handle(msg, rawMsg, clientSocket, clientPlayer, clientPlayer.joinedRoom if clientPlayer else None)
        if response:
            return response.toJSON()
        else:
            return ""

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        return ""