__author__ = 'mateusz'

class UnknownMessageHandler(object):
    def handleRequest(self, msg, jsonMsg, gameServerSocket):
        print "Unknown message from server: %s" % jsonMsg