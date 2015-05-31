from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

__author__ = 'mateusz'

class DiceArea(BoxLayout):
    diceOwner = ObjectProperty()
    diceOne = ObjectProperty()
    diceTwo = ObjectProperty()

class BoardMenu(FloatLayout):
    pass

class CityFieldDetails(BoxLayout):
    pass