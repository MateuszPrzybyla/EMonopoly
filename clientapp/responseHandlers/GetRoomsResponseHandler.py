from kivy.app import App

__author__ = 'mateusz'

class GetRoomsResponseHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.gameRoomController = self.app.gameRoomScreen.gameRoomController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.gameRoomController.populateRooms(msg['responseData']['rooms'])
            print jsonMsg
        else:
            print "GET_ROOMS failed"