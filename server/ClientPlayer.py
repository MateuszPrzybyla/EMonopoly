from threading import Lock
from utils.decorators import synchronized

__author__ = 'mateusz'


class ClientPlayer(object):
    lastId = 0
    idLock = Lock()
    BANK_ID = 0
    BANK_PLAYER = None
    ALL_ID = -1
    ALL_PLAYER = None

    def __init__(self, name, socket, identifier=None):
        self.id = self.assignId() if identifier is None else identifier
        self.name = name
        self.socket = socket
        self.joinedRoom = None

    @staticmethod
    def bankPlayer():
        if (ClientPlayer.BANK_PLAYER) is None:
            ClientPlayer.BANK_PLAYER = ClientPlayer(name="BANK", socket=None, identifier=ClientPlayer.BANK_ID)
        return ClientPlayer.BANK_PLAYER

    @staticmethod
    def allPlayer():
        if ClientPlayer.ALL_PLAYER is None:
            ClientPlayer.ALL_PLAYER = ClientPlayer(name="ALL", socket=None, identifier=ClientPlayer.ALL_ID)
        return ClientPlayer.ALL_PLAYER

    @synchronized(idLock)
    def assignId(self):
        ClientPlayer.lastId += 1
        return ClientPlayer.lastId

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name
        }