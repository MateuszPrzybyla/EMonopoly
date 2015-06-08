from Queue import Queue
from copy import deepcopy
import random
from threading import Event, Lock

import server.Bidding
from server.Bidding import Bid
from server.ClientPlayer import ClientPlayer
from server.monopoly.ChanceCards import CHANCE_CARDS, COMMUNITY_CARDS
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
    ENDED = 'ENDED'


class MonopolyGame(object):
    START_PASS_BONUS = 200

    def __init__(self, id, playersNumber, players):
        self.id = id
        self.fieldsSet = [GameField(FIELD_MODEL) for FIELD_MODEL in GAME_FIELDS]
        for field in self.fieldsSet:
            field.fieldSet = self.fieldsSet
        self.state = GameState.NEW
        self.playersNumber = playersNumber
        self.allPlayers = deepcopy(players)
        self.activePlayers = players
        self.lastPlayerMove = None
        self.bankPlayer = ClientPlayer.bankPlayer()
        self.startRequest = set()
        self.playersData = dict()
        self.nextMoves = list()
        self.nextMovesLock = Lock()
        self.biddingQueue = Queue()
        self.biddingManager = None
        self.waitForBidMoveEvent = Event()
        self.lastDice = None
        self.chanceCards = deepcopy(CHANCE_CARDS)
        self.communityCards = deepcopy(COMMUNITY_CARDS)
        random.shuffle(self.chanceCards)
        random.shuffle(self.communityCards)

    def addStartRequest(self, player):
        alreadyExists = player in self.startRequest
        self.startRequest.add(player)
        return not alreadyExists, self.playersLeftToStart()

    def playersLeftToStart(self):
        return self.playersNumber - len(self.startRequest)

    def isReadyToStart(self):
        return len(self.startRequest) == self.playersNumber and self.state != GameState.ACTIVE

    def isActive(self):
        return self.state == GameState.ACTIVE

    def startGame(self):
        if self.state == GameState.ACTIVE:
            return
        self.state = GameState.ACTIVE
        self.playersData = {player.id: PlayerData(0, 500) for player in self.activePlayers}
        self.addPlayerMove(self.activePlayers[0].id)

    def getHeadMove(self, player, moveType, pop=True):
        with self.nextMovesLock:
            if len(self.nextMoves) > 0:
                expectedMove = self.nextMoves[-1]
                if player in expectedMove.eligiblePlayers and expectedMove.moveType == moveType and pop:
                    return self.nextMoves.pop()

    def clearPlayerMoves(self, playerId):
        with self.nextMovesLock:
            print "Clearing player moves, before (%d): %s" % (
                len(self.nextMoves), [str(move) for move in reversed(self.nextMoves)])
            self.nextMoves = filter(lambda move: any(player.id != playerId for player in move.eligiblePlayers),
                                    self.nextMoves)
            print "Clearing player moves, after (%d): %s" % (
                len(self.nextMoves), [str(move) for move in reversed(self.nextMoves)])

    def addMove(self, move):
        with self.nextMovesLock:
            self.nextMoves.append(move)

    def doDiceMove(self, playerId, expectedMove):
        player = self.getPlayerById(playerId)
        dices = (random.randint(1, 6), random.randint(1, 6), player.name)
        # dices = (5, 5, player.name) if not self.lastDice else (6, 6, player.name)
        self.lastDice = (dices[0], dices[1])
        diceSum = dices[0] + dices[1]
        newPosition = self.playersData[playerId].movePlayer(diceSum)
        if dices[0] == dices[1]:
            if expectedMove.moveData['roll'] < 3:
                self.addMove(GameMove.diceMove(player, expectedMove.moveData['roll'] + 1))
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

    def performPlayerOnFieldAction(self, field, playerId, diceResult, fixedCoeff=None):
        player = self.getPlayerById(playerId)
        if field.model.isBuyable() and not field.owner:
            self.addMove(GameMove.buyOptionMove(player, field.model))
        elif field.owner and field.owner != playerId and not field.mortgage:
            target = self.getPlayerById(field.owner)
            self.addMove(GameMove.feeMove(player, target, field, diceResult, fixedCoeff=fixedCoeff))
        elif field.model.number == GO_TO_JAIL_POSITION:
            self.goToJail(playerId)
        elif field.model.type == FieldType.TAX:
            self.addMove(GameMove.feeMove(player, self.getPlayerById(ClientPlayer.BANK_ID),
                                          field, diceResult, fixedCoeff=fixedCoeff))
        elif field.model.type == FieldType.DRAW_CHANCE:
            self.addMove(GameMove.draw(player, 'CHANCE'))
        elif field.model.type == FieldType.DRAW_COMMUNITY:
            self.addMove(GameMove.draw(player, 'COMMUNITY'))

    def goToJail(self, playerId):
        self.playersData[playerId].goToJail()
        self.getHeadMove(self.getPlayerById(playerId), MoveType.DICE)

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
            if self.playersData[playerId].balance >= field.model.value:
                field.owner = playerId
                self.playersData[playerId].addBalance(-field.model.value)
            else:
                self.addMove(GameMove.buyOptionMove(self.getPlayerById(playerId), field.model))
        else:
            self.startFieldBidding(field, self.estateBidEnded(bidCallback))

    def doPayFee(self, playerId, moveDetails, expectedMove, bidCallback):
        if moveDetails['pay']:
            expectedMoveData = expectedMove.moveData
            fee = expectedMoveData['fee']
            totalFee = fee if expectedMoveData['targetPlayer']['id'] is not ClientPlayer.ALL_ID \
                else fee * (len(self.activePlayers) - 1)
            if self.playersData[playerId].balance < totalFee:
                player = self.getPlayerById(playerId)
                targetPlayer = self.getPlayerById(expectedMoveData['targetPlayer']['id'])
                self.addMove(GameMove.feeMove(player, targetPlayer, fee=fee, diceResult=sum(self.lastDice)))
            else:
                if expectedMoveData['targetPlayer']['id'] == ClientPlayer.ALL_ID:
                    targetPlayers = filter(lambda player: player.id != playerId, self.activePlayers)
                else:
                    targetPlayers = [self.getPlayerById(expectedMoveData['targetPlayer']['id'])]
                self.playersData[playerId].addBalance(-fee * len(targetPlayers))
                for targetPlayer in targetPlayers:
                    if targetPlayer.id > 0:
                        self.playersData[targetPlayer.id].addBalance(fee)
        else:
            self.goBankrupt(playerId, None, bidCallback)

    def doJailMove(self, playerId, moveDetails):
        player = self.getPlayerById(playerId)
        playerData = self.playersData[playerId]
        if moveDetails['method'] == 'pay' and playerData.turnsInJailLeft() > 0:
            if playerData.balance < JAIL_QUIT_FEE:
                self.addMove(GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
            else:
                playerData.addBalance(-JAIL_QUIT_FEE)
                playerData.quitJail()
                self.addPlayerMove(playerId)
        elif moveDetails['method'] == 'card':
            if playerData.hasJailCard():
                playerData.jailCards[0].use(self, playerId)
                self.addPlayerMove(playerId)
            else:
                self.addMove(GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
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
        nextToRoll = (playerNo + 1) % len(self.activePlayers)
        self.playersData[playerId].resetMove()
        self.playersData[playerId].countJailTurns()
        self.addPlayerMove(self.activePlayers[nextToRoll].id)

    def startFieldBidding(self, field, onBiddingComplete):
        self.biddingManager = server.Bidding.BiddingManager(self.activePlayers, self.playersData, self.nextMoves,
                                                            self.nextMovesLock, field, onBiddingComplete,
                                                            self.biddingQueue, BID_TIME_SECONDS,
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
            deck = self.chanceCards
        elif expectedMove.moveData['type'] == 'COMMUNITY':
            deck = self.communityCards
        else:
            return
        card = deck.pop()
        print "Player %d draws %s card: %s" % (playerId, expectedMove.moveData['type'], card.text)
        card.handle(self, playerId)
        if not card.staysWithPlayer():
            deck.insert(0, card)

    def doHouseMove(self, playerId, moveDetails):
        if moveDetails['action'] == 'buy':
            self.doBuyHouse(playerId, moveDetails['fieldNo'])
        elif moveDetails['action'] == 'sell':
            self.doSellHouse(playerId, moveDetails['fieldNo'])

    def doBuyHouse(self, playerId, fieldNo):
        field = self.fieldsSet[fieldNo]
        if not field.canBuildHouse(playerId):
            return
        cost = field.getHouseCost()
        if cost == 0 or self.playersData[playerId].balance < cost:
            return
        self.playersData[playerId].addBalance(-cost)
        field.houses += 1

    def doSellHouse(self, playerId, fieldNo):
        field = self.fieldsSet[fieldNo]
        if not field.canSellHouse(playerId):
            return
        soldValue = field.sellHouse()
        self.playersData[playerId].addBalance(soldValue)

    def doDebtMove(self, playerId, moveDetails, bidCallback):
        if moveDetails['paid']:
            if self.playersData[playerId].balance < 0:
                self.addMove(GameMove.payDebt(self.getPlayerById(playerId)))
            else:
                self.addPlayerMove(playerId)
        else:
            self.goBankrupt(playerId, None, bidCallback)

    def notifyPlayerLeft(self, playerId, getGameStateCallback):
        if self.getHeadMove(self.getPlayerById(playerId), MoveType.FEE, pop=False) is not None:
            self.goBankrupt(playerId, None, getGameStateCallback)  # TODO pass fee player
        else:
            self.goBankrupt(playerId, None, getGameStateCallback)

    def playerBankruptBiddingComplete(self, playerId, getGameStateCallback):
        def combinedCallback(biddingResult):
            winner = biddingResult.winningBid.owner
            biddingResult.field.owner = winner.id
            self.playersData[winner.id].addBalance(-biddingResult.winningBid.value)
            playersFields = filter(lambda field: field.owner == playerId, self.fieldsSet)
            if len(playersFields) > 0:
                self.startFieldBidding(playersFields[0],
                                       self.playerBankruptBiddingComplete(playerId, getGameStateCallback))
            getGameStateCallback(self)

        return combinedCallback

    def goBankrupt(self, playerId, possessionTarget, getGameStateCallback):
        soldValue = 0
        playersFields = filter(lambda field: field.owner == playerId, self.fieldsSet)
        for field in playersFields:
            soldValue += field.clearHouses()
        self.playersData[playerId].addBalance(soldValue)
        self.doEndMove(playerId)
        self.clearPlayerMoves(playerId)
        self.activePlayers = [player for player in self.activePlayers if player.id != playerId]
        if possessionTarget is not None:
            pass  # przekaz wszystko temu komu trzeba
        elif possessionTarget is None and len(self.activePlayers) > 1 and len(playersFields) > 0:
            self.startFieldBidding(playersFields[0], self.playerBankruptBiddingComplete(playerId, getGameStateCallback))
        elif len(self.activePlayers) == 1:
            self.addMove(GameMove.winMove(self.allPlayers, self.activePlayers[0]))
            self.state = GameState.ENDED
            getGameStateCallback(self)


    def doMortgageMove(self, playerId, moveDetails):
        if moveDetails['action'] == 'lift':
            self.doMortgageLift(playerId, moveDetails['fieldNo'])
        elif moveDetails['action'] == 'sell':
            self.doMortgageSell(playerId, moveDetails['fieldNo'])

    def doMortgageLift(self, playerId, fieldNo):
        field = self.fieldsSet[fieldNo]
        if not field.canLiftMortgage(playerId):
            return
        mortgageValue = field.getMortgageBuyValue()
        if self.playersData[playerId].balance < mortgageValue:
            return
        field.mortgage = False
        self.playersData[playerId].addBalance(-mortgageValue)

    def doMortgageSell(self, playerId, fieldNo):
        field = self.fieldsSet[fieldNo]
        if not field.canDoMortgage(playerId):
            return
        mortgageValue = field.getMortgageSellValue()
        field.mortgage = True
        self.playersData[playerId].addBalance(mortgageValue)

    def addPlayerMove(self, playerId):
        player = self.getPlayerById(playerId)
        self.addMove(GameMove.endMove(player))
        playerData = self.playersData[playerId]
        if playerData.balance < 0:
            self.addMove(GameMove.payDebt(player))
        if playerData.isInJail():
            self.addMove(GameMove.inJail(player, playerData.turnsInJailLeft(), playerData.hasJailCard()))
        else:
            self.addMove(GameMove.diceMove(player))

    def getPlayerById(self, playerId):
        if playerId == ClientPlayer.BANK_ID:
            return ClientPlayer.bankPlayer()
        if playerId == ClientPlayer.ALL_ID:
            return ClientPlayer.allPlayer()
        return self.activePlayers[self.getPlayerNo(playerId)]

    def getPlayerNo(self, playerId):
        for i, player in enumerate(self.activePlayers):
            if player.id == int(playerId):
                return i

    def isPlayerActive(self, playerId):
        return any(player.id == playerId for player in self.activePlayers)

    def toDict(self):
        return {
            'id': self.id,
            'fields': [field.model.toDict() for field in self.fieldsSet],
            'state': self.state,
            'playersNumber': self.playersNumber,
            'players': [player.toDict() for player in self.activePlayers],
            'playersData': {playerId: data.toDict() for (playerId, data) in self.playersData.items()},
            'nextMove': self.nextMoves[-1].toDict()
        }

    def toDictStateOnly(self):
        return {
            'state': self.state,
            'fields': {field.model.number: field.toDictStateOnly() for field in self.fieldsSet
                       if not field.isDefault()},
            'playersData': {playerId: data.toDict() for (playerId, data) in self.playersData.items()
                            if self.isPlayerActive(playerId)},
            'nextMove': self.nextMoves[-1].toDict()
        }