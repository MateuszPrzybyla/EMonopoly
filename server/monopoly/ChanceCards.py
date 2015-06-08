from server.ClientPlayer import ClientPlayer
from server.monopoly.GameMove import GameMove

__author__ = 'mateusz'


def positionChange(targetPosition=0, change=0):
    def handler(game, playerId):
        playerData = game.playersData[playerId]
        if targetPosition:
            playerData.movePlayerToField(targetPosition)
        elif change:
            playerData.movePlayer(change)
        else:
            return
        game.checkStartBonus(playerId)
        game.performPlayerOnFieldAction(game.fieldsSet[playerData.fieldPosition], playerId, sum(game.lastDice))

    return handler


def advanceToNearestAirport(game, playerId):
    position = game.playersData[playerId].fieldPosition
    newPosition = (position + (10 - (position - 5) % 10)) % 40
    game.playersData[playerId].movePlayerToField(newPosition)
    game.checkStartBonus(playerId)
    game.performPlayerOnFieldAction(game.fieldsSet[newPosition], playerId, sum(game.lastDice))


def earn(amount):
    def handler(game, playerId):
        game.playersData[playerId].addBalance(amount)

    return handler


def goToJail(game, playerId):
    game.goToJail(playerId)


def payEachPlayer(fee):
    def handler(game, playerId):
        player = game.getPlayerById(playerId)
        fieldNo = game.playersData[playerId].fieldPosition
        game.nextMoves.append(GameMove.feeMove(player, ClientPlayer.allPlayer(), fee=fee, fieldNo=fieldNo))

    return handler


class ChanceCard(object):
    def __init__(self, text, handler):
        self.text = text
        self.handler = handler


CHANCE_CARDS = [
    # trip to Illinois Avenue
    # trip to St. Charles Place
    # trip to the nearest utility
    # trip to Reading Railroad
    ChanceCard("Advance to Go", positionChange(targetPosition=0)),
    ChanceCard("Advance to the nearest airport", advanceToNearestAirport),
    ChanceCard("Bank pays you dividend of $50", earn(50)),
    # GET OUT OF JAIL FREE
    ChanceCard("Go back 3 spaces", positionChange(change=-3)),
    ChanceCard("Go to Jail", goToJail),
    # general repairs (pay for each house/hotel)
    ChanceCard("Pay poor tax of $15", earn(-15)),
    ChanceCard("Take a walk to Paris", positionChange(targetPosition=39)),
    ChanceCard("You have been elected Chairman of the Board - Pay each player $50", payEachPlayer(50))
]
