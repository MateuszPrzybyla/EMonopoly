from kivy.app import App

__author__ = 'mateusz'

class CreateRoomHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.gameRoomController = self.app.gameRoomScreen.gameRoomController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.gameRoomController.closeCreateRoomPopup()
            self.app.changeScreen('singleRoomScreen', msg['responseData'])
        else:
            self.gameRoomController.createRoomPopup.setError(msg['message'])
            print "CREATE_ROOM failed"