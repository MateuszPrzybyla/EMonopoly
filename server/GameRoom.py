from threading import Lock
from utils.decorators import synchronized

__author__ = 'mateusz'


class GameRoom(object):
    lastId = 0
    idLock = Lock()

    def __init__(self, owner, name, playersNumber, password):
        self.id = self.assignId()
        self.owner = owner
        self.name = name
        self.playersNumber = playersNumber
        self.password = password

    @synchronized(idLock)
    def assignId(self):
        GameRoom.lastId += 1
        return GameRoom.lastId

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.name,
            'private': self.password and len(self.password) > 0,
            'playersNumber': self.playersNumber
        }