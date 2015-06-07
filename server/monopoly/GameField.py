from utils.eMonopoly import FieldType

__author__ = 'mateusz'


class GameField(object):
    def __init__(self, model):
        self.model = model
        self.owner = None
        self.houses = 0
        self.mortgage = False
        self.fieldSet = []

    def isDefault(self):
        return not self.owner and self.houses == 0 and not self.mortgage

    def isMonopolized(self):
        return all([field.owner == self.owner for field in self.getAssociatedFields()])

    def getFee(self, diceResult):
        if self.model.type == FieldType.TAX:
            return self.model.value
        if self.owner is None:
            return 0
        if self.model.type == FieldType.CITY:
            if self.houses == 0 and self.isMonopolized():
                return 2 * self.model.fees[0]
            return self.model.fees[self.houses]
        elif self.model.type == FieldType.AIRPORT:
            return 50 * sum(field.owner == self.owner for field in self.getAssociatedFields())
        elif self.model.type == FieldType.WATER_POWER:
            ownedFields = sum([field.owner == self.owner for field in self.getAssociatedFields()])
            return 4 * diceResult if ownedFields == 1 else 10 * diceResult
        return 0

    def getAssociatedFields(self):
        if self.model.type == FieldType.AIRPORT or self.model.type == FieldType.WATER_POWER:
            return filter(lambda field: field.model.type == self.model.type, self.fieldSet)
        if self.model.type == FieldType.CITY:
            return filter(lambda field: field.model.color == self.model.color, self.fieldSet)
        return []

    def toDictStateOnly(self):
        return {
            'owner': self.owner,
            'houses': self.houses,
            'mortgage': self.mortgage
        }