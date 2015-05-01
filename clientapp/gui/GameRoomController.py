from kivy.uix.boxlayout import BoxLayout
from clientapp.gui.CreateRoomPopup import CreateRoomPopup

__author__ = 'mateusz'

class GameRoomController(BoxLayout):
    def joinRoom(self):
        pass

    def openCreateRoomPopup(self):
        CreateRoomPopup().open()