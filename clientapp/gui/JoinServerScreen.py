from kivy.uix.screenmanager import Screen
from clientapp.requests.JoinServerRequest import JoinServerRequest

__author__ = 'mateusz'


class JoinServerScreen(Screen):
    def __init__(self, gameServerClient, **kwargs):
        super(JoinServerScreen, self).__init__(**kwargs)
        self.gameServerClient = gameServerClient

    def joinServer(self, nick):
        self.gameServerClient.send(JoinServerRequest(nick))