from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from clientapp.gui.CreateRoomPopup import CreateRoomPopup
from clientapp.gui.RoomListElement import RoomListElement
from clientapp.requests.GetRoomsRequest import GetRoomsRequest
from clientapp.requests.JoinRoomRequest import JoinRoomRequest

__author__ = 'mateusz'

class GameRoomController(BoxLayout):
    roomsArea = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameRoomController, self).__init__(**kwargs)
        self.gameServerClient = App.get_running_app().gameServerClient

    def joinRoom(self, roomId):
        print "Joining room %d" % roomId
        self.gameServerClient.send(JoinRoomRequest(roomId))

    def openCreateRoomPopup(self):
        self.createRoomPopup = CreateRoomPopup()
        self.createRoomPopup.open()

    def closeCreateRoomPopup(self):
        if self.createRoomPopup:
            self.createRoomPopup.dismiss()
            self.createRoomPopup = None

    def refreshRooms(self):
        print "Refreshing room list"
        self.gameServerClient.send(GetRoomsRequest())

    def populateRooms(self, rooms):
        for room in rooms:
            self.roomsArea.add_widget(RoomListElement(room['id'], room['owner'], room['playersNumber'], room['players'], self))