# pylint: disable=E1101
# pylint: disable=no-name-in-module
""" Contains widget and their logic related to displaying menu and dispatching click buttons to gameServerClient"""
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from clientapp.requests.GameMoveRequest import GameMoveRequest
from utils.eMonopoly import MoveType, FieldType
# pylint: enable=no-name-in-module

__author__ = 'mateusz'


class DiceArea(BoxLayout):
    """ Contains information about last dice roll"""
    diceOwner = ObjectProperty()
    diceOne = ObjectProperty()
    diceTwo = ObjectProperty()

    def updateDice(self, dice1, dice2, diceOwner):
        """ Updates information about last dice """
        self.diceOwner.text = "%s rolls..." % diceOwner
        self.diceOne.text = str(dice1)
        self.diceTwo.text = str(dice2)


class BoardMenuWrapper(BoxLayout):
    """ Wraps all menu with sync and async part. Every user operation comes from within this widget """
    syncMenu = ObjectProperty()
    asyncMenu = ObjectProperty()

    def __init__(self, **kwargs):
        super(BoardMenuWrapper, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def updateMenu(self, gameData):
        """ Updates information about available move at the moment """
        nextMove = gameData['nextMove']
        self.syncMenu.clear_widgets()
        if all([player['name'] != self.app.getData('nick') for player in nextMove['eligiblePlayers']]):
            self.syncMenu.add_widget(WaitForMove())
        elif nextMove['moveType'] == MoveType.DICE:
            self.syncMenu.add_widget(RollTheDice())
        elif nextMove['moveType'] == MoveType.BUY:
            self.syncMenu.add_widget(BuyEstate(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.FEE:
            self.syncMenu.add_widget(PayFee(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.JAIL:
            self.syncMenu.add_widget(InJail(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.BID:
            self.syncMenu.add_widget(Bidding(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.DRAW:
            self.syncMenu.add_widget(Draw(nextMove['moveData']))
        elif nextMove['moveType'] == MoveType.DEBT:
            self.syncMenu.add_widget(Debt())
        elif nextMove['moveType'] == MoveType.END:
            self.syncMenu.add_widget(EndMove())
        elif nextMove['moveType'] == MoveType.WIN:
            self.syncMenu.add_widget(GameEnd(nextMove['moveData']))
        self.asyncMenu.updateMenu(gameData)


class BoardMenu(BoxLayout):
    """ Base class for all synchronous moves menu """

    def __init__(self, **kwargs):
        super(BoardMenu, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient


class WaitForMove(BoardMenu):
    """ Mock menu displaying information about waiting for a move """
    pass


class GameEnd(BoardMenu):
    """ Mock menu displaying information about end of the game and the winner """
    winnerLabel = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(GameEnd, self).__init__(**kwargs)
        self.winnerLabel.text = "Winner: %s" % moveData['winner']['name']


class RollTheDice(BoardMenu):
    """ Menu with single button to roll the dice """

    def rollTheDice(self):
        """ Sends a request to trigger rolling the dice """
        self.gameServerClient.send(GameMoveRequest.rollTheDice())


class BuyEstate(BoardMenu):
    """ Menu with options to buy an estate associated with current player's field """
    fieldName = ObjectProperty()
    fieldValue = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(BuyEstate, self).__init__(**kwargs)
        self.fieldNo = moveData['fieldNo']
        self.fieldName.text = self.app.getData('gameFields')[self.fieldNo]['name']
        self.fieldValue.text = "%d $" % moveData['value']

    def buy(self):
        """ Sends a request with positive decision about buying an estate """
        self.gameServerClient.send(GameMoveRequest.buyResponse(self.fieldNo, True))

    def doNotBuy(self):
        """ Sends a request with negative decision about buying an estate """
        self.gameServerClient.send(GameMoveRequest.buyResponse(self.fieldNo, False))


class PayFee(BoardMenu):
    """ Contains information about fee move - player can pay the fee, or if has no money and possibility - can
        announce going bankrupt
    """
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
        """ Sends a request with confirmation of the fee """
        self.gameServerClient.send(GameMoveRequest.payFee(True))

    def goBankrupt(self):
        """ Sends a request with information that players gives up as a bankrupt """
        self.gameServerClient.send(GameMoveRequest.payFee(False))


class InJail(BoardMenu):
    """ Menu with options to select what to do when player is in jail """
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
        """ Sends a request to immediately pay and quit the jail """
        self.gameServerClient.send(GameMoveRequest.quitJail('pay'))

    def rollTheDice(self):
        """ Sends a request to roll the dice and wait for the double """
        self.gameServerClient.send(GameMoveRequest.quitJail('dice'))

    def useTheCard(self):
        """ Sends a request to use the 'Get out of Jail Free" Card """
        self.gameServerClient.send(GameMoveRequest.quitJail('card'))


class Bidding(BoardMenu):
    """ Menu with options to bid """
    fieldName = ObjectProperty()
    currentValue = ObjectProperty()
    currentWinner = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(Bidding, self).__init__(**kwargs)
        self.fieldNo = moveData['fieldNo']
        self.fieldName.text = self.app.getData('gameFields')[self.fieldNo]['name']
        self.currentWinner.text = "Winner: %s" % moveData['currentWinner']['name'] \
            if 'currentWinner' in moveData else ""
        self.currentValue.text = "Winning price: %d $" % moveData['currentMin']

    def bid(self, bidValue):
        """ Sends a request to with a bid """
        try:
            self.gameServerClient.send(GameMoveRequest.bidMove(int(bidValue)))
        except ValueError:
            pass


class Draw(BoardMenu):
    """ Menu with button to draw a card (chance/community) """
    cardType = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(Draw, self).__init__(**kwargs)
        self.cardType.text = moveData['type']

    def draw(self):
        """ Sends a request to draw a card """
        self.gameServerClient.send(GameMoveRequest.drawMove())


class Debt(BoardMenu):
    """ Menu with button to handle the debt """

    def paid(self):
        """ Sends a request to free the debt """
        self.gameServerClient.send(GameMoveRequest.payDebt(True))

    def goBankrupt(self):
        """ Sends a request announcing going bankrupt """
        self.gameServerClient.send(GameMoveRequest.payDebt(False))


class EndMove(BoardMenu):
    """ Menu with button to end current move """

    def endMove(self):
        """ Sends a request to end current move """
        self.gameServerClient.send(GameMoveRequest.endMove())


class AsyncMenu(ScreenManager):
    """ Menu with asynchronous operations that can be done at any time (buying/selling a house, managing a mortgage)"""
    mainScreen = ObjectProperty()
    buyHouseScreen = ObjectProperty()
    sellHouseScreen = ObjectProperty()
    mortgageSellScreen = ObjectProperty()
    mortgageLiftScreen = ObjectProperty()

    def __init__(self, **kwargs):
        super(AsyncMenu, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def updateMenu(self, gameData):
        """ Updates asynchronous menu data with updated informations about players fields """
        if not isinstance(gameData['fields'], dict):
            return
        playerId = self.app.getData('playerId')
        appFields = self.app.getData('gameFields')
        ownedCities = [fieldNo for (fieldNo, fieldData) in gameData['fields'].items() if
                       fieldData['owner'] == playerId and appFields[int(fieldNo)]['type'] == FieldType.CITY]
        self.buyHouseScreen.addFields(ownedCities)
        self.sellHouseScreen.addFields(ownedCities)
        ownedProperties = [fieldNo for (fieldNo, fieldData) in gameData['fields'].items() if
                           fieldData['owner'] == playerId]
        self.mortgageSellScreen.addFields(ownedProperties)
        self.mortgageLiftScreen.addFields(ownedProperties)

    def loadMainScreen(self):
        """ Loads main screen of the async menu """
        self.current = self.mainScreen.name

    def goBuyHouse(self):
        """ Loads 'Buy House' screen of the async menu """
        self.current = self.buyHouseScreen.name

    def goSellHouse(self):
        """ Loads 'Sell House' screen of the async menu """
        self.current = self.sellHouseScreen.name

    def goMortgageSell(self):
        """ Loads 'Mortgage' screen of the async menu """
        self.current = self.mortgageSellScreen.name

    def goMortgageLift(self):
        """ Loads 'Lift Mortgage' screen of the async menu """
        self.current = self.mortgageLiftScreen.name


class AsyncMenuScreen(Screen):
    """ Base class for all async menu screens """
    fieldsList = ObjectProperty()
    selectedField = ObjectProperty()
    buttonText = StringProperty()
    screenTitle = StringProperty()

    def __init__(self, **kwargs):
        super(AsyncMenuScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient
        self.selectedNo = None

    def addFields(self, fields):
        """ Adds field buttons (with field number) to the screen with passed fields """
        appFields = self.app.getData('gameFields')
        self.fieldsList.clear_widgets()
        for fieldNo in sorted(fields, key=int):
            self.fieldsList.add_widget(
                BuyHouseButton(fieldNo, str(appFields[int(fieldNo)]['name']), self.updateSelectedField))

    def updateSelectedField(self, btn):
        """ Updates selected field, sets field name label to currently selected """
        self.selectedNo = btn.fieldNo
        self.selectedField.text = "Selected: %s" % btn.fieldName

    def execute(self):
        """ Submits action on selected field """
        moveRequest = self.getMoveRequest(self.selectedNo)
        if self.selectedNo and moveRequest:
            self.gameServerClient.send(moveRequest)

    def getMoveRequest(self, selectedNo):
        """ Gets MoveRequest that will be sent during submit """
        pass

    def goBack(self):
        """ Goes back to the main screen of the async menu """
        self.manager.loadMainScreen()


class BuyHouseScreen(AsyncMenuScreen):
    """ Buy House screen of the async menu """

    def __init__(self, **kwargs):
        self.buttonText = "BUY"
        self.screenTitle = "Buy a house"
        super(BuyHouseScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        """ Returns BuyHouse move request """
        return GameMoveRequest.buyHouseMove(selectedNo)


class SellHouseScreen(AsyncMenuScreen):
    """ Sell House screen of the async menu """

    def __init__(self, **kwargs):
        self.buttonText = "SELL"
        self.screenTitle = "Sell a house"
        super(SellHouseScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        """ Returns SellHouse move request """
        return GameMoveRequest.sellHouseMove(selectedNo)


class MortgageSellScreen(AsyncMenuScreen):
    """ Mortgage screen of the async menu """

    def __init__(self, **kwargs):
        self.buttonText = "MORTGAGE"
        self.screenTitle = "Mortgage"
        super(MortgageSellScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        """ Returns Mortgage move request """
        return GameMoveRequest.mortgageSellMove(selectedNo)


class MortgageLiftScreen(AsyncMenuScreen):
    """ Lift Mortgage screen of the async menu """

    def __init__(self, **kwargs):
        self.buttonText = "LIFT MORTGAGE"
        self.screenTitle = "Lift the mortgage"
        super(MortgageLiftScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        """ Returns LiftMortgage move request """
        return GameMoveRequest.mortgageLiftMove(selectedNo)


# pylint: disable=invalid-name
class BuyHouseButton(Button):
    """ A single button representing one field that can be used for async operation """

    def __init__(self, fieldNo, fieldName, on_press_callback, **kwargs):
        super(BuyHouseButton, self).__init__(**kwargs)
        self.fieldNo = fieldNo
        self.fieldName = fieldName
        self.text = str(fieldNo)
        self.font_size = 12
        self.bind(on_press=on_press_callback)


#pylint: enable=invalid-name

class CityFieldDetails(BoxLayout):
    """ Widget class for field details menu element """
    pass

