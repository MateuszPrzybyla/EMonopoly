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
    def endMove():
        return GameMoveRequest(MoveType.END)