import struct

__author__ = 'mateusz'


class ClientDisconnectedException(Exception):
    pass


def send(socket, msg):
    frmt = "=%ds" % len(msg)
    packedMsg = struct.pack(frmt, msg)
    packedHdr = struct.pack('=I', len(packedMsg))

    _send(socket, packedHdr)
    _send(socket, packedMsg)


def _send(socket, msg):
    sent = 0
    while sent < len(msg):
        sent += socket.send(msg[sent:])


def _read(socket, size):
    data = ''
    while len(data) < size:
        dataTmp = socket.recv(size - len(data))
        data += dataTmp
        if dataTmp == '':
            raise ClientDisconnectedException("socket connection broken")
    return data


def _msgLength(socket):
    d = _read(socket, 4)
    s = struct.unpack('=I', d)
    return s[0]


def read(socket):
    size = _msgLength(socket)
    data = _read(socket, size)
    frmt = "=%ds" % size
    return struct.unpack(frmt, data)[0]