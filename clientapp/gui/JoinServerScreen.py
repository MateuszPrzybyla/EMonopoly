from kivy.app import App
from clientapp.gui.EMonopolyScreen import EMonopolyScreen
from clientapp.requests.JoinServerRequest import JoinServerRequest

__author__ = 'mateusz'


class JoinServerScreen(EMonopolyScreen):
    def __init__(self, **kwargs):
        super(JoinServerScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.gameServerClient = App.get_running_app().gameServerClient

    def on_leave(self, *args):
        self.ids['errorLabel'].text = ''
        self.ids['nickInput'].text = ''

    def joinServer(self, nick):
        self.gameServerClient.send(JoinServerRequest(nick))