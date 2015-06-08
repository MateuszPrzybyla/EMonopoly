# pylint: disable=E1101
# pylint: disable=no-name-in-module
""" Widgets with logic for displaying single game field (city/special/corner)
"""
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
# pylint: enable=no-name-in-module

__author__ = 'mateusz'


def calculateFontSize(text, width):
    """ Calculates font size for displaying field name """
    return int(width * 0.75 / len(text))


def parseColor(color):
    """ Parses a color from hex representation to a triple """
    return get_color_from_hex(color)


class CityNameLabel(Label):
    """ Encapsulates styles for field name label on the field """
    ownerColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(CityNameLabel, self).__init__(**kwargs)
        self.ownerColor = (0, 0, 0, 1)


class FieldValueLabel(Label):
    """ Encapsulates styles for field value label on the field """
    ownerColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(FieldValueLabel, self).__init__(**kwargs)
        self.ownerColor = (0, 0, 0, 1)


class PlayerMarker(BoxLayout):
    """ Manages style of a player marker that is displayed on a field """
    markerColor = ObjectProperty()

    # pylint: disable=invalid-name
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
        # pylint: enable=invalid-name


class CityField(BoxLayout):
    """ Base widget for all city fields widgets """
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
        """ Resets the state of the widget to initial state - no owner with no houses """
        self.markBoughtByPlayer("#000000")
        self.buildingArea.setHouse(0)
        self.drawMortgage(False)

    def markBoughtByPlayer(self, hexColor):
        """ Marks that a field is owned by a player with given color """
        self.cityName.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)

    def setHouse(self, houseNo):
        """ Delegates displaying appropriate number of houses to the building area """
        self.buildingArea.setHouse(houseNo)

    def putPlayerOnField(self, playerNo, hexColor):
        """ Puts player marker on this field, marker is created by one of subclasses """
        marker = self.createPlayerMarker(playerNo, hexColor)
        if not marker:
            return
        self.playerMarkers[playerNo] = marker
        self.playerMarkerArea.add_widget(marker)

    def removePlayerFromField(self, playerNo):
        """ Removes player marker from this field """
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])

    def drawMortgage(self, isMortgage):
        """ Possibly draws two lines indicating that field is mortgaged """
        if isMortgage:
            with self.canvas.after:
                Color(0, 0, 0, mode='rgb')
                Line(points=(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), width=1)
                Line(points=(self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1]), width=1)
        else:
            self.canvas.after.clear()


# pylint: disable=no-self-use
class WestCityField(CityField):
    """ Class representing widget of the city field located on the west row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside horizontal fields (West/East) """
        return PlayerMarker(playerNo, hexColor, False)


class EastCityField(CityField):
    """ Class representing widget of the city field located on the east row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside horizontal fields (West/East) """
        return PlayerMarker(playerNo, hexColor, False)


class NorthCityField(CityField):
    """ Class representing widget of the city field located on the north row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside vertical fields (South/North) """
        return PlayerMarker(playerNo, hexColor, True)


class SouthCityField(CityField):
    """ Class representing widget of the city field located on the south row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside vertical fields (South/North) """
        return PlayerMarker(playerNo, hexColor, True)


class SpecialField(BoxLayout):
    """ Base widget for all non-city fields widgets (Airports, Chance/Community, Tax...) """
    namesWrapper = ObjectProperty()
    value = ObjectProperty()
    nameFirstRow = ObjectProperty()
    nameSecondRow = ObjectProperty()
    playerMarkerArea = ObjectProperty()

    # pylint: disable=invalid-name
    def __init__(self, fieldName, value=None):
        """ Depending on the number of words in the fieldName populates either one or two labels in the widget """
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
        # pylint: enable=invalid-name

    def setInitialState(self):
        """ Resets the state of the widget to initial state - no owner with no mortgage """
        self.markBoughtByPlayer("#000000")
        self.drawMortgage(False)

    def markBoughtByPlayer(self, hexColor):
        """ Marks that a field is owned by a player with given color """
        for label in self.namesWrapper.children:
            label.ownerColor = parseColor(hexColor)
        self.value.ownerColor = parseColor(hexColor)

    def putPlayerOnField(self, playerNo, hexColor):
        """ Puts player marker on this field, marker is created by one of subclasses """
        marker = self.createPlayerMarker(playerNo, hexColor)
        if marker:
            self.playerMarkers[playerNo] = marker
            self.playerMarkerArea.add_widget(marker)

    def removePlayerFromField(self, playerNo):
        """ Removes player marker from this field """
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])

    def drawMortgage(self, isMortgage):
        """ Possibly draws two lines indicating that field is mortgaged """
        if isMortgage:
            with self.canvas.after:
                Color(0, 0, 0, mode='rgb')
                Line(points=(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]), width=1)
                Line(points=(self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1]), width=1)
        else:
            self.canvas.after.clear()


class SpecialEastField(SpecialField):
    """ Class representing widget of the non-city field located on the east row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside horizontal fields (West/East) """
        return PlayerMarker(playerNo, hexColor, False)


class SpecialWestField(SpecialField):
    """ Class representing widget of the non-city field located on the west row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside horizontal fields (West/East) """
        return PlayerMarker(playerNo, hexColor, False)


class SpecialSouthField(SpecialField):
    """ Class representing widget of the non-city field located on the south row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside vertical fields (South/North) """
        return PlayerMarker(playerNo, hexColor, True)


class SpecialNorthField(SpecialField):
    """ Class representing widget of the non-city field located on the north row of the board """

    def createPlayerMarker(self, playerNo, hexColor):
        """ Creates a player marker with given color adjusted to be displayed inside vertical fields (South/North) """
        return PlayerMarker(playerNo, hexColor, True)


class CornerBox(BoxLayout):
    """ Widget that manages displaying corner fields (start/jail/park/go to jail) """
    imageSrc = StringProperty(None)
    playerMarkerArea = ObjectProperty()
    playerMarkerJailArea = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CornerBox, self).__init__(**kwargs)
        self.playerMarkers = dict()

    def putPlayerOnField(self, playerNo, hexColor, inJail):
        """ Puts player marker on this field. If marker should indicate that player is in jail,
            it is displayed in a special box layout """
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
        """ Creates a player marker with given color
            adjusted to be displayed inside corner fields (horizontal order) """
        return PlayerMarker(playerNo, hexColor, True)

    def removePlayerFromField(self, playerNo):
        """ Removes player marker from this field """
        if playerNo in self.playerMarkers:
            self.playerMarkerArea.clear_widgets(children=[self.playerMarkers[playerNo]])
            if self.playerMarkerJailArea:
                self.playerMarkerJailArea.clear_widgets(children=[self.playerMarkers[playerNo]])
                # pylint: enable=no-self-use
