import random
from utils.eMonopoly import GAME_FIELDS, MoveType, FieldType

__author__ = 'mateusz'


class GameState(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'


class PlayerData(object):
    def __init__(self, fieldPosition=0, startBalance=1500):
        self.fieldPosition = fieldPosition
        self.singleMoveFields = []
        self.balance = startBalance
        self.buildings = dict()

    def movePlayer(self, moveSize):
        self.fieldPosition += moveSize
        self.fieldPosition %= 40
        self.singleMoveFields.append(self.fieldPosition)
        return self.fieldPosition

    def toDict(self):
        return {
            'position': self.fieldPosition,
            'singleMoveFields': self.singleMoveFields,
            'balance': self.balance,
            'buildings': self.buildings
        }


class GameMove(object):
    def __init__(self, eligiblePlayers, moveType, moveData=None):
        self.eligiblePlayers = eligiblePlayers
        self.moveType = moveType
        self.moveData = moveData

    def toDict(self):
        if self.moveData:
            return {
                'eligiblePlayers': [player.toDict() for player in self.eligiblePlayers],
                'moveType': self.moveType,
                'moveData': self.moveData
            }
        else:
            return {
                'eligiblePlayers': [player.toDict() for player in self.eligiblePlayers],
                'moveType': self.moveType
            }

    @staticmethod
    def diceMove(player, rollNumber=1):
        return GameMove([player], MoveType.DICE, {'roll': rollNumber})

    @staticmethod
    def buyOptionMove(player, field):
        return GameMove([player], MoveType.BUY, {
            'fieldNo': field.number,
            'value': field.value
        })

    @staticmethod
    def endMove(player):
        return GameMove([player], MoveType.END)

    def __str__(self):
        return "TYPE: %s, PLAYERS: %s, MOVE_DATA: %s" % (
            self.moveType, [player.name for player in self.eligiblePlayers], str(self.moveData) )


class GameField(object):
    def __init__(self, model):
        self.model = model
        self.owner = None
        self.houses = 0
        self.mortgage = False

    def isDefault(self):
        return self.owner == None and self.houses == 0 and not self.mortgage

    def toDictStateOnly(self):
        return {
            'owner': self.owner,
            'houses': self.houses,
            'mortgage': self.mortgage
        }


class MonopolyGame(object):
    def __init__(self, id, playersNumber, players):
        self.id = id
        self.fieldsSet = [GameField(FIELD_MODEL) for FIELD_MODEL in GAME_FIELDS]
        self.state = GameState.NEW
        self.playersNumber = playersNumber
        self.players = players
        self.startRequest = set()
        self.playersData = dict()
        self.nextMoves = list()

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
        self.addNextPlayerMoves(0)
        self.playersData = {player.id: PlayerData(0, 1500) for player in self.players}

    def acceptMove(self, player, moveType):
        expectedMove = self.nextMoves[-1]
        # niektore ruchy moga byc wykonane w dowolnym momencie
        # stawianie budynkow, sprzedaz nieruchomosci, zastaw hipoteczny, handel z innymi
        if player in expectedMove.eligiblePlayers and expectedMove.moveType == moveType:
            return self.nextMoves.pop()

    def doDiceMove(self, playerId, expectedMove):
        dices = (random.randint(1, 6), random.randint(1, 6))
        diceSum = dices[0] + dices[1]
        playerNo = self.getPlayerNo(playerId)
        if dices[0] == dices[1]:
            # add check for 3 doubles in a row (go to jail)
            if expectedMove.moveData['roll'] < 3:
                self.nextMoves.append(GameMove.diceMove(self.players[playerNo], expectedMove.moveData['roll'] + 1))
            else:  # go to jail
                pass
        else:  # collect go through start bonus
            pass
        newPosition = self.playersData[playerId].movePlayer(diceSum)
        self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId)
        return dices

    def performPlayerOnFieldAction(self, field, playerId):
        playerNo = self.getPlayerNo(playerId)
        if field.model.isBuyable() and not field.owner:
            self.nextMoves.append(GameMove.buyOptionMove(self.players[playerNo], field.model))

    def doBuyEstate(self, playerId, moveDetails):
        if moveDetails['decision']:
            field = self.fieldsSet[moveDetails['fieldNo']]
            field.owner = playerId
            self.playersData[playerId].balance -= field.model.value

    def doEndMove(self, playerId):
        playerNo = self.getPlayerNo(playerId)
        nextToRoll = (playerNo + 1) % self.playersNumber
        playerData = self.playersData[playerId]
        playerData.singleMoveFields = [playerData.fieldPosition]
        self.addNextPlayerMoves(nextToRoll)

    def sendPlayerToJail(self, playerId):
        pass

    def addNextPlayerMoves(self, playerNo):
        self.nextMoves.append(GameMove.endMove(self.players[playerNo]))
        self.nextMoves.append(GameMove.diceMove(self.players[playerNo]))

    def getPlayerNo(self, playerId):
        for i, player in enumerate(self.players):
            if player.id == int(playerId):
                return i

    def toDict(self):
        return {
            'id': self.id,
            'fields': [field.model.toDict() for field in self.fieldsSet],
            'state': self.state,
            'playersNumber': self.playersNumber,
            'players': [player.toDict() for player in self.players],
            'playersData': {playerId: data.toDict() for (playerId, data) in self.playersData.items()},
            'nextMove': self.nextMoves[-1].toDict()
        }

    def toDictStateOnly(self):
        return {
            'state': self.state,
            'fields': {field.model.number: field.toDictStateOnly() for field in self.fieldsSet
                       if not field.isDefault()},
            'playersData': {playerId: data.toDict() for (playerId, data) in self.playersData.items()},
            'nextMove': self.nextMoves[-1].toDict()
        }