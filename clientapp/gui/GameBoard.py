from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from clientapp.gui.HorizontalCityField import HorizontalCityField

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

    def initialize(self):
        for i in range(9):
            self.westPart.add_widget(HorizontalCityField("Buda", "400", "FFFFFF"))