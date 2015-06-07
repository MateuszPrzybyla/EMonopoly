from threading import Lock
from utils.decorators import synchronized

__author__ = 'mateusz'

class ClientPlayer(object):
    lastId = 0
    idLock = Lock()
    BANK_ID = 0

    def __init__(self, name, socket, identifier=None):
        self.id = self.assignId() if identifier is None else identifier
        self.name = name
        self.socket = socket
        self.joinedRoom = None

    @staticmethod
    def bankPlayer():
        return ClientPlayer(name="BANK", socket=None, identifier=ClientPlayer.BANK_ID)

    @synchronized(idLock)
    def assignId(self):
        ClientPlayer.lastId += 1
        return ClientPlayer.lastId

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name
        }