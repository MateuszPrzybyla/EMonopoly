from Queue import Queue
from copy import deepcopy
import random
from threading import Event

import server.Bidding
from server.Bidding import Bid
from server.ClientPlayer import ClientPlayer
from server.monopoly.ChanceCards import CHANCE_CARDS
from server.monopoly.GameField import GameField
from server.monopoly.GameMove import GameMove
from server.monopoly.PlayerData import PlayerData
from utils.eMonopoly import GAME_FIELDS, FieldType


__author__ = 'mateusz'

GO_TO_JAIL_POSITION = 30
JAIL_QUIT_FEE = 50
BID_TIME_SECONDS = 10


class GameState(object):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'


class MonopolyGame(object):
    START_PASS_BONUS = 200

    def __init__(self, id, playersNumber, players):
        self.id = id
        self.fieldsSet = [GameField(FIELD_MODEL) for FIELD_MODEL in GAME_FIELDS]
        for field in self.fieldsSet:
            field.fieldSet = self.fieldsSet
        self.state = GameState.NEW
        self.playersNumber = playersNumber
        self.players = players
        self.bankPlayer = ClientPlayer.bankPlayer()
        self.startRequest = set()
        self.playersData = dict()
        self.nextMoves = list()
        self.biddingQueue = Queue()
        self.biddingManager = None
        self.waitForBidMoveEvent = Event()
        self.lastDice = None
        self.chanceCards = deepcopy(CHANCE_CARDS)
        random.shuffle(self.chanceCards)

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
        self.lastDice = (dices[0], dices[1])
        diceSum = dices[0] + dices[1]
        newPosition = self.playersData[playerId].movePlayer(diceSum)
        if dices[0] == dices[1]:
            if expectedMove.moveData['roll'] < 3 and newPosition != GO_TO_JAIL_POSITION:
                self.nextMoves.append(GameMove.diceMove(self.players[playerNo], expectedMove.moveData['roll'] + 1))
            else:
                self.playersData[playerId].goToJail()
                return dices
        else:
            self.checkStartBonus(playerId)
        self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId, diceSum)
        return dices

    def checkStartBonus(self, playerId):
        startPasses = self.playersData[playerId].calculateStartPasses()
        self.playersData[playerId].addBalance(startPasses * MonopolyGame.START_PASS_BONUS)

    def performPlayerOnFieldAction(self, field, playerId, diceResult):
        playerNo = self.getPlayerNo(playerId)
        if field.model.isBuyable() and not field.owner:
            self.nextMoves.append(GameMove.buyOptionMove(self.players[playerNo], field.model))
        elif field.owner and field.owner != playerId and not field.mortgage:
            targetNo = self.getPlayerNo(field.owner)
            self.nextMoves.append(GameMove.feeMove(self.players[playerNo], self.players[targetNo], field, diceResult))
        elif field.model.number == GO_TO_JAIL_POSITION:
            self.playersData[playerId].goToJail()
        elif field.model.type == FieldType.TAX:
            self.nextMoves.append(GameMove.feeMove(self.players[playerNo], self.bankPlayer, field, diceResult))
        elif field.model.type == FieldType.DRAW_CHANCE:
            self.nextMoves.append(GameMove.draw(self.players[playerNo], 'CHANCE'))

    def estateBidEnded(self, bidCallback):
        def combinedCallback(biddingResult):
            winner = biddingResult.winningBid.owner
            biddingResult.field.owner = winner.id
            self.playersData[winner.id].addBalance(-biddingResult.winningBid.value)
            bidCallback(self)
        return combinedCallback

    def doBuyEstate(self, playerId, moveDetails, bidCallback):
        field = self.fieldsSet[moveDetails['fieldNo']]
        if moveDetails['decision']:
            field.owner = playerId
            self.playersData[playerId].addBalance(-field.model.value)
        else:
            self.startFieldBidding(field, self.estateBidEnded(bidCallback))

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
                if expectedMoveData['targetPlayer']['id'] != ClientPlayer.BANK_ID:
                    self.playersData[expectedMoveData['targetPlayer']['id']].addBalance(fee)
        else:
            pass  # TODO - go bankrupt

    def doJailMove(self, playerId, moveDetails):
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
            self.lastDice = (dices[0], dices[1])
            if dices[0] == dices[1] or playerData.turnsInJailLeft() == 0:
                playerData.quitJail()
                newPosition = playerData.movePlayer(dices[0] + dices[1])
                self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId, dices[0] + dices[1])
            if playerData.turnsInJailLeft() == 0:
                playerData.addBalance(-JAIL_QUIT_FEE)
            return dices

    def doEndMove(self, playerId):
        playerNo = self.getPlayerNo(playerId)
        nextToRoll = (playerNo + 1) % self.playersNumber
        self.playersData[playerId].resetMove()
        self.playersData[playerId].countJailTurns()
        self.addPlayerMove(nextToRoll)

    def startFieldBidding(self, field, onBiddingComplete):
        self.biddingManager = server.Bidding.BiddingManager(self.players, self.playersData, self.nextMoves, field,
                                                            onBiddingComplete, self.biddingQueue, BID_TIME_SECONDS,
                                                            self.waitForBidMoveEvent)
        self.waitForBidMoveEvent.clear()
        self.biddingManager.start()
        print "Start bidding - wait"
        self.waitForBidMoveEvent.wait()
        print "Start bidding - wait finished"

    def doBidMove(self, playerId, moveDetails):
        self.waitForBidMoveEvent.clear()
        self.biddingQueue.put(Bid(self.players[self.getPlayerNo(playerId)], moveDetails['value']))
        print "Bid move - wait"
        self.waitForBidMoveEvent.wait()
        print "Bid move - wait finished"

    def doDrawMove(self, playerId, expectedMove):
        if expectedMove.moveData['type'] == 'CHANCE':
            card = self.chanceCards.pop()
            card.handler(self, playerId)
            self.chanceCards.insert(0, card)

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