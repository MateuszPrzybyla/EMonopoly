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
from utils.eMonopoly import GAME_FIELDS, FieldType, MoveType


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
        self.addPlayerMove(self.players[0].id)

    def popMove(self, player, moveType):
        expectedMove = self.nextMoves[-1]
        # niektore ruchy moga byc wykonane w dowolnym momencie
        # stawianie budynkow, sprzedaz nieruchomosci, zastaw hipoteczny, handel z innymi
        if player in expectedMove.eligiblePlayers and expectedMove.moveType == moveType:
            return self.nextMoves.pop()

    def doDiceMove(self, playerId, expectedMove):
        player = self.getPlayerById(playerId)
        # dices = (random.randint(1, 6), random.randint(1, 6), player.name)
        dices = (5, 5, player.name) if not self.lastDice else (6, 6, player.name)
        self.lastDice = (dices[0], dices[1])
        diceSum = dices[0] + dices[1]
        newPosition = self.playersData[playerId].movePlayer(diceSum)
        if dices[0] == dices[1]:
            if expectedMove.moveData['roll'] < 3:
                self.nextMoves.append(GameMove.diceMove(player, expectedMove.moveData['roll'] + 1))
            else:
                self.goToJail(playerId)
                return dices
        else:
            self.checkStartBonus(playerId)
        self.performPlayerOnFieldAction(self.fieldsSet[newPosition], playerId, diceSum)
        return dices

    def checkStartBonus(self, playerId):
        startPasses = self.playersData[playerId].calculateStartPasses()
        self.playersData[playerId].addBalance(startPasses * MonopolyGame.START_PASS_BONUS)

    def performPlayerOnFieldAction(self, field, playerId, diceResult):
        player = self.getPlayerById(playerId)
        if field.model.isBuyable() and not field.owner:
            self.nextMoves.append(GameMove.buyOptionMove(player, field.model))
        elif field.owner and field.owner != playerId and not field.mortgage:
            target = self.getPlayerById(field.owner)
            self.nextMoves.append(GameMove.feeMove(player, target, field, diceResult))
        elif field.model.number == GO_TO_JAIL_POSITION:
            self.goToJail(playerId)
        elif field.model.type == FieldType.TAX:
            self.nextMoves.append(GameMove.feeMove(player, self.getPlayerById(ClientPlayer.BANK_ID), field, diceResult))
        elif field.model.type == FieldType.DRAW_CHANCE:
            self.nextMoves.append(GameMove.draw(player, 'CHANCE'))

    def goToJail(self, playerId):
        self.playersData[playerId].goToJail()
        self.popMove(self.getPlayerById(playerId), MoveType.DICE)

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
            totalFee = fee if expectedMoveData['targetPlayer']['id'] is not ClientPlayer.ALL_ID \
                else fee * (len(self.players) - 1)
            if self.playersData[playerId].balance < totalFee:
                player = self.getPlayerById(playerId)
                targetPlayer = self.getPlayerById(expectedMoveData['targetPlayer']['id'])
                self.nextMoves.append(GameMove.feeMove(player, targetPlayer, field, sum(self.lastDice)))
            else:
                if expectedMoveData['targetPlayer']['id'] == ClientPlayer.ALL_ID:
                    targetPlayers = filter(lambda player: player.id != playerId, self.players)
                else:
                    targetPlayers = [self.getPlayerById(expectedMoveData['targetPlayer']['id'])]
                self.playersData[playerId].addBalance(-fee * len(targetPlayers))
                for targetPlayer in targetPlayers:
                    if targetPlayer.id > 0:
                        self.playersData[targetPlayer.id].addBalance(fee)
        else:
            pass  # TODO - go bankrupt

    def doJailMove(self, playerId, moveDetails):
        player = self.getPlayerById(playerId)
        playerData = self.playersData[playerId]
        if moveDetails['method'] == 'pay' and playerData.turnsInJailLeft() > 0:
            if playerData.balance < JAIL_QUIT_FEE:
                self.nextMoves.append(
                    GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
            else:
                playerData.addBalance(-JAIL_QUIT_FEE)
                playerData.quitJail()
                self.addPlayerMove(playerId)
        elif moveDetails['method'] == 'card':
            if playerData.hasJailCard():
                playerData.quitJail()
                self.addPlayerMove(playerId)
            else:
                self.nextMoves.append(
                    GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
        elif moveDetails['method'] == 'dice':
            dices = (random.randint(1, 6), random.randint(1, 6), player.name)
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
        self.addPlayerMove(self.players[nextToRoll].id)

    def startFieldBidding(self, field, onBiddingComplete):
        self.biddingManager = server.Bidding.BiddingManager(self.players, self.playersData, self.nextMoves, field,
                                                            onBiddingComplete, self.biddingQueue, BID_TIME_SECONDS,
                                                            self.waitForBidMoveEvent)
        self.waitForBidMoveEvent.clear()
        self.biddingManager.start()
        self.waitForBidMoveEvent.wait()

    def doBidMove(self, playerId, moveDetails):
        self.waitForBidMoveEvent.clear()
        self.biddingQueue.put(Bid(self.getPlayerById(playerId), moveDetails['value']))
        self.waitForBidMoveEvent.wait()

    def doDrawMove(self, playerId, expectedMove):
        if expectedMove.moveData['type'] == 'CHANCE':
            card = self.chanceCards.pop()
            card.handler(self, playerId)
            self.chanceCards.insert(0, card)

    def addPlayerMove(self, playerId):
        player = self.getPlayerById(playerId)
        self.nextMoves.append(GameMove.endMove(player))
        playerData = self.playersData[playerId]
        if playerData.isInJail():
            self.nextMoves.append(
                GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
        else:
            self.nextMoves.append(GameMove.diceMove(player))

    def getPlayerById(self, playerId):
        if playerId == ClientPlayer.BANK_ID:
            return ClientPlayer.bankPlayer()
        if playerId == ClientPlayer.ALL_ID:
            return ClientPlayer.allPlayer()
        return self.players[self.getPlayerNo(playerId)]

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