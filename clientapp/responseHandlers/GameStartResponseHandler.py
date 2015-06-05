from kivy.app import App

from clientapp.gui.board.GameBoard import GameBoard


__author__ = 'mateusz'


class GameStartResponseHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.gameWidget = self.app.singleRoomScreen.singleRoomGameWidget
        self.chatController = self.app.singleRoomScreen.chatController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success'] and 'responseData' in msg:
            self.chatController.appendMessage('Player %s wants to start a game' % msg['responseData']['player'], '', '',
                                              infoMessage=True)
            if msg['responseData']['gameStarted']:
                self.gameWidget.clear_widgets()
                boardWidget = GameBoard()
                boardWidget.initialize(msg['responseData'])
                self.gameWidget.add_widget(boardWidget)
                self.chatController.appendMessage('Game is on!', '', '', infoMessage=True)
            else:
                self.gameWidget.startMsgLabel.text = \
                    "Waiting for all players to start... (%d left)" % msg['responseData']['playersLeft']
        else:
            print "START_GAME failed"