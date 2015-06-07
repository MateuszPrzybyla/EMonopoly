__author__ = 'mateusz'


class FieldType(object):
    START = "START"
    CITY = "CITY"
    TAX = "TAX"
    DRAW_CHANCE = "CHANCE"
    DRAW_COMMUNITY = "COMMUNITY"
    JAIL = "JAIL"
    GO_TO_JAIL = "GO_TO_JAIL"
    AIRPORT = "AIRPORT"
    WATER_POWER = "WATER_POWER"
    PARKING = "PARKING"


class FieldColor(object):
    BROWN = "#8B4513"
    LIGHT_BLUE = "#87CEEB"
    PURPLE = "#9932CC"
    ORANGE = "#FFA500"
    RED = "#FF0000"
    YELLOW = "#FFFF00"
    GREEN = "#008000"
    DARK_BLUE = "0000FF"


class Field(object):
    def __init__(self, number, name, type, color=None, value=None, fees=[]):
        self.number = number
        self.name = name
        self.type = type
        self.color = color
        self.value = value
        self.fees = fees

    def isBuyable(self):
        return self.type in [FieldType.CITY, FieldType.AIRPORT, FieldType.WATER_POWER]

    def toDict(self):
        return {
            'number': self.number,
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'value': self.value,
            'fees' : self.fees
        }


GAME_FIELDS = [
    Field(0, 'Start', FieldType.START),

    Field(1, 'Vilnius', FieldType.CITY, FieldColor.BROWN, 60, [2, 10, 30, 90, 160, 250]),
    Field(2, 'Community Chest', FieldType.DRAW_COMMUNITY),
    Field(3, 'Riga', FieldType.CITY, FieldColor.BROWN, 60, [4, 20, 60, 180, 320, 450]),
    Field(4, 'Income Tax', FieldType.TAX, value=200),
    Field(5, 'Schiphol Airport', FieldType.AIRPORT, value=200),
    Field(6, 'Sofia', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [6, 30, 90, 270, 400, 550]),
    Field(7, 'Chance', FieldType.DRAW_CHANCE),
    Field(8, 'Bucharest', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [6, 30, 90, 270, 400, 550]),
    Field(9, 'Warsaw', FieldType.CITY, FieldColor.LIGHT_BLUE, 120, [8, 40, 100, 300, 450, 600]),

    Field(10, 'Jail', FieldType.JAIL),

    Field(11, 'Budapest', FieldType.CITY, FieldColor.PURPLE, 140, [10, 50, 150, 450, 625, 750]),
    Field(12, 'Electric Company', FieldType.WATER_POWER, value=150),
    Field(13, 'Bern', FieldType.CITY, FieldColor.PURPLE, 140, [10, 50, 150, 450, 625, 750]),
    Field(14, 'Helsinki', FieldType.CITY, FieldColor.PURPLE, 170, [12, 60, 180, 500, 700, 900]),
    Field(15, 'Frankfurt Airport', FieldType.AIRPORT, value=200),
    Field(16, 'Stockholm', FieldType.CITY, FieldColor.ORANGE, 180, [14, 70, 200, 550, 750, 950]),
    Field(17, 'Community Chest', FieldType.DRAW_COMMUNITY),
    Field(18, 'Vienna', FieldType.CITY, FieldColor.ORANGE, 180, [14, 70, 200, 550, 750, 950]),
    Field(19, 'Lisbon', FieldType.CITY, FieldColor.ORANGE, 200, [16, 80, 220, 600, 800, 1000]),

    Field(20, 'Parking', FieldType.PARKING),

    Field(21, 'Madrid', FieldType.CITY, FieldColor.RED, 220, [18, 90, 250, 700, 875, 1050]),
    Field(22, 'Chance', FieldType.DRAW_CHANCE),
    Field(23, 'Athens', FieldType.CITY, FieldColor.RED, 220, [18, 90, 250, 700, 875, 1050]),
    Field(24, 'Dublin', FieldType.CITY, FieldColor.RED, 240, [20, 100, 300, 750, 925, 1100]),
    Field(25, 'Paris Airport', FieldType.AIRPORT, value=200),
    Field(26, 'Copenhagen', FieldType.CITY, FieldColor.YELLOW, 260, [22, 110, 330, 800, 975, 1150]),
    Field(27, 'London', FieldType.CITY, FieldColor.YELLOW, 260, [22, 110, 330, 800, 975, 1150]),
    Field(28, 'Water Works', FieldType.WATER_POWER, value=150),
    Field(29, 'Luxembourg', FieldType.CITY, FieldColor.YELLOW, 280, [24, 120, 360, 850, 1025, 1200]),

    Field(30, 'Go to Jail', FieldType.GO_TO_JAIL),

    Field(31, 'Brussels', FieldType.CITY, FieldColor.GREEN, 300, [26, 130, 390, 900, 1100, 1275]),
    Field(32, 'Amsterdam', FieldType.CITY, FieldColor.GREEN, 300, [26, 130, 390, 900, 1100, 1275]),
    Field(33, 'Community Chest', FieldType.DRAW_COMMUNITY),
    Field(34, 'Rome', FieldType.CITY, FieldColor.GREEN, 320, [28, 150, 450, 1000, 1200, 1400]),
    Field(35, 'London Airport', FieldType.AIRPORT, value=200),
    Field(36, 'Chance', FieldType.DRAW_CHANCE),
    Field(37, 'Berlin', FieldType.CITY, FieldColor.DARK_BLUE, 350, [35, 175, 500, 1100, 1300, 1500]),
    Field(38, 'Luxury Tax', FieldType.TAX, value=100),
    Field(39, 'Paris', FieldType.CITY, FieldColor.DARK_BLUE, 400, [50, 200, 600, 1400, 1700, 2000]),

]

class MoveType(object):
    DICE = 'DICE'
    BUY = 'BUY'
    FEE = 'FEE'
    JAIL = 'JAIL'
    DRAW = 'DRAW'
    BID = 'BID'
    END = 'END'
    BROKEN = 'BROKEN'