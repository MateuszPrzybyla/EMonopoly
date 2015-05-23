from clientapp.requests.Request import Request

__author__ = 'mateusz'


class JoinRoomRequest(Request):
    def __init__(self, roomId):
        super(JoinRoomRequest, self).__init__("JOIN_ROOM", {'roomId': roomId})