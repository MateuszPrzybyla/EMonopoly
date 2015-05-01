from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from clientapp.requests.ServerChatMsg import ServerChatMsg

__author__ = 'mateusz'


class ChatMessage(Label):
    pass


class ChatController(BoxLayout):
    msgList = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChatController, self).__init__(**kwargs)
        self.gameServerClient = App.get_running_app().gameServerClient

    def clear(self):
        self.msgList.clear_widgets()

    def clearSendMsg(self):
        self.ids['chatMsg'].text = ''

    def appendServerMessage(self, msg, author, timestamp):
        self.msgList.add_widget(ChatMessage(text='[b]%s:[/b] %s' % (author, msg)))
        print "Message from %s, content %s, timestamp %s" % (author, msg, "")

    def sendServerChatMsg(self, msg):
        self.gameServerClient.send(ServerChatMsg(msg))
        self.clearSendMsg()