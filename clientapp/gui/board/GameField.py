from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

__author__ = 'mateusz'


def calculateFontSize(text, width):
    return int(width * 0.75 / len(text))


def parseColor(color):
    return get_color_from_hex(color)

class CityNameLabel(Label):
    ownerColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(CityNameLabel, self).__init__(**kwargs)
        self.ownerColor = (0, 0, 0, 1)


class FieldValueLabel(Label):
    ownerColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(FieldValueLabel, self).__init__(**kwargs)
        self.ownerColor = (0, 0, 0, 1)


class CityField(BoxLayout):
    cityName = ObjectProperty()
    value = ObjectProperty()
    buildingArea = ObjectProperty()
    ownerColor = ObjectProperty()

    def __init__(self, cityName, value, color):
        super(CityField, self).__init__()
        self.cityName.text = cityName
        self.cityName.font_size = str(calculateFontSize(cityName, self.width)) + 'sp'
        self.value.text = str(value) + " $"
        self.buildingArea.fieldColor = parseColor(color)
        self.ownerColor = (0, 0, 0)

    def markBoughtByPlayer(self, hexColor):
        self.cityName.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)


class WestCityField(CityField):
    pass


class EastCityField(CityField):
    pass


class NorthCityField(CityField):
    pass


class SouthCityField(CityField):
    pass


class SpecialField(BoxLayout):
    namesWrapper = ObjectProperty()
    value = ObjectProperty()
    nameFirstRow = ObjectProperty()
    nameSecondRow = ObjectProperty()

    def __init__(self, fieldName, value=None):
        super(SpecialField, self).__init__()
        words = fieldName.split(' ')
        if len(words) == 1:
            self.namesWrapper.clear_widgets(children=[self.nameSecondRow])
            self.nameFirstRow.text = words[0]
            self.nameFirstRow.font_size = calculateFontSize(words[0], self.width)
        else:
            self.nameFirstRow.text, self.nameSecondRow.text = words[0], words[1]
            firstSize, secondSize = calculateFontSize(words[0], self.width), calculateFontSize(words[1], self.width)
            font_size = min(firstSize, secondSize)
            self.nameFirstRow.font_size, self.nameSecondRow.font_size = font_size, font_size
        if value:
            self.value.text = str(value) + " $"

    def markBoughtByPlayer(self, hexColor):
        for label in self.namesWrapper.children:
            label.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)


class SpecialHorizontalField(SpecialField):
    pass


class SpecialVerticalField(SpecialField):
    pass

class CornerBox(BoxLayout):
    imageSrc = StringProperty(None)