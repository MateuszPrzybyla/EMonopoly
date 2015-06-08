import socket

from server.ClientPlayer import ClientPlayer
from server.GameClient import GameClient
from server.requestHandlers.Response import Response
from utils.socket import send


__author__ = 'mateusz'


class GameServer(object):
    def __init__(self, port):
        self.port = port
        self.connectedClients = dict()
        self.players = dict()
        self.rooms = dict()

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

    def getRoom(self, id):
        for room in self.rooms.values():
            if room.id == id:
                return room

    def notifyClientDisconnected(self, client):
        client.socket.close()
        if client in self.connectedClients and self.connectedClients[client]:
            self.clearPlayerData(self.connectedClients[client])
        if client in self.connectedClients:
            self.connectedClients.pop(client)
        print "Client %s disconnected. Connected clients: %d" % (client.address, len(self.connectedClients))

    def notifyNewPlayer(self, nick, clientSocket):
        self.players[nick] = ClientPlayer(nick, clientSocket)
        for connectedClient in self.connectedClients.keys():
            if connectedClient.socket == clientSocket:
                self.connectedClients[connectedClient] = self.players[nick]
                break
        print "Player %s joined the server" % nick
        return self.players[nick].id

    def notifyPlayerLeaveServer(self, clientSocket):
        for connectedClient in self.connectedClients.keys():
            if connectedClient.socket == clientSocket:
                print "Player %s leaved the server" % self.connectedClients[connectedClient].name
                self.clearPlayerData(self.connectedClients[connectedClient])
                self.connectedClients[connectedClient] = None
                return True
        return False

    def clearPlayerData(self, clientPlayer):
        if clientPlayer in self.rooms:
            self.rooms.pop(clientPlayer)
        self.players.pop(clientPlayer.name)
        if clientPlayer.joinedRoom and clientPlayer in clientPlayer.joinedRoom.players:
            clientPlayer.joinedRoom.players.remove(clientPlayer)

    def notifyNewRoom(self, clientPlayer, room):
        self.rooms[clientPlayer] = room
        print "Player %s created a room: %s (id: %d)" % (clientPlayer.name, room.name, room.id)

    def notifyCloseRoom(self, clientPlayer, room):
        for player in room.players:
            player.joinedRoom = None
        if clientPlayer in self.rooms:
            self.rooms.pop(clientPlayer)
            print "Closing a room %d" % room.id

    def broadcastAllPlayers(self, response):
        if isinstance(response, Response):
            msg = response.toJSON()
        else:
            msg = response
        for player in self.players.values():
            send(player.socket, msg)

    def broadcastAllRoom(self, room, response, skipAuthor = None):
        if isinstance(response, Response):
            msg = response.toJSON()
        else:
            msg = response
        for player in room.players:
            if player != skipAuthor:
                send(player.socket, msg)


if __name__ == "__main__":
    ports = [1234, 1235, 1236]
    for port in ports:
        try:
            print "Trying start on port %d" % port
            GameServer(port).run()
            print "Start on port %d" % port
        except Exception as e:
            print str(e)