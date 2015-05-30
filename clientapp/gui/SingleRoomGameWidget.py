from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from clientapp.requests.GameStartRequest import GameStartRequest

__author__ = 'mateusz'

class SingleRoomGameWidget(AnchorLayout):
    startMsgLabel = ObjectProperty()
    initialView = ObjectProperty()

    def __init__(self, **kwargs):
        super(SingleRoomGameWidget, self).__init__(**kwargs)
        self.gameServerClient = App.get_running_app().gameServerClient

    def startGame(self):
        self.gameServerClient.send(GameStartRequest())

    def restoreInitialView(self):
        self.clear_widgets()
        self.add_widget(self.initialView)