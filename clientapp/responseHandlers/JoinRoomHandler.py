from kivy.app import App

__author__ = 'mateusz'


class JoinRoomHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.chatController = self.app.singleRoomScreen.chatController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            if msg['responseData']['player'] == self.app.getData('nick'):
                self.app.changeScreen('singleRoomScreen', msg['responseData']['room'])
            else:
                self.chatController.appendMessage('Player %s has joined the room' % msg['responseData']['player'], '',
                                                  '', infoMessage=True)
        else:
            print "JOIN_ROOM failed"