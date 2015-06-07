__author__ = 'mateusz'


def positionChange(target):
    def handler(game, playerId):
        game.playersData[playerId].movePlayerToField(target)
        game.checkStartBonus(playerId)
        game.performPlayerOnFieldAction(game.fieldsSet[target], playerId, sum(game.lastDice))

    return handler


class ChanceCard(object):
    def __init__(self, text, handler):
        self.text = text
        self.handler = handler


CHANCE_CARDS = [
    ChanceCard("Advance to Go", positionChange(0))
]
