import json
from server.requestHandlers.RequestHandler import RequestHandler
from server.requestHandlers.Response import NotAPlayerResponse, Response
from utils.eMonopoly import MoveType

__author__ = 'mateusz'


class GameStateResponse(Response):
    def __init__(self, success, msg, gameState, diceResult=None):
        responseData = {
            'gameData': gameState
        }
        if diceResult:
            responseData['dice1'] = diceResult[0]
            responseData['dice2'] = diceResult[1]
            responseData['diceOwner'] = diceResult[2]
        super(GameStateResponse, self).__init__("GAME_STATE", success, msg, responseData)


class NotEligibleForMove(Response):
    def __init__(self):
        super(NotEligibleForMove, self).__init__("MOVE_RESULT", False, "You are not eligible for a move")


class GameMoveRequestHandler(RequestHandler):
    def __init__(self, gameServer):
        super(GameMoveRequestHandler, self).__init__()
        self.gameServer = gameServer

    def getBidEndCallback(self, room):
        def callback(game):
            print "bid end callback!"
            print "Game moves queue (%d): %s" % (len(game.nextMoves), [str(move) for move in reversed(game.nextMoves)])
            self.gameServer.broadcastAllRoom(room, GameStateResponse(True, "", game.toDictStateOnly()))
        return callback

    def handle(self, msg, rawMsg, clientSocket, clientPlayer, joinedRoom):
        if not clientPlayer:
            return NotAPlayerResponse()
        monopolyGame = joinedRoom.game
        action = json.loads(rawMsg)['action'][5:]
        expectedMove = monopolyGame.popMove(clientPlayer, action)
        if not expectedMove and not self.isAsync(action):
            return NotEligibleForMove()
        diceResult = None
        if action == MoveType.DICE:
            diceResult = monopolyGame.doDiceMove(clientPlayer.id, expectedMove)
        elif action == MoveType.BUY:
            monopolyGame.doBuyEstate(clientPlayer.id, msg, self.getBidEndCallback(joinedRoom))
        elif action == MoveType.FEE:
            monopolyGame.doPayFee(clientPlayer.id, msg, expectedMove, self.getBidEndCallback(joinedRoom))
        elif action == MoveType.JAIL:
            diceResult = monopolyGame.doJailMove(clientPlayer.id, msg)
        elif action == MoveType.BID:
            monopolyGame.doBidMove(clientPlayer.id, msg)
        elif action == MoveType.DRAW:
            monopolyGame.doDrawMove(clientPlayer.id, expectedMove)
        elif action == MoveType.END:
            monopolyGame.doEndMove(clientPlayer.id)
        elif action == MoveType.HOUSE:
            monopolyGame.doHouseMove(clientPlayer.id, msg)
        elif action == MoveType.MORTGAGE:
            monopolyGame.doMortgageMove(clientPlayer.id, msg)
        print "Game moves queue (%d): %s" % (
            len(monopolyGame.nextMoves), [str(move) for move in reversed(monopolyGame.nextMoves)])
        self.gameServer.broadcastAllRoom(joinedRoom,
                                         GameStateResponse(True, "", monopolyGame.toDictStateOnly(), diceResult))

    def isAsync(self, action):
        return action in [MoveType.HOUSE, MoveType.MORTGAGE]