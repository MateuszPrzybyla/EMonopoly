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
                    popup_layout = BoxLayout(orientation='vertical')
                    popup = Popup(content=popup_layout)
                    popup_layout.add_widget(Label(text='Room has been closed by the owner'))
                    close_button = Button(text='Close')
                    close_button.bind(on_press=popup.dismiss)
                    popup_layout.add_widget(close_button)
                    popup.bind(on_dismiss=lambda x: self.app.changeScreen('gameRoom'))
                    popup.open()
                else:
                    self.chatController.appendMessage('Player %s has left the room' % msg['responseData']['player'],
                                                      '', '', info_message=True)
        else:
            print "QUIT_ROOM failed"