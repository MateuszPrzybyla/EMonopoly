from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

__author__ = 'mateusz'


class QuitRoomResponseHandler(object):
    def __init__(self):
        self.app = App.get_running_app()
        self.chatController = self.app.singleRoomScreen.chatController

    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        if msg['success'] and 'player' in msg['responseData']:
            if msg['responseData']['player'] == self.app.getData('nick'):
                self.app.changeScreen('gameRoom')
            else:
                if msg['responseData']['isRoomDead']:
                    popupLayout = BoxLayout(orientation='vertical')
                    popup = Popup(content=popupLayout)
                    popupLayout.add_widget(Label(text='Room has been closed by the owner'))
                    closeButton = Button(text='Close')
                    closeButton.bind(on_press=popup.dismiss)
                    popupLayout.add_widget(closeButton)
                    popup.bind(on_dismiss=lambda x: self.app.changeScreen('gameRoom'))
                    popup.open()
                else:
                    self.chatController.appendMessage('Player %s has left the room' % msg['responseData']['player'], '', '',
                                                  infoMessage=True)
        else:
            print "QUIT_ROOM failed"