from kivy.app import App

__author__ = 'mateusz'

class JoinRoomHandler(object):
    def __init__(self):
        self.app = App.get_running_app()

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.app.changeScreen('singleRoomScreen', msg['responseData'])
        else:
            print "JOIN_ROOM failed"