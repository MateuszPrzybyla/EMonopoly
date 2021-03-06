import json
from json.encoder import JSONEncoder
from server.ClientPlayer import ClientPlayer
from server.GameRoom import GameRoom

__author__ = 'mateusz'


class ResponseEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, Response):
                return {
                    'action': obj.action,
                    'success': obj.success,
                    'message': obj.message,
                    'responseData': obj.responseData
                }
            else:
                return JSONEncoder.default(obj)
        except Exception as e:
            pass


class Response(object):
    def __init__(self, action, success, message="", responseData=None):
        self.action = action
        self.success = success
        self.message = message
        self.responseData = responseData

    def toJSON(self):
        return json.dumps(self, cls=ResponseEncoder)


class NotAPlayerResponse(Response):
    def __init__(self):
        super(NotAPlayerResponse, self).__init__("NOT_A_PLAYER", False, "Not authenticated", {})