from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from clientapp.gui.board.GameField import WestCityField, SpecialHorizontalField, NorthCityField, EastCityField, \
    SouthCityField, SpecialVerticalField, CityField

from utils.eMonopoly import FieldType


__author__ = 'mateusz'


class GameBoard(FloatLayout):
    startBox = ObjectProperty()
    jailBox = ObjectProperty()
    goToJailBox = ObjectProperty()
    parkingBox = ObjectProperty()
    northPart = ObjectProperty()
    southPart = ObjectProperty()
    westPart = ObjectProperty()
    eastPart = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.widgetFields = dict()
        self.fields = []

    def initialize(self, gameData):
        self.createFieldsView(self.westPart, WestCityField, SpecialHorizontalField, reversed(gameData['fields'][1:10]))
        self.createFieldsView(self.northPart, NorthCityField, SpecialVerticalField, gameData['fields'][11:20])
        self.createFieldsView(self.eastPart, EastCityField, SpecialHorizontalField, gameData['fields'][21:30])
        self.createFieldsView(self.southPart, SouthCityField, SpecialVerticalField, reversed(gameData['fields'][31:40]))
        for i in range(40):
            self.buildHouse(i % 6, i)

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

    def buildHouse(self, houseNo, fieldNo):
        if fieldNo in self.widgetFields and isinstance(self.widgetFields[fieldNo], CityField):
            self.widgetFields[fieldNo].buildingArea.setHouse(houseNo)