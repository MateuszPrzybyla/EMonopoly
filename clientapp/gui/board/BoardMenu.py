from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from clientapp.requests.GameMoveRequest import GameMoveRequest
from utils.eMonopoly import MoveType, FieldType

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
    syncMenu = ObjectProperty()
    asyncMenu = ObjectProperty()

    def __init__(self, **kwargs):
        super(BoardMenuWrapper, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def updateMenu(self, gameData):
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
    def __init__(self, **kwargs):
        super(BoardMenu, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.gameServerClient = self.app.gameServerClient


class WaitForMove(BoardMenu):
    pass


class GameEnd(BoardMenu):
    winnerLabel = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(GameEnd, self).__init__(**kwargs)
        self.winnerLabel.text = "Winner: %s" % moveData['winner']['name']


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


class Bidding(BoardMenu):
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
        try:
            self.gameServerClient.send(GameMoveRequest.bidMove(int(bidValue)))
        except ValueError:
            pass


class Draw(BoardMenu):
    cardType = ObjectProperty()

    def __init__(self, moveData, **kwargs):
        super(Draw, self).__init__(**kwargs)
        self.cardType.text = moveData['type']

    def draw(self):
        self.gameServerClient.send(GameMoveRequest.drawMove())


class Debt(BoardMenu):
    def paid(self):
        self.gameServerClient.send(GameMoveRequest.payDebt(True))

    def goBankrupt(self):
        self.gameServerClient.send(GameMoveRequest.payDebt(False))


class EndMove(BoardMenu):
    def endMove(self):
        self.gameServerClient.send(GameMoveRequest.endMove())


class AsyncMenu(ScreenManager):
    mainScreen = ObjectProperty()
    buyHouseScreen = ObjectProperty()
    sellHouseScreen = ObjectProperty()
    mortgageSellScreen = ObjectProperty()
    mortgageLiftScreen = ObjectProperty()

    def __init__(self, **kwargs):
        super(AsyncMenu, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def updateMenu(self, gameData):
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
        self.current = self.mainScreen.name

    def goBuyHouse(self):
        self.current = self.buyHouseScreen.name

    def goSellHouse(self):
        self.current = self.sellHouseScreen.name

    def goMortgageSell(self):
        self.current = self.mortgageSellScreen.name

    def goMortgageLift(self):
        self.current = self.mortgageLiftScreen.name


class AsyncMenuScreen(Screen):
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
        appFields = self.app.getData('gameFields')
        self.fieldsList.clear_widgets()
        for fieldNo in sorted(fields, key=int):
            self.fieldsList.add_widget(
                BuyHouseButton(fieldNo, str(appFields[int(fieldNo)]['name']), self.updateSelectedField))

    def updateSelectedField(self, btn):
        self.selectedNo = btn.fieldNo
        self.selectedField.text = "Selected: %s" % btn.fieldName

    def execute(self):
        moveRequest = self.getMoveRequest(self.selectedNo)
        if self.selectedNo and moveRequest:
            self.gameServerClient.send(moveRequest)

    def getMoveRequest(self, selectedNo):
        pass

    def goBack(self):
        self.manager.loadMainScreen()


class BuyHouseScreen(AsyncMenuScreen):
    def __init__(self, **kwargs):
        self.buttonText = "BUY"
        self.screenTitle = "Buy a house"
        super(BuyHouseScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        return GameMoveRequest.buyHouseMove(selectedNo)


class SellHouseScreen(AsyncMenuScreen):
    def __init__(self, **kwargs):
        self.buttonText = "SELL"
        self.screenTitle = "Sell a house"
        super(SellHouseScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        return GameMoveRequest.sellHouseMove(selectedNo)


class MortgageSellScreen(AsyncMenuScreen):
    def __init__(self, **kwargs):
        self.buttonText = "MORTGAGE"
        self.screenTitle = "Mortgage"
        super(MortgageSellScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        return GameMoveRequest.mortgageSellMove(selectedNo)


class MortgageLiftScreen(AsyncMenuScreen):
    def __init__(self, **kwargs):
        self.buttonText = "LIFT MORTGAGE"
        self.screenTitle = "Lift the mortgage"
        super(MortgageLiftScreen, self).__init__(**kwargs)

    def getMoveRequest(self, selectedNo):
        return GameMoveRequest.mortgageLiftMove(selectedNo)


class BuyHouseButton(Button):
    def __init__(self, fieldNo, fieldName, on_press_callback, **kwargs):
        super(BuyHouseButton, self).__init__(**kwargs)
        self.fieldNo = fieldNo
        self.fieldName = fieldName
        self.text = str(fieldNo)
        self.font_size = 12
        self.bind(on_press=on_press_callback)


class CityFieldDetails(BoxLayout):
    pass

