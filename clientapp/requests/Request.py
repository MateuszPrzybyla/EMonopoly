import json
from json import JSONEncoder

__author__ = 'mateusz'

class RequestEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Request):
            return {
                'action': obj.action,
                'requestData': obj.requestData
            }
        else:
            return JSONEncoder.default(obj)

class Request(object):
    def __init__(self, action, requestData):
        self.action = action
        self.requestData = requestData

    def toJSON(self):
        return json.dumps(self, cls=RequestEncoder)