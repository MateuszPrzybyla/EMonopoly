from kivy.app import App

__author__ = 'mateusz'

class GameStateResponseHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.gameWidget = self.app.singleRoomScreen.singleRoomGameWidget

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if 'responseData' in msg:
            gameBoard = self.gameWidget.children[0]
            gameBoard.updateGameState(msg['responseData'])