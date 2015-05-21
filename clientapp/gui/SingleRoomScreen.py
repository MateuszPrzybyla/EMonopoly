from kivy.app import App
from kivy.properties import ObjectProperty
from clientapp.gui.EMonopolyScreen import EMonopolyScreen

__author__ = 'mateusz'

class SingleRoomScreen(EMonopolyScreen):
    roomName = ObjectProperty()

    def __init__(self, **kwargs):
        super(SingleRoomScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def load(self, args):
        self.roomName.text = "#%d %s" % (args['id'], args['name'])

    def quitRoom(self):
        self.app.changeScreen('gameRoom')