""" Here is gathered a logic for displaying house and hotel markers on the building area of the field """
# pylint: disable=no-name-in-module
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.utils import get_hex_from_color
# pylint: enable=no-name-in-module

__author__ = 'mateusz'

# pylint: disable=no-self-use
class FieldBuildingArea(GridLayout):
    """ This class manages displaying houses and hotel markers on the building area of the field """
    fieldColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(FieldBuildingArea, self).__init__(**kwargs)
        self.fieldColor = (1, 1, 1)

    def setHouse(self, houseNo):
        """ Sets 'h' characters for each house, or "HOTEL" word for a hotel """
        self.clear_widgets()
        for letter in "HOTEL" if houseNo == 5 else 'h' * houseNo:
            label = Label(
                text="[color=%s]%s[/color]" % (get_hex_from_color(self.inverseColor(self.fieldColor)), letter),
                font_size=self.getHouseSize(),
                markup=True)
            self.add_widget(label)

    def inverseColor(self, color):
        """ Returns an inverse color for a given. Used to choose a font color for a given background """
        return 1 - color[0], 1 - color[1], 1 - color[2]

    def getHouseSize(self):
        """ Returns default house marker size """
        return '12sp'


class VerticalFieldBuildingArea(FieldBuildingArea):
    """ This class represents building area inside vertical field """

    def getHouseSize(self):
        """ Returns house marker size for building areas inside vertical fields """
        return '12sp'


class HorizontalFieldBuildingArea(FieldBuildingArea):
    """ This class represents building area inside horizontal field """

    def getHouseSize(self):
        """ Returns house marker size for building areas inside horizontal fields """
        return '10sp'

# pylint: enable=no-self-use
