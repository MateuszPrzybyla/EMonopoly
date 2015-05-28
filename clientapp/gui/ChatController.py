from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from clientapp.requests.ChatMsg import ChatMsg

__author__ = 'mateusz'


class ChatMessage(Label):
    pass


class ChatController(BoxLayout):
    msgList = ObjectProperty()
    msgType = StringProperty()

    def __init__(self, **kwargs):
        super(ChatController, self).__init__(**kwargs)
        self.gameServerClient = App.get_running_app().gameServerClient

    def clear(self):
        self.msgList.clear_widgets()

    def clearSendMsg(self):
        self.ids['chatMsg'].text = ''

    def appendMessage(self, msg, author, timestamp, infoMessage=False):
        format = '[i][b]%s%s[/b] %s[/i]' if infoMessage else '[b]%s%s[/b] %s'
        self.msgList.add_widget(ChatMessage(text=format % (author, ':' if author else '', msg)))
        print "Message from %s, content %s, timestamp %s" % (author, msg, "")

    def sendChatMsg(self, msgType, msg):
        self.gameServerClient.send(ChatMsg(msg, msgType))
        self.clearSendMsg()