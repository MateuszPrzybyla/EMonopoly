from server.ClientPlayer import ClientPlayer
from server.monopoly.GameMove import GameMove

__author__ = 'mateusz'


def positionChange(targetPosition=None, change=None):
    def handler(card, game, playerId):
        playerData = game.playersData[playerId]
        if targetPosition is not None:
            playerData.movePlayerToField(targetPosition)
        elif change is not None:
            playerData.movePlayer(change)
        else:
            return
        game.checkStartBonus(playerId)
        game.performPlayerOnFieldAction(game.fieldsSet[playerData.fieldPosition], playerId, sum(game.lastDice))

    return handler


def advanceToNearest(*fields):
    def handler(card, game, playerId):
        position = game.playersData[playerId].fieldPosition
        nearestDiff = min((40 + field - position) % 40 for field in fields)
        game.playersData[playerId].movePlayer(nearestDiff)
        game.checkStartBonus(playerId)
        newPosition = game.playersData[playerId].fieldPosition
        game.performPlayerOnFieldAction(game.fieldsSet[newPosition], playerId, sum(game.lastDice), fixedCoeff=10)

    return handler


def earn(amount):
    def handler(card, game, playerId):
        game.playersData[playerId].addBalance(amount)

    return handler


def getOutOfJail(card, game, playerId):
    game.playersData[playerId].addJailCard(card)


def getOutOfJailUse(card, game, playerId):
    game.playersData[playerId].quitJail()
    game.playersData[playerId].removeJailCard(card)
    game.chanceCards.insert(0, card)


def goToJail(card, game, playerId):
    game.goToJail(playerId)


def payEachPlayer(fee):
    def handler(card, game, playerId):
        player = game.getPlayerById(playerId)
        game.nextMoves.append(GameMove.feeMove(player, ClientPlayer.allPlayer(), fee=fee))

    return handler


def collectFromAll(amount):
    def handler(card, game, playerId):
        otherPlayers = filter(lambda player: player.id != playerId, game.activePlayers)
        game.playersData[playerId].addBalance(amount * len(otherPlayers))
        for otherPlayer in otherPlayers:
            game.playersData[otherPlayer.id].addBalance(-amount)

    return handler


class Card(object):
    def __init__(self, text, handler, useHandler=None):
        self.text = text
        self.handler = handler
        self.useHandler = useHandler

    def staysWithPlayer(self):
        return self.useHandler is not None

    def handle(self, game, playerId):
        self.handler(self, game, playerId)

    def use(self, game, playerId):
        if self.useHandler:
            self.useHandler(self, game, playerId)


CHANCE_CARDS = [
    Card("Advance to Go", positionChange(targetPosition=0)),
    Card("Advance to the nearest airport", advanceToNearest(5, 15, 25, 35)),
    Card("Advance to Dublin", positionChange(targetPosition=24)),
    Card("Advance to Budapest", positionChange(targetPosition=11)),
    Card("Advance to Schiphol Airport", positionChange(targetPosition=5)),
    Card("Bank pays you dividend of $50", earn(50)),
    Card("Your building and loan matures - Collect $150", earn(150)),
    Card("You have won a crossword competition - Collect $100", earn(100)),
    Card("Go back 3 spaces", positionChange(change=-3)),
    Card("Go to Jail", goToJail),
    # general repairs (pay for each house/hotel)
    Card("Pay poor tax of $15", earn(-15)),
    Card("Take a walk to Paris", positionChange(targetPosition=39)),
    Card("Get out of Jail FREE", getOutOfJail, getOutOfJailUse),
    Card("Advance to nearest utility", advanceToNearest(12, 28)),
    Card("You have been elected Chairman of the Board - Pay each player $50", payEachPlayer(50))
]

COMMUNITY_CARDS = [
    Card("Advance to Go", positionChange(targetPosition=0)),
    Card("Bank error in your favor - Collect $200", earn(200)),
    Card("Doctor's fees - Pay $50", earn(-50)),
    Card("From sale of stock you get $50", earn(50)),
    Card("Get out of Jail FREE", getOutOfJail, getOutOfJailUse),
    Card("Go to Jail", goToJail),
    Card("Grand Opera Night Opening - Collect $50 from every player for opening night seats", collectFromAll(50)),
    Card("Holiday Xmas Fund matures - Receive $100", earn(100)),
    Card("Income tax refund - Collect $20", earn(20)),
    Card("Life insurance matures - Collect $100", earn(100)),
    Card("Pay hospital fees of $100", earn(-100)),
    Card("Pay school fees of $150", earn(-150)),
    Card("Receive $25 consultancy fee", earn(25)),
    # general repairs (pay for each house/hotel)
    Card("You have won second prize in a beauty contest - Collect $10", earn(10)),
    Card("You inherit $100", earn(100)),
    Card("It is your birthday - Collect $10 from each player", collectFromAll(10))
]
