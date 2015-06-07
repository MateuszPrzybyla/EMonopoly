from Queue import Empty
from threading import Thread

from server.monopoly.GameMove import GameMove


__author__ = 'mateusz'


class Bid(object):
    def __init__(self, owner, value):
        self.owner = owner
        self.value = value


class BiddingResult(object):
    def __init__(self, winningBid, field):
        self.winningBid = winningBid
        self.field = field


class BiddingManager(Thread):
    def __init__(self, players, playersData, movesStack, field, resultCallback, bidQueue, bidTimeout,
                 waitForBidMoveEvent):
        super(BiddingManager, self).__init__()
        self.players = players
        self.playersData = playersData
        self.movesStack = movesStack
        self.field = field
        self.bidTimeout = bidTimeout
        self.waitForBidMoveEvent = waitForBidMoveEvent
        self.bidQueue = bidQueue
        self.resultCallback = resultCallback
        self.winningBid = Bid(None, 0)

    def run(self):
        lastMoveInQueue = GameMove.bidMove(self.players, 0, None, self.field)
        self.movesStack.append(lastMoveInQueue)
        self.waitForBidMoveEvent.set()
        while True:
            try:
                bid = self.bidQueue.get(block=True, timeout=self.bidTimeout)
                if bid.value > self.winningBid.value and self.playersData[bid.owner.id].balance >= bid.value:
                    self.winningBid = bid
                    print "Got new winning bid!"
                lastMoveInQueue = GameMove.bidMove(self.players, self.winningBid.value,
                                                   self.winningBid.owner, self.field)
                self.movesStack.append(lastMoveInQueue)
                self.waitForBidMoveEvent.set()
            except Empty:
                if self.winningBid.owner and self.winningBid.value > 0:
                    self.movesStack.remove(lastMoveInQueue)
                    self.resultCallback(BiddingResult(self.winningBid, self.field))
                    break