__author__ = 'mateusz'

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.app import App
from kivy.factory import Factory

from clientapp.GameServerClient import GameServerClient
from clientapp.gui.GameRoomScreen import GameRoomScreen
from clientapp.gui.JoinServerScreen import JoinServerScreen


Factory.register('ChatController', module='clientapp.gui.ChatController')
Factory.register('ChatMessage', module='clientapp.gui.ChatController')
Factory.register('GameRoomController', module='clientapp.gui.GameRoomController')
Factory.register('CreateRoomPopup', module='clientapp.gui.CreateRoomPopup')

class EMonopolyClientApp(App):
    def __init__(self, **kwargs):
        super(EMonopolyClientApp, self).__init__(**kwargs)
        self.data = dict()
        self.gameServerClient = GameServerClient('matdeb', 1234, self)

    def on_stop(self):
        self.gameServerClient.close()

    def build(self):
        self.joinServerScreen = JoinServerScreen(name='typeNickname')
        self.gameRoomScreen = GameRoomScreen(name='gameRoom')

        self.screenManager = ScreenManager()
        self.screenManager.add_widget(self.joinServerScreen)
        self.screenManager.add_widget(self.gameRoomScreen)
        self.screenManager.transition = NoTransition(duration=0)
        self.gameServerClient.start()
        return self.screenManager

    def setData(self, key, value):
        self.data[key] = value

    def getData(self, key):
        return self.data[key]

    def changeScreen(self, screenName):
        self.screenManager.current = screenName


EMonopolyClientApp().run()