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
    def endMove():
        return GameMoveRequest(MoveType.END)