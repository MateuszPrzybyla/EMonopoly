from utils.eMonopoly import MoveType

__author__ = 'mateusz'


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
    def feeMove(player, targetPlayer, field, diceResult):
        return GameMove([player], MoveType.FEE, {
            'targetPlayer': targetPlayer.toDict(),
            'fieldNo': field.model.number,
            'fee': field.getFee(diceResult)
        })

    @staticmethod
    def inJail(player, turnsInJailLeft, hasJailCard):
        return GameMove([player], MoveType.JAIL, {
            'turnsLeft': turnsInJailLeft,
            'hasCard': hasJailCard
        })

    @staticmethod
    def bidMove(players, currentMin, currentWinner, field):
        if currentWinner:
            return GameMove(players, MoveType.BID, {
                'currentMin': currentMin,
                'currentWinner': currentWinner.toDict(),
                'fieldNo': field.model.number
            })
        else:
            return GameMove(players, MoveType.BID, {
                'currentMin': currentMin,
                'fieldNo': field.model.number
            })

    @staticmethod
    def endMove(player):
        return GameMove([player], MoveType.END)

    def __str__(self):
        return "TYPE: %s, PLAYERS: %s, MOVE_DATA: %s" % (
            self.moveType, [player.name for player in self.eligiblePlayers], str(self.moveData))