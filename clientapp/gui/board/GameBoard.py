# pylint: disable=E1101
# pylint: disable=no-name-in-module
""" Contains layout of the whole game board (fields, corner boxes, building areas etc.) and the menu
"""
from collections import OrderedDict
from os.path import dirname

from kivy.app import App

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from clientapp.gui.board.GameField import WestCityField, NorthCityField, EastCityField, \
    SouthCityField, CityField, SpecialWestField, SpecialNorthField, SpecialEastField, \
    SpecialSouthField, CornerBox
from utils.eMonopoly import FieldType
# pylint: enable=no-name-in-module


__author__ = 'mateusz'

PLAYER_COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]


class GameBoard(BoxLayout):
    """ Contains layout of the whole game board (fields, corner boxes, building areas etc.) and the menu """
    startBox = ObjectProperty()
    jailBox = ObjectProperty()
    parkingBox = ObjectProperty()
    goToJailBox = ObjectProperty()
    northPart = ObjectProperty()
    southPart = ObjectProperty()
    westPart = ObjectProperty()
    eastPart = ObjectProperty()
    diceArea = ObjectProperty()
    boardMenu = ObjectProperty()
    gameStats = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.widgetFields = dict()
        self.players = OrderedDict()
        self.playersData = dict()
        self.playersRenderedPositions = dict()

    def initialize(self, data):
        """ Initializes game board with initial fields state (default) """
        gameData = data['gameData']
        self.app.setData('gameFields', dict())
        self.createFieldsView(self.westPart, WestCityField, SpecialWestField, reversed(gameData['fields'][1:10]))
        self.createFieldsView(self.northPart, NorthCityField, SpecialNorthField, gameData['fields'][11:20])
        self.createFieldsView(self.eastPart, EastCityField, SpecialEastField, gameData['fields'][21:30])
        self.createFieldsView(self.southPart, SouthCityField, SpecialSouthField, reversed(gameData['fields'][31:40]))
        self.createCornerBoxFieldView(0, self.startBox, 'cornergo.jpg')
        self.createCornerBoxFieldView(10, self.jailBox, 'cornerinjail.jpg')
        self.createCornerBoxFieldView(20, self.parkingBox, 'cornerfreepark.jpg')
        self.createCornerBoxFieldView(30, self.goToJailBox, 'cornerjail.jpg')

        self.players = self.assignAdditionalData(gameData['players'])
        self.createPlayersBalanceStats(gameData['playersData'])
        self.updateGameState(data)

    def createCornerBoxFieldView(self, number, cornerBox, bgFileName):
        """ Creates corner box widget """
        self.widgetFields[number] = cornerBox
        cornerBox.imageSrc = dirname(__file__) + '/../assets/' + bgFileName

    def createFieldsView(self, targetLayout, cityClz, specialClz, dataFields):
        """ Creates single field widget (horizontal/vertical) depending on specified classes"""
        appDataFields = self.app.getData('gameFields')
        for field in dataFields:
            if field['type'] == FieldType.CITY:
                widgetField = cityClz(field['name'], field['value'], field['color'])
                targetLayout.add_widget(widgetField)
            else:
                widgetField = specialClz(field['name'], field['value'])
                targetLayout.add_widget(widgetField)
            self.widgetFields[field['number']] = widgetField
            appDataFields[field['number']] = field

    def createPlayersBalanceStats(self, playersData):
        """ Creates widget displayed at the bottom with players balance"""
        for playerId, player in self.players.items():
            self.gameStats.add_widget(Label(text="%s: %d" % (player['name'], playersData[str(playerId)]['balance'])))

    @staticmethod
    def assignAdditionalData(players):
        """ Initialized players info with additional useful in rendering players information """
        playersWithDetails = OrderedDict()
        for i, player in enumerate(players):
            playersWithDetails[player['id']] = player
            playersWithDetails[player['id']]['color'] = PLAYER_COLORS[i]
            playersWithDetails[player['id']]['number'] = i + 1
        return playersWithDetails

    def getPlayerColor(self, playerId):
        """ Returns color associated with player with given id"""
        return self.players[int(playerId)]['color']

    def updateGameState(self, data):
        """ Invoked after every game state update retrieved from the server. Updates field state and players data"""
        gameData = data['gameData']
        for playerId, playerData in gameData['playersData'].items():
            self.movePlayerToField(playerData['position'], playerId, playerData['inJail'])
        self.boardMenu.updateMenu(gameData)
        if 'dice1' in data and 'dice2' in data and 'diceOwner' in data:
            self.diceArea.updateDice(data['dice1'], data['dice2'], data['diceOwner'])
        self.updateFieldsState(gameData['fields'])
        self.updateBalanceStats(gameData['playersData'])

    def movePlayerToField(self, fieldNo, playerId, inJail=False):
        """ Moves player marker from previous field to the next one """
        playerNo = self.players[int(playerId)]['number']
        field = self.widgetFields[fieldNo]
        if playerNo in self.playersRenderedPositions:
            self.playersRenderedPositions[playerNo].removePlayerFromField(playerNo)
        if isinstance(field, CornerBox):
            field.putPlayerOnField(playerNo, self.getPlayerColor(playerId), inJail)
        else:
            field.putPlayerOnField(playerNo, self.getPlayerColor(playerId))
        self.playersRenderedPositions[playerNo] = field

    def updateFieldsState(self, fields):
        """ Updates field related data with each update from the server, color is updated,
            mortgaged marker and houses area
        """
        for fieldNo, widgetField in self.widgetFields.items():
            if isinstance(widgetField, CornerBox):
                continue
            if str(fieldNo) not in fields:
                widgetField.setInitialState()
            else:
                fieldState = fields[str(fieldNo)]
                widgetField.markBoughtByPlayer(self.getPlayerColor(fieldState['owner']))
                widgetField.drawMortgage(fieldState['mortgage'])
                if isinstance(widgetField, CityField):
                    widgetField.setHouse(fieldState['houses'])

    def updateBalanceStats(self, playersData):
        """ Updates players balance statistics """
        for playerId, player in self.players.items():
            label = self.gameStats.children[player['number'] - 1]
            if str(playerId) in playersData:
                label.text = "%s: %d" % (player['name'], playersData[str(playerId)]['balance'])
            else:
                label.text = "%s: BROKEN" % player['name']
