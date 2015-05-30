from kivy.app import App
from kivy.properties import ObjectProperty
from clientapp.gui.EMonopolyScreen import EMonopolyScreen
from clientapp.requests.QuitRoomRequest import QuitRoomRequest

__author__ = 'mateusz'

class SingleRoomScreen(EMonopolyScreen):
    roomName = ObjectProperty()
    chatController = ObjectProperty()
    singleRoomGameWidget = ObjectProperty()

    def __init__(self, **kwargs):
        super(SingleRoomScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient

    def on_leave(self, *args):
        self.chatController.clear()
        self.singleRoomGameWidget.restoreInitialView()

    def load(self, args):
        self.roomId = args['id']
        self.roomName.text = "#%d %s" % (args['id'], args['name'])

    def quitRoom(self):
        self.gameServerClient.send(QuitRoomRequest())