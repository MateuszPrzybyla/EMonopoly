from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import ScreenManager, NoTransition

from clientapp.GameServerClient import GameServerClient
from clientapp.gui.GameRoomScreen import GameRoomScreen
from clientapp.gui.JoinServerScreen import JoinServerScreen

__author__ = 'mateusz'

from kivy.app import App


class EMonopolyClientApp(App):
    def __init__(self, **kwargs):
        super(EMonopolyClientApp, self).__init__(**kwargs)
        self.gameServerClient = GameServerClient('matdeb', 1234, self)

    def on_stop(self):
        self.gameServerClient.close()

    def build(self):
        self.joinServerScreen = JoinServerScreen(self.gameServerClient, name='typeNickname')
        self.gameRoomScreen = GameRoomScreen(self.gameServerClient, name='gameRoom')

        self.screenManager = ScreenManager()
        self.screenManager.add_widget(self.joinServerScreen)
        self.screenManager.add_widget(self.gameRoomScreen)
        self.screenManager.transition = NoTransition(duration=0)
        self.gameServerClient.start()
        return self.screenManager

    def changeScreen(self, screenName):
        self.screenManager.current = screenName


EMonopolyClientApp().run()