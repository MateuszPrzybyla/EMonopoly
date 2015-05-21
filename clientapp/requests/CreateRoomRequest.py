from clientapp.requests.Request import Request

__author__ = 'mateusz'


class CreateRoomRequest(Request):
    def __init__(self, roomName, playersNumber, isPrivate, password):
        super(CreateRoomRequest, self).__init__("CREATE_ROOM", {
            'roomName': roomName,
            'playersNumber': playersNumber,
            'isPrivate': isPrivate,
            'password': password
        })