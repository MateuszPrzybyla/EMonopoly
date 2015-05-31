from threading import Lock
from utils.decorators import synchronized

__author__ = 'mateusz'

class ClientPlayer(object):
    lastId = 0
    idLock = Lock()

    def __init__(self, name, socket):
        self.id = self.assignId()
        self.name = name
        self.socket = socket
        self.joinedRoom = None

    @synchronized(idLock)
    def assignId(self):
        ClientPlayer.lastId += 1
        return ClientPlayer.lastId

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name
        }