import socket
from threading import Lock

from server.ClientPlayer import ClientPlayer
from server.GameClient import GameClient
from server.requestHandlers.Response import Response


__author__ = 'mateusz'


class GameServer(object):
    def __init__(self, port):
        self.port = port
        self.connectedClients = dict()
        self.players = dict()
        self.playersLock = Lock()
        self.rooms = list()

    def run(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((socket.gethostname(), self.port))
        print "Server bound to %s" % socket.gethostname()
        self.serverSocket.listen(5)
        try:
            while True:
                (clientSocket, address) = self.serverSocket.accept()
                client = GameClient(self, clientSocket, address)
                self.connectedClients[client] = None
                print "Handling client %s. Number of connected clients: %d" % (address, len(self.connectedClients))
                client.start()
        except Exception as e:
            print "Server exception %s" % e
        finally:
            self.serverSocket.close()
            print "Closing server..."

    def getClientPlayer(self, socket):
        for connectedClient in self.connectedClients.keys():
            if connectedClient.socket == socket:
                return self.connectedClients[connectedClient]

    def notifyClientDisconnected(self, client):
        client.socket.close()
        if self.connectedClients[client]:
            self.players.pop(self.connectedClients[client].name)
        self.connectedClients.pop(client)
        print "Client %s disconnected. Connected clients: %d" % (client.address, len(self.connectedClients))

    # to chyba idzie 2 razy?
    def notifyNewPlayer(self, nick, clientSocket):
        self.players[nick] = ClientPlayer(nick, clientSocket)
        for connectedClient in self.connectedClients.keys():
            if connectedClient.socket == clientSocket:
                self.connectedClients[connectedClient] = self.players[nick]
        print "Player %s joined the server" % nick

    def broadcastAllPlayers(self, response):
        if isinstance(response, Response):
            msg = response.toJSON()
        else:
            msg = response
        for player in self.players.values():
            player.socket.send(msg)


if __name__ == "__main__":
    ports = [1234, 1235]
    for port in ports:
        try:
            print "Trying start on port %d" % port
            GameServer(port).run()
            print "Start on port %d" % port
        except Exception as e:
            print str(e)