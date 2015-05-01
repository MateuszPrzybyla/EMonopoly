from kivy.app import App

__author__ = 'mateusz'

class JoinServerResponseHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.joinServerScreen = self.app.joinServerScreen

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.app.setData('nick', msg['responseData']['nick'])
            self.app.changeScreen('gameRoom')
        else:
            print "JOIN_SERVER failed"
            self.joinServerScreen.ids['errorLabel'].text = msg['message']