from clientapp.requests.Request import Request

__author__ = 'mateusz'

class QuitRoomRequest(Request):
    def __init__(self):
        super(QuitRoomRequest, self).__init__("QUIT_ROOM")