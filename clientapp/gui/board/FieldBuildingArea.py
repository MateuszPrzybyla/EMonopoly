from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.utils import get_hex_from_color

__author__ = 'mateusz'


class FieldBuildingArea(GridLayout):
    fieldColor = ObjectProperty()

    def __init__(self, **kwargs):
        super(FieldBuildingArea, self).__init__(**kwargs)
        self.fieldColor = (1, 1, 1)

    def setHouse(self, houseNo):
        self.clear_widgets()
        for letter in ("HOTEL" if houseNo == 5 else 'h' * houseNo):
            label = Label(
                text="[color=%s]%s[/color]" % (get_hex_from_color(self.inverseColor(self.fieldColor)), letter),
                font_size=self.getHouseSize(),
                markup=True)
            self.add_widget(label)

    def inverseColor(self, color):
        return 1 - color[0], 1 - color[1], 1 - color[2]

    def getHouseSize(self):
        return '12sp'


class VerticalFieldBuildingArea(FieldBuildingArea):
    def getHouseSize(self):
        return '12sp'


class HorizontalFieldBuildingArea(FieldBuildingArea):
    def getHouseSize(self):
        return '10sp'