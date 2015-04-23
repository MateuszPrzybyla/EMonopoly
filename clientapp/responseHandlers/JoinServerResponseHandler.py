__author__ = 'mateusz'

class JoinServerResponseHandler(object):
    def __init__(self, clientApp, joinServerScreen):
        self.clientApp = clientApp
        self.joinServerScreen = joinServerScreen

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.clientApp.changeScreen('gameRoom')
        else:
            print "JOIN_SERVER failed"
            self.joinServerScreen.ids['errorLabel'].text = msg['message']