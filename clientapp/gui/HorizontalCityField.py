from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

__author__ = 'mateusz'

class HorizontalCityField(BoxLayout):
    cityName = ObjectProperty()
    value = ObjectProperty()
    fieldColor = ObjectProperty()

    def __init__(self, cityName, value, color):
        super(HorizontalCityField, self).__init__()
        self.cityName.text = cityName
        self.value.text = value + " $"