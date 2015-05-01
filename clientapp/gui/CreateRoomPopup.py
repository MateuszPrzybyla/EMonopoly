from kivy.uix.popup import Popup

__author__ = 'mateusz'


class CreateRoomPopup(Popup):
    def createRoomRequest(self, roomName, playersNumber, isPrivate, password):
        print "Creating a room %s %s %s %s" % (roomName, playersNumber, isPrivate, password)
        self.dismiss()

    def setPasswordActive(self, checkbox, password):
        password.disabled = not checkbox.active