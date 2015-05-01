from kivy.app import App

__author__ = 'mateusz'

class LeaveServerResponseHandler(object):
    def __init__(self):
        self.clientApp = App.get_running_app()

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.clientApp.changeScreen('typeNickname')
        else:
            print "LEAVE_SERVER failed"