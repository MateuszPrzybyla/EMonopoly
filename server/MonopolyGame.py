from utils.eMonopoly import GAME_FIELDS

__author__ = 'mateusz'


class GameState(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'


class MonopolyGame(object):
    def __init__(self, playersNumber, players):
        self.fieldsSet = GAME_FIELDS
        self.state = GameState.NEW
        self.playersNumber = playersNumber
        self.players = players
        self.startRequest = set()

    def addStartRequest(self, player):
        alreadyExists = player in self.startRequest
        self.startRequest.add(player)
        return not alreadyExists, self.playersLeftToStart()

    def playersLeftToStart(self):
        return self.playersNumber - len(self.startRequest)

    def isReadyToStart(self):
        return len(self.startRequest) == self.playersNumber and self.state == GameState.NEW

    def startGame(self):
        if self.state != GameState.NEW:
            return
        self.state = GameState.ACTIVE

    def consumePlayerMove(self):
        if self.state != GameState.ACTIVE:
            return False