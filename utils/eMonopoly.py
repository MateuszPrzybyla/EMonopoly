__author__ = 'mateusz'


class FieldType(object):
    CITY = 1
    BONUS = 2
    DRAW = 3
    JAIL = 4
    RAIL = 5


class FieldColor(object):
    BROWN = 1
    LIGHT_BLUE = 2
    PURPLE = 3
    ORANGE = 4
    RED = 5
    YELLOW = 6
    GREEN = 7
    DARK_BLUE = 8


class Field(object):
    lastNumber = 0

    def __init__(self, name, type, color=None, price=None, fees=[]):
        self.number = Field.nextNumber()
        self.name = name
        self.type = type
        self.color = color
        self.price = price
        self.fees = fees

    @staticmethod
    def nextNumber():
        number = Field.lastNumber
        Field.lastNumber += 1
        return number


GAME_FIELDS = [
    Field('Start', FieldType.BONUS),

    Field('Vilnius', FieldType.CITY, FieldColor.BROWN, 60, [10, 30, 90, 160, 250]),
    Field('Riga', FieldType.CITY, FieldColor.BROWN, 60, [20, 60, 180, 320, 450]),

    Field('Sofia', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [30, 90, 270, 400, 550]),
    Field('Bucharest', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [30, 90, 270, 400, 550]),
    Field('Warsaw', FieldType.CITY, FieldColor.LIGHT_BLUE, 120, [40, 100, 300, 450, 600]),

    Field('Budapest', FieldType.CITY, FieldColor.PURPLE, 140, [50, 150, 450, 625, 750]),
    Field('Bern', FieldType.CITY, FieldColor.PURPLE, 140, [50, 150, 450, 625, 750]),
    Field('Helsinki', FieldType.CITY, FieldColor.PURPLE, 170, [60, 180, 500, 700, 900]),

    Field('Stockholm', FieldType.CITY, FieldColor.ORANGE, 180, [70, 200, 550, 750, 950]),
    Field('Vienna', FieldType.CITY, FieldColor.ORANGE, 180, [70, 200, 550, 750, 950]),
    Field('Lisbon', FieldType.CITY, FieldColor.ORANGE, 200, [80, 220, 600, 800, 100]),

    Field('Madrid', FieldType.CITY, FieldColor.RED, 220, [90, 250, 700, 875, 1050]),
    Field('Athens', FieldType.CITY, FieldColor.RED, 220, [90, 250, 700, 875, 1050]),
    Field('Dublin', FieldType.CITY, FieldColor.RED, 240, [100, 300, 750, 925, 1100]),

    Field('Copenhagen', FieldType.CITY, FieldColor.YELLOW, 260, [110, 330, 800, 975, 1150]),
    Field('London', FieldType.CITY, FieldColor.YELLOW, 260, [110, 330, 800, 975, 1150]),
    Field('Luxembourg', FieldType.CITY, FieldColor.YELLOW, 280, [120, 360, 850, 1025, 1200]),

    Field('Brussels', FieldType.CITY, FieldColor.GREEN, 300, [130, 390, 900, 1100, 1275]),
    Field('Amsterdam', FieldType.CITY, FieldColor.GREEN, 300, [130, 390, 900, 1100, 1275]),
    Field('Rome', FieldType.CITY, FieldColor.GREEN, 320, [150, 450, 1000, 1200, 1400]),

    Field('Berlin', FieldType.CITY, FieldColor.DARK_BLUE, 350, [175, 500, 1100, 1300, 1500]),
    Field('Paris', FieldType.CITY, FieldColor.DARK_BLUE, 400, [200, 600, 1400, 1700, 2000]),

    # ------ copy ------
    Field('Vilnius', FieldType.CITY, FieldColor.BROWN, 60, [10, 30, 90, 160, 250]),
    Field('Riga', FieldType.CITY, FieldColor.BROWN, 60, [20, 60, 180, 320, 450]),

    Field('Sofia', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [30, 90, 270, 400, 550]),
    Field('Bucharest', FieldType.CITY, FieldColor.LIGHT_BLUE, 100, [30, 90, 270, 400, 550]),
    Field('Warsaw', FieldType.CITY, FieldColor.LIGHT_BLUE, 120, [40, 100, 300, 450, 600]),

    Field('Budapest', FieldType.CITY, FieldColor.PURPLE, 140, [50, 150, 450, 625, 750]),
    Field('Bern', FieldType.CITY, FieldColor.PURPLE, 140, [50, 150, 450, 625, 750]),
    Field('Helsinki', FieldType.CITY, FieldColor.PURPLE, 170, [60, 180, 500, 700, 900]),

    Field('Stockholm', FieldType.CITY, FieldColor.ORANGE, 180, [70, 200, 550, 750, 950]),
    Field('Vienna', FieldType.CITY, FieldColor.ORANGE, 180, [70, 200, 550, 750, 950]),
    Field('Lisbon', FieldType.CITY, FieldColor.ORANGE, 200, [80, 220, 600, 800, 100]),

    Field('Madrid', FieldType.CITY, FieldColor.RED, 220, [90, 250, 700, 875, 1050]),
    Field('Athens', FieldType.CITY, FieldColor.RED, 220, [90, 250, 700, 875, 1050]),
    Field('Dublin', FieldType.CITY, FieldColor.RED, 240, [100, 300, 750, 925, 1100]),

    Field('Copenhagen', FieldType.CITY, FieldColor.YELLOW, 260, [110, 330, 800, 975, 1150]),
    Field('London', FieldType.CITY, FieldColor.YELLOW, 260, [110, 330, 800, 975, 1150]),
    Field('Luxembourg', FieldType.CITY, FieldColor.YELLOW, 280, [120, 360, 850, 1025, 1200]),

    Field('Brussels', FieldType.CITY, FieldColor.GREEN, 300, [130, 390, 900, 1100, 1275]),
    Field('Amsterdam', FieldType.CITY, FieldColor.GREEN, 300, [130, 390, 900, 1100, 1275]),
    Field('Rome', FieldType.CITY, FieldColor.GREEN, 320, [150, 450, 1000, 1200, 1400]),

    Field('Berlin', FieldType.CITY, FieldColor.DARK_BLUE, 350, [175, 500, 1100, 1300, 1500]),
    Field('Paris', FieldType.CITY, FieldColor.DARK_BLUE, 400, [200, 600, 1400, 1700, 2000]),
]