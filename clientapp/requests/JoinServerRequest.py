from clientapp.requests.Request import Request

__author__ = 'mateusz'


class JoinServerRequest(Request):
    def __init__(self, nick):
        super(JoinServerRequest, self).__init__("JOIN_SERVER", {'nick': nick})