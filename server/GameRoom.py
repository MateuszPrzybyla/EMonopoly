from threading import Lock
from server.MonopolyGame import MonopolyGame
from utils.decorators import synchronized

__author__ = 'mateusz'


class GameRoom(object):
    lastId = 0
    idLock = Lock()

    def __init__(self, owner, name, playersNumber, players, password):
        self.id = self.assignId()
        self.owner = owner
        self.name = name
        self.playersNumber = playersNumber
        self.players = players
        self.password = password
        self.game = MonopolyGame(int(playersNumber), players)

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
            'players': [player.name for player in self.players],
            'playersNumber': self.playersNumber
        }