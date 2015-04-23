from clientapp.requests.Request import Request

__author__ = 'mateusz'

class ServerChatMsg(Request):
    def __init__(self, msg):
        super(ServerChatMsg, self).__init__("SERVER_CHAT_MSG", {'msg': msg})