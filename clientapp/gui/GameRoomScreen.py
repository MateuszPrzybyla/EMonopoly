from kivy.app import App
from kivy.properties import ObjectProperty
from clientapp.gui.EMonopolyScreen import EMonopolyScreen
from clientapp.requests.LeaveServerRequest import LeaveServerRequest

__author__ = 'mateusz'


class GameRoomScreen(EMonopolyScreen):
    chatController = ObjectProperty()
    gameRoomController = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameRoomScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient
        self.ids['loggedUserHeader'].text = "Logged in as: %s " % self.app.getData('nick')

    def on_leave(self, *args):
        if self.app.currentScreen().name == 'typeNickname':
            self.ids['loggedUserHeader'].text = "Logged out"
            self.chatController.clear()

    def logOut(self):
        self.gameServerClient.send(LeaveServerRequest())