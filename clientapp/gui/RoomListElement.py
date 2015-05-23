from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

__author__ = 'mateusz'

class RoomListElement(BoxLayout):
    roomNumber = ObjectProperty()
    roomName = ObjectProperty()
    playersNumber = ObjectProperty()
    roomPlayers = ObjectProperty()
    color = NumericProperty(1)

    def __init__(self, roomNumber, roomName, playersNumber, players, roomController):
        super(RoomListElement, self).__init__()
        self.roomNumberId = roomNumber
        self.roomNumber.text = "#%d" % roomNumber
        self.roomName.text = roomName
        self.playersNumber.text = playersNumber
        if players:
            self.roomPlayers.text = "[b]%s[/b]%s" % (players[0], ', '.join(players[1:]))
        else:
            self.roomPlayers.text = ""
        self.roomController = roomController

    def joinRoom(self):
        self.roomController.joinRoom(self.roomNumberId)