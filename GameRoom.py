from threading import Lock
from decorators import synchronized

__author__ = 'mateusz'


class GameRoom(object):
    lastId = 0
    idLock = Lock()

    def __init__(self, owner):
        self.owner = owner

    @synchronized(idLock)
    def assignId(self):
        GameRoom.lastId += 1
        self.id = GameRoom.lastId