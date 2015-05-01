from clientapp.requests.Request import Request

__author__ = 'mateusz'

class LeaveServerRequest(Request):
    def __init__(self):
        super(LeaveServerRequest, self).__init__("LEAVE_SERVER")