from clientapp.requests.Request import Request

__author__ = 'mateusz'

class ChatMsg(Request):
    def __init__(self, msg, type):
        super(ChatMsg, self).__init__("CHAT_MSG", {'msg': msg, 'type': type})