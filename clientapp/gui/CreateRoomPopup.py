from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from clientapp.requests.CreateRoomRequest import CreateRoomRequest

__author__ = 'mateusz'


class CreateRoomPopup(Popup):
    errorLabel = ObjectProperty()

    def __init__(self, **kwargs):
        super(CreateRoomPopup, self).__init__(**kwargs)
        self.gameServerClient = App.get_running_app().gameServerClient

    def createRoomRequest(self, roomName, playersNumber, isPrivate, password):
        print "Creating a room %s %s %s %s" % (roomName, playersNumber, isPrivate, password)
        self.gameServerClient.send(CreateRoomRequest(roomName, playersNumber, isPrivate, password))

    def setPasswordActive(self, checkbox, password):
        password.disabled = not checkbox.active

    def setError(self, msg):
        self.errorLabel.text = msg