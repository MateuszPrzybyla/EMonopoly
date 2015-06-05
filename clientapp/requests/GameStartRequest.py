from clientapp.requests.Request import Request

__author__ = 'mateusz'

class GameStartRequest(Request):
    def __init__(self):
        super(GameStartRequest, self).__init__("START_GAME", {})