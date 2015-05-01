from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from clientapp.requests.LeaveServerRequest import LeaveServerRequest

__author__ = 'mateusz'


class GameRoomScreen(Screen):
    chatController = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameRoomScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        app = App.get_running_app()
        self.gameServerClient = app.gameServerClient
        self.ids['loggedUserHeader'].text = "Logged in as: %s " % app.getData('nick')

    def on_leave(self, *args):
        self.ids['loggedUserHeader'].text = "Logged out"
        self.chatController.clear()

    def logOut(self):
        self.gameServerClient.send(LeaveServerRequest())