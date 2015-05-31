from os.path import dirname

from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from clientapp.gui.board.GameField import WestCityField, SpecialHorizontalField, NorthCityField, EastCityField, \
    SouthCityField, SpecialVerticalField, CityField, SpecialField

from utils.eMonopoly import FieldType


__author__ = 'mateusz'

PLAYER_COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]


class GameBoard(FloatLayout):
    startBox = ObjectProperty()
    jailBox = ObjectProperty()
    parkingBox = ObjectProperty()
    goToJailBox = ObjectProperty()
    northPart = ObjectProperty()
    southPart = ObjectProperty()
    westPart = ObjectProperty()
    eastPart = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.widgetFields = dict()
        self.fields = []
        self.players = []

    def initialize(self, gameData):
        self.createFieldsView(self.westPart, WestCityField, SpecialHorizontalField, reversed(gameData['fields'][1:10]))
        self.createFieldsView(self.northPart, NorthCityField, SpecialVerticalField, gameData['fields'][11:20])
        self.createFieldsView(self.eastPart, EastCityField, SpecialHorizontalField, gameData['fields'][21:30])
        self.createFieldsView(self.southPart, SouthCityField, SpecialVerticalField, reversed(gameData['fields'][31:40]))
        dir = dirname(__file__)
        self.startBox.imageSrc = dir + '/../assets/cornergo.jpg'
        self.jailBox.imageSrc = dir + '/../assets/cornerinjail.jpg'
        self.parkingBox.imageSrc = dir + '/../assets/cornerfreepark.jpg'
        self.goToJailBox.imageSrc = dir + '/../assets/cornerjail.jpg'

        self.players = self.assignColors(gameData['players'])
        # for i in range(40):
        #     self.buildHouse(i, i % 6)
        #     self.markFieldBoughtByPlayer(i, self.players[0]['id'])

    def createFieldsView(self, targetLayout, cityClz, specialClz, dataFields):
        for field in dataFields:
            if field['type'] == FieldType.CITY:
                widgetField = cityClz(field['name'], field['value'], field['color'])
                targetLayout.add_widget(widgetField)
            else:
                widgetField = specialClz(field['name'], field['value'])
                targetLayout.add_widget(widgetField)
            self.widgetFields[field['number']] = widgetField
            self.fields.append(field)

    def assignColors(self, players):
        for i, player in enumerate(players):
            player['color'] = PLAYER_COLORS[i]
        return players

    def getPlayerColor(self, playerId):
        for player in self.players:
            if player['id'] == playerId:
                return player['color']

    def buildHouse(self, fieldNo, houseNo):
        if fieldNo in self.widgetFields and isinstance(self.widgetFields[fieldNo], CityField):
            self.widgetFields[fieldNo].buildingArea.setHouse(houseNo)

    def markFieldBoughtByPlayer(self, fieldNo, playerId):
        if fieldNo in self.widgetFields and (isinstance(self.widgetFields[fieldNo], CityField) or isinstance(
                self.widgetFields[fieldNo], SpecialField)):
            self.widgetFields[fieldNo].markBoughtByPlayer(self.getPlayerColor(playerId))