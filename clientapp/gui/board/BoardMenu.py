from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from clientapp.requests.GameMoveRequest import GameMoveRequest
from utils.eMonopoly import MoveType

__author__ = 'mateusz'


class DiceArea(BoxLayout):
    diceOwner = ObjectProperty()
    diceOne = ObjectProperty()
    diceTwo = ObjectProperty()

    def updateDice(self, dice1, dice2, diceOwner):
        self.diceOwner.text = "%s rolls..." % diceOwner
        self.diceOne.text = str(dice1)
        self.diceTwo.text = str(dice2)


class BoardMenuWrapper(BoxLayout):
    def __init__(self, **kwargs):
        super(BoardMenuWrapper, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def updateMenu(self, nextMove):
        self.clear_widgets()
        if all([player['name'] != self.app.getData('nick') for player in nextMove['eligiblePlayers']]):
            self.add_widget(WaitForMove())
        elif nextMove['moveType'] == MoveType.DICE:
            self.add_widget(RollTheDice())
        elif nextMove['moveType'] == MoveType.BUY:
            self.add_widget(BuyEstate(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.FEE:
            self.add_widget(PayFee(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.JAIL:
            self.add_widget(InJail(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.END:
            self.add_widget(EndMove())


class BoardMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(BoardMenu, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient


class WaitForMove(BoardMenu):
    pass


class RollTheDice(BoardMenu):
    def rollTheDice(self):
        self.gameServerClient.send(GameMoveRequest.rollTheDice())


class BuyEstate(BoardMenu):
    fieldName = ObjectProperty()
    fieldValue = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(BuyEstate, self).__init__(**kwargs)
        self.fieldNo = moveData['fieldNo']
        self.fieldName.text = self.app.getData('gameFields')[self.fieldNo]['name']
        self.fieldValue.text = "%d $" % moveData['value']

    def buy(self):
        self.gameServerClient.send(GameMoveRequest.buyResponse(self.fieldNo, True))

    def doNotBuy(self):
        self.gameServerClient.send(GameMoveRequest.buyResponse(self.fieldNo, False))

class PayFee(BoardMenu):
    targetPlayer = ObjectProperty()
    fee = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(PayFee, self).__init__(**kwargs)
        if moveData['targetPlayer']:
            self.targetPlayer.text = "Player: %s" % moveData['targetPlayer']['name']
        else:
            self.targetPlayer.text = ""
        self.fee.text = "%d $" % moveData['fee']

    def payFee(self):
        self.gameServerClient.send(GameMoveRequest.payFee(True))

    def goBankrupt(self):
        self.gameServerClient.send(GameMoveRequest.payFee(False))

class InJail(BoardMenu):
    turnsLeft = ObjectProperty()
    jailCard = ObjectProperty()
    payAndQuitBtn = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(InJail, self).__init__(**kwargs)
        self.turnsLeft.text = "%d turn(s) left" % moveData['turnsLeft']
        if moveData['turnsLeft'] == 0:
            self.payAndQuitBtn.parent.clear_widgets(children=[self.payAndQuitBtn])
        if not moveData['hasCard']:
            self.jailCard.parent.clear_widgets(children=[self.jailCard])

    def payAndQuit(self):
        self.gameServerClient.send(GameMoveRequest.quitJail('pay'))

    def rollTheDice(self):
        self.gameServerClient.send(GameMoveRequest.quitJail('dice'))

    def useTheCard(self):
        self.gameServerClient.send(GameMoveRequest.quitJail('card'))

class EndMove(BoardMenu):
    def endMove(self):
        self.gameServerClient.send(GameMoveRequest.endMove())


class CityFieldDetails(BoxLayout):
    pass