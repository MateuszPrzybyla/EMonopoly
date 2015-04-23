from kivy.uix.screenmanager import Screen
from clientapp.requests.ServerChatMsg import ServerChatMsg

__author__ = 'mateusz'


class GameRoomScreen(Screen):
    def __init__(self, gameServerClient, **kwargs):
        super(GameRoomScreen, self).__init__(**kwargs)
        self.gameServerClient = gameServerClient

    def sendServerChatMsg(self, msg):
        self.gameServerClient.send(ServerChatMsg(msg))
