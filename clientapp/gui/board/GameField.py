from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
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


class PlayerMarker(BoxLayout):
    markerColor = ObjectProperty()

    def __init__(self, playerNo, markerColor, insideVerticalField, **kwargs):
        self.markerColor = parseColor(markerColor)
        super(PlayerMarker, self).__init__(**kwargs)
        label = Label(text='[b]%s[/b]' % str(playerNo), font_size='12sp', markup=True)
        self.size_hint = (.25, 1) if insideVerticalField else (1, .25)
        if insideVerticalField:
            self.pos_hint = {'x': .25 * (playerNo - 1), 'y': 0}
        else:
            self.pos_hint = {'x': 0, 'y': .25 * (4 - playerNo)}
        self.add_widget(label)


class CityField(BoxLayout):
    cityName = ObjectProperty()
    value = ObjectProperty()
    buildingArea = ObjectProperty()
    ownerColor = ObjectProperty()
    playerMarkerArea = ObjectProperty()

    def __init__(self, cityName, value, color):
        super(CityField, self).__init__()
        self.cityName.text = cityName
        self.cityName.font_size = str(calculateFontSize(cityName, self.width)) + 'sp'
        self.value.text = str(value) + " $"
        self.buildingArea.fieldColor = parseColor(color)
        self.ownerColor = (0, 0, 0)
        self.playerMarkers = dict()

    def setInitialState(self):
        self.markBoughtByPlayer("#000000")
        self.buildingArea.setHouse(0)

    def markBoughtByPlayer(self, hexColor):
        self.cityName.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)

    def setHouse(self, houseNo):
        self.buildingArea.setHouse(houseNo)

    def putPlayerOnField(self, playerNo, hexColor):
        marker = self.createPlayerMarker(playerNo, hexColor)
        if not marker:
            return
        self.playerMarkers[playerNo] = marker
        self.playerMarkerArea.add_widget(marker)

    def createPlayerMarker(self, playerNo, hexColor):
        return None

    def removePlayerFromField(self, playerNo):
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])

    def drawMortgage(self, isMortgage):
        if isMortgage:
            with self.canvas.after:
                Color(0, 0, 0, mode='rgb')
                Line(points=(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), width=1)
                Line(points=(self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1]), width=1)
        else:
            self.canvas.after.clear()


class WestCityField(CityField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, False)


class EastCityField(CityField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, False)


class NorthCityField(CityField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, True)


class SouthCityField(CityField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, True)


class SpecialField(BoxLayout):
    namesWrapper = ObjectProperty()
    value = ObjectProperty()
    nameFirstRow = ObjectProperty()
    nameSecondRow = ObjectProperty()
    playerMarkerArea = ObjectProperty()

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
        self.playerMarkers = dict()

    def setInitialState(self):
        self.markBoughtByPlayer("#000000")

    def markBoughtByPlayer(self, hexColor):
        for label in self.namesWrapper.children:
            label.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)

    def putPlayerOnField(self, playerNo, hexColor):
        marker = self.createPlayerMarker(playerNo, hexColor)
        if not marker:
            return
        self.playerMarkers[playerNo] = marker
        self.playerMarkerArea.add_widget(marker)

    def createPlayerMarker(self, playerNo, hexColor):
        return None

    def removePlayerFromField(self, playerNo):
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])

    def drawMortgage(self, isMortgage):
        if isMortgage:
            with self.canvas.after:
                Color(0, 0, 0, mode='rgb')
                Line(points=(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), width=1)
                Line(points=(self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1]), width=1)
        else:
            self.canvas.after.clear()



class SpecialEastField(SpecialField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, False)


class SpecialWestField(SpecialField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, False)


class SpecialSouthField(SpecialField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, True)


class SpecialNorthField(SpecialField):
    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, True)


class CornerBox(BoxLayout):
    imageSrc = StringProperty(None)
    playerMarkerArea = ObjectProperty()
    playerMarkerJailArea = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CornerBox, self).__init__(**kwargs)
        self.playerMarkers = dict()

    def putPlayerOnField(self, playerNo, hexColor, inJail):
        marker = self.createPlayerMarker(playerNo, hexColor)
        if not marker:
            return
        self.playerMarkers[playerNo] = marker
        if inJail:
            if self.playerMarkerJailArea:
                self.playerMarkerJailArea.add_widget(marker)
        else:
            self.playerMarkerArea.add_widget(marker)

    def createPlayerMarker(self, playerNo, hexColor):
        return PlayerMarker(playerNo, hexColor, True)

    def removePlayerFromField(self, playerNo):
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])
            if self.playerMarkerJailArea:
                self.playerMarkerJailArea.clear_widgets(children=[self.playerMarkers[playerNo]])