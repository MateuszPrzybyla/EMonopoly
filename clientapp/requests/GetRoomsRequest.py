from clientapp.requests.Request import Request

__author__ = 'mateusz'

class GetRoomsRequest(Request):
    def __init__(self):
        super(GetRoomsRequest, self).__init__("GET_ROOMS", {})