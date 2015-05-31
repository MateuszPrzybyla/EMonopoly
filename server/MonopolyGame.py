from utils.eMonopoly import GAME_FIELDS

__author__ = 'mateusz'


class GameState(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'


class PlayerData(object):
    def __init__(self, fieldPosition=0, startBalance=1500, housesLeft=32):
        self.fieldPosition = fieldPosition
        self.balance = startBalance
        self.housesLeft = housesLeft
        self.buildings = dict()

    def toDict(self):
        return {
            'position': self.fieldPosition,
            'balance': self.balance,
            'housesLeft': self.housesLeft,
            'buildings': self.buildings
        }


class MonopolyGame(object):
    def __init__(self, id, playersNumber, players):
        self.id = id
        self.fieldsSet = GAME_FIELDS
        self.state = GameState.NEW
        self.playersNumber = playersNumber
        self.players = players
        self.startRequest = set()
        self.playersData = dict()
        self.moveOwner = None

    def addStartRequest(self, player):
        alreadyExists = player in self.startRequest
        self.startRequest.add(player)
        return not alreadyExists, self.playersLeftToStart()

    def playersLeftToStart(self):
        return self.playersNumber - len(self.startRequest)

    def isReadyToStart(self):
        return len(self.startRequest) == self.playersNumber and self.state != GameState.ACTIVE

    def startGame(self):
        if self.state == GameState.ACTIVE:
            return
        self.state = GameState.ACTIVE
        self.moveOwner = self.players[0]
        self.playersData = {player.id: PlayerData(0, 1500, 32) for player in self.players}

    def consumePlayerMove(self):
        if self.state != GameState.ACTIVE:
            return False

    def toDict(self):
        return {
            'id': self.id,
            'fields': [field.toDict() for field in self.fieldsSet],
            'state': self.state,
            'playersNumber': self.playersNumber,
            'players': [player.toDict() for player in self.players],
            'playersData': {playerId: data.toDict() for (playerId, data) in self.playersData.items()},
            'moveOwner': self.moveOwner.toDict()
        }