from kivy.app import App

__author__ = 'mateusz'


class ServerChatMsgHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.chatController = self.app.gameRoomScreen.chatController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success']:
            self.chatController.appendMessage(msg['responseData']['content'], msg['responseData']['author'],
                                                    "")