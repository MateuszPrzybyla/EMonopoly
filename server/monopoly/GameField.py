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
        return all([field.owner == self.owner and self.owner for field in self.getAssociatedFields()])

    def getFee(self, diceResult, fixedCoeff=None):
        if self.model.type == FieldType.TAX:
            return self.model.value
        if self.owner is None:
            return 0
        if self.model.type == FieldType.CITY:
            if self.houses == 0 and self.isMonopolized():
                return 2 * self.model.fees[0]
            if self.houses > 5:
                return 0
            return self.model.fees[self.houses]
        elif self.model.type == FieldType.AIRPORT:
            return 50 * sum(field.owner == self.owner for field in self.getAssociatedFields())
        elif self.model.type == FieldType.WATER_POWER:
            ownedFields = sum([field.owner == self.owner for field in self.getAssociatedFields()])
            if fixedCoeff is not None:
                coeff = fixedCoeff
            elif ownedFields == 1:
                coeff = 4
            else:
                coeff = 10
            return coeff * diceResult
        return 0

    def getAssociatedFields(self):
        if self.model.type == FieldType.AIRPORT or self.model.type == FieldType.WATER_POWER:
            return filter(lambda field: field.model.type == self.model.type, self.fieldSet)
        if self.model.type == FieldType.CITY:
            return filter(lambda field: field.model.color == self.model.color, self.fieldSet)
        return []

    def canBuildHouse(self, playerId, houseChange=lambda houses: houses + 1, checkOwning=True):
        if self.model.type != FieldType.CITY or self.houses >= 5:
            return False
        associatedFields = self.getAssociatedFields()
        if checkOwning and any(field.owner != playerId or field.mortgage for field in associatedFields):
            return False
        houseLevels = [field.houses + 1 if field == self else field.houses
                       for field in associatedFields if field.owner == playerId]
        return max(houseLevels) - min(houseLevels) < 2

    def canSellHouse(self, playerId):
        if self.model.type != FieldType.CITY or self.houses <= 0:
            return False
        houseLevels = [field.houses - 1 if field == self else field.houses
                       for field in self.getAssociatedFields() if field.owner == playerId]
        return max(houseLevels) - min(houseLevels) < 2

    def sellHouse(self):
        if self.houses == 0:
            return 0
        soldValue = int(self.model.houseCost * 0.5)
        self.houses -= 1
        return soldValue

    def getHouseCost(self):
        if self.houses >= 5:
            return 0
        return self.model.houseCost

    def clearHouses(self):
        value = 0
        while self.houses > 0:
            value += self.sellHouse()
        return value

    def canDoMortgage(self, playerId):
        return self.owner == playerId and not self.mortgage and \
               all([field.houses == 0 for field in self.getAssociatedFields()])

    def getMortgageSellValue(self):
        return int(self.model.value * 0.5)

    def canLiftMortgage(self, playerId):
        return self.owner == playerId and self.mortgage

    def getMortgageBuyValue(self):
        return int(1.1 * self.getMortgageSellValue())

    def toDictStateOnly(self):
        return {
            'owner': self.owner,
            'houses': self.houses,
            'mortgage': self.mortgage
        }