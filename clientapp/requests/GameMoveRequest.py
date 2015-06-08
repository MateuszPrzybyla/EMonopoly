from clientapp.requests.Request import Request
from utils.eMonopoly import MoveType

__author__ = 'mateusz'


class GameMoveRequest(Request):
    def __init__(self, type, moveData={}):
        super(GameMoveRequest, self).__init__("GAME_" + type, moveData)

    @staticmethod
    def rollTheDice():
        return GameMoveRequest(MoveType.DICE)

    @staticmethod
    def buyResponse(fieldNo, decision):
        return GameMoveRequest(MoveType.BUY, {
            'fieldNo': fieldNo,
            'decision': decision
        })

    @staticmethod
    def payFee(pay):
        return GameMoveRequest(MoveType.FEE, {
            'pay': pay
        })

    @staticmethod
    def bidMove(value):
        return GameMoveRequest(MoveType.BID, {
            'value': value
        })

    @staticmethod
    def quitJail(method):
        return GameMoveRequest(MoveType.JAIL, {
            'method': method
        })

    @staticmethod
    def drawMove():
        return GameMoveRequest(MoveType.DRAW)

    @staticmethod
    def buyHouseMove(fieldNo):
        return GameMoveRequest(MoveType.HOUSE, {
            'action': 'buy',
            'fieldNo': int(fieldNo)
        })

    @staticmethod
    def sellHouseMove(fieldNo):
        return GameMoveRequest(MoveType.HOUSE, {
            'action': 'sell',
            'fieldNo': int(fieldNo)
        })

    @staticmethod
    def mortgageSellMove(fieldNo):
        return GameMoveRequest(MoveType.MORTGAGE, {
            'action': 'sell',
            'fieldNo': int(fieldNo)
        })

    @staticmethod
    def mortgageLiftMove(fieldNo):
        return GameMoveRequest(MoveType.MORTGAGE, {
            'action': 'lift',
            'fieldNo': int(fieldNo)
        })

    @staticmethod
    def endMove():
        return GameMoveRequest(MoveType.END)