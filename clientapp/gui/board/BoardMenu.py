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

class EndMove(BoardMenu):
    def endMove(self):
        self.gameServerClient.send(GameMoveRequest.endMove())

class CityFieldDetails(BoxLayout):
    pass