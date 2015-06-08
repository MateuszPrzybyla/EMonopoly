__author__ = 'mateusz'

JAIL_POSITION = 10

class PlayerData(object):
    def __init__(self, fieldPosition=0, startBalance=1500):
        self.fieldPosition = fieldPosition
        self.singleMoveChanges = []
        self.singleMoveStart = fieldPosition
        self.balance = startBalance
        self.inJailTurns = 0
        self.inJail = False
        self.jailCards = []

    def movePlayer(self, moveSize):
        self.fieldPosition += moveSize
        self.fieldPosition %= 40
        self.singleMoveChanges.append(moveSize)
        return self.fieldPosition

    def movePlayerToField(self, fieldNumber, forward=True):
        change = (fieldNumber - self.fieldPosition + 40) % 40
        if not forward:
            change = 40 - change
        self.singleMoveChanges.append(change)
        self.fieldPosition = fieldNumber
        return self.fieldPosition

    def resetMove(self):
        self.singleMoveChanges = []
        self.singleMoveStart = self.fieldPosition

    def calculateStartPasses(self):
        startPasses = 0
        previous = self.singleMoveStart
        for change in self.singleMoveChanges:
            if previous + change >= 40 and change > 0:
                startPasses += 1
            previous = (previous + change + 40) % 40
        return startPasses

    def addBalance(self, change):
        self.balance += change

    def goToJail(self):
        self.inJailTurns = 0
        self.inJail = True
        self.fieldPosition = JAIL_POSITION
        self.resetMove()

    def isInJail(self):
        return self.inJail

    def countJailTurns(self):
        if self.inJail:
            self.inJailTurns += 1

    def turnsInJailLeft(self):
        if not self.inJail:
            return 0
        return 3 - self.inJailTurns

    def addJailCard(self, card):
        self.jailCards.append(card)

    def removeJailCard(self, card):
        self.jailCards.remove(card)

    def hasJailCard(self):
        return len(self.jailCards) > 0

    def quitJail(self):
        self.inJail = False
        self.inJailTurns = 0

    def toDict(self):
        return {
            'position': self.fieldPosition,
            'singleMoveChanges': self.singleMoveChanges,
            'singleMoveStart': self.singleMoveStart,
            'balance': self.balance,
            'inJail': self.inJail,
            'hasJailCard': self.hasJailCard()
        }
