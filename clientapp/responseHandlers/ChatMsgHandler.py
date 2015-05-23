from kivy.app import App

__author__ = 'mateusz'


class ChatMsgHandler(object):
    def __init__(self):
        self.app = App.get_running_app()

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success'] and 'type' in msg['responseData']:
            if msg['responseData']['type'] == 'SERVER':
                controller = self.app.gameRoomScreen.chatController
            elif msg['responseData']['type'] == 'ROOM':
                controller = self.app.singleRoomScreen.chatController
            controller.appendMessage(msg['responseData']['content'], msg['responseData']['author'], '')