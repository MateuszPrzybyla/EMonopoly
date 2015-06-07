import random

from utils.eMonopoly import GAME_FIELDS, MoveType


__author__ = 'mateusz'

JAIL_POSITION = 10
GO_TO_JAIL_POSITION = 30
JAIL_QUIT_FEE = 50


class GameState(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'


class PlayerData(object):
    def __init__(self, fieldPosition=0, startBalance=1500):
        self.fieldPosition = fieldPosition
        self.singleMoveChanges = []
        self.singleMoveStart = fieldPosition
        self.balance = startBalance
        self.inJailTurns = 0
        self.inJail = False
        self.buildings = dict()

    def movePlayer(self, moveSize):
        self.fieldPosition += moveSize
        self.fieldPosition %= 40
        self.singleMoveChanges.append(moveSize)
        return self.fieldPosition

    def movePlayerToField(self, fieldNumber, forward=True):
        change = (fieldNumber - self.fieldPosition + 40) % 40
        if not forward:
            change = 40 - change
        self.singleMoveChanges.append(change)
        self.fieldPosition = fieldNumber
        return self.fieldPosition

    def resetMove(self):
        self.singleMoveChanges = []
        self.singleMoveStart = self.fieldPosition

    def calculateStartPasses(self):
        startPasses = 0
        previous = self.singleMoveStart
        for change in self.singleMoveChanges:
            if previous + change >= 40 and change > 0:
                startPasses += 1
            previous = (previous + change + 40) % 40
        return startPasses

    def addBalance(self, change):
        self.balance += change

    def goToJail(self):
        self.inJailTurns = 0
        self.inJail = True
        self.fieldPosition = JAIL_POSITION
        self.resetMove()

    def isInJail(self):
        return self.inJail

    def countJailTurns(self):
        if self.inJail:
            self.inJailTurns += 1

    def turnsInJailLeft(self):
        if not self.inJail:
            return 0
        return 3 - self.inJailTurns

    def quitJail(self):
        self.inJail = False
        self.inJailTurns = 0

    def hasJailCard(self):  # TODO add field
        return False

    def toDict(self):
        return {
            'position': self.fieldPosition,
            'singleMoveChanges': self.singleMoveChanges,
            'singleMoveStart': self.singleMoveStart,
            'balance': self.balance,
            'buildings': self.buildings,
            'inJail': self.inJail
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
    def feeMove(player, targetPlayer, field):
        return GameMove([player], MoveType.FEE, {
            'targetPlayer': targetPlayer.toDict(),
            'fieldNo': field.model.number,
            'fee': field.getFee()
        })

    @staticmethod
    def inJail(player, turnsInJailLeft, hasJailCard):
        return GameMove([player], MoveType.JAIL, {
            'turnsLeft': turnsInJailLeft,
            'hasCard': hasJailCard
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
        self.monopoly = False

    def isDefault(self):
        return not self.owner and self.houses == 0 and not self.mortgage

    def getFee(self):  # TODO calculate it more seriously
        return 163

    def toDictStateOnly(self):
        return {
            'owner': self.owner,
            'houses': self.houses,
            'mortgage': self.mortgage
        }


class MonopolyGame(object):
    START_PASS_BONUS = 200

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
        self.playersData = {player.id: PlayerData(0, 1500) for player in self.players}
        self.addPlayerMove(0)

    def acceptMove(self, player, moveType):
        expectedMove = self.nextMoves[-1]
        # niektore ruchy moga byc wykonane w dowolnym momencie
        # stawianie budynkow, sprzedaz nieruchomosci, zastaw hipoteczny, handel z innymi
        if player in expectedMove.eligiblePlayers and expectedMove.moveType == moveType:
            return self.nextMoves.pop()

    def doDiceMove(self, playerId, expectedMove):
        playerNo = self.getPlayerNo(playerId)
        dices = (random.randint(1, 6), random.randint(1, 6), self.players[playerNo].name)
        diceSum = dices[0] + dices[1]
        newPosition = self.playersData[playerId].movePlayer(diceSum)
        if dices[0] == dices[1]:
            if expectedMove.moveData['roll'] < 3 and newPosition != GO_TO_JAIL_POSITION:
                self.nextMoves.append(GameMove.diceMove(self.players[playerNo], expectedMove.moveData['roll'] + 1))
            else:
                self.playersData[playerId].goToJail()
                return dices
        else:
            startPasses = self.playersData[playerId].calculateStartPasses()
            self.playersData[playerId].addBalance(startPasses * MonopolyGame.START_PASS_BONUS)
        self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId)
        return dices

    def performPlayerOnFieldAction(self, field, playerId):
        playerNo = self.getPlayerNo(playerId)
        if field.model.isBuyable() and not field.owner:
            self.nextMoves.append(GameMove.buyOptionMove(self.players[playerNo], field.model))
        elif field.owner and field.owner != playerId and not field.mortgage:
            targetNo = self.getPlayerNo(field.owner)
            self.nextMoves.append(GameMove.feeMove(self.players[playerNo], self.players[targetNo], field))
        elif field.model.number == GO_TO_JAIL_POSITION:
            self.playersData[playerId].goToJail()

    def doBuyEstate(self, playerId, moveDetails):
        if moveDetails['decision']:
            field = self.fieldsSet[moveDetails['fieldNo']]
            field.owner = playerId
            self.playersData[playerId].addBalance(-field.model.value)
        else:
            pass  # TODO licytacja

    def doPayFee(self, playerId, moveDetails, expectedMove):
        if moveDetails['pay']:
            expectedMoveData = expectedMove.moveData
            field = self.fieldsSet[expectedMoveData['fieldNo']]
            fee = expectedMoveData['fee']
            if self.playersData[playerId].balance < fee:
                playerNo = self.getPlayerNo(playerId)
                targetNo = self.getPlayerNo(field.owner)
                self.nextMoves.append(GameMove.feeMove(self.players[playerNo], self.players[targetNo], field))
            else:
                self.playersData[playerId].addBalance(-fee)
                self.playersData[expectedMoveData['targetPlayer']['id']].addBalance(fee)
        else:
            pass  # TODO - go bankrupt

    def doJailMove(self, playerId, moveDetails, expectedMove):
        playerNo = self.getPlayerNo(playerId)
        playerData = self.playersData[playerId]
        if moveDetails['method'] == 'pay' and playerData.turnsInJailLeft() > 0:
            if playerData.balance < JAIL_QUIT_FEE:
                self.nextMoves.append(
                    GameMove.inJail(self.players[playerNo], playerData.turnsInJailLeft(), playerData.hasJailCard()))
            else:
                playerData.addBalance(-JAIL_QUIT_FEE)
                playerData.quitJail()
                self.addPlayerMove(playerNo)
        elif moveDetails['method'] == 'card':
            if playerData.hasJailCard():
                playerData.quitJail()
                self.addPlayerMove(playerNo)
            else:
                self.nextMoves.append(
                    GameMove.inJail(self.players[playerNo], playerData.turnsInJailLeft(), playerData.hasJailCard()))
        elif moveDetails['method'] == 'dice':
            dices = (random.randint(1, 6), random.randint(1, 6), self.players[playerNo].name)
            if dices[0] == dices[1] or playerData.turnsInJailLeft() == 0:
                playerData.quitJail()
                newPosition = playerData.movePlayer(dices[0] + dices[1])
                self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId)
            if playerData.turnsInJailLeft() == 0:
                playerData.addBalance(-JAIL_QUIT_FEE)
            return dices

    def doEndMove(self, playerId):
        playerNo = self.getPlayerNo(playerId)
        nextToRoll = (playerNo + 1) % self.playersNumber
        self.playersData[playerId].resetMove()
        self.playersData[playerId].countJailTurns()
        self.addPlayerMove(nextToRoll)

    def addPlayerMove(self, playerNo):
        playerId = self.players[playerNo].id
        self.nextMoves.append(GameMove.endMove(self.players[playerNo]))
        playerData = self.playersData[playerId]
        if playerData.isInJail():
            self.nextMoves.append(
                GameMove.inJail(self.players[playerNo], playerData.turnsInJailLeft(), playerData.hasJailCard()))
        else:
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