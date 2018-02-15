import socket
import struct

from board import Board

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 1337)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

BUFFER_SIZE = 64

board = Board()
board.output()

try:
    sock.send(b'Bot #1')
    data = sock.recv(1)
    print(data)
    print('Received the id')
    data = sock.recv(BUFFER_SIZE)
    #print('Received', data)
    unpacked = struct.unpack('17c', data)
    board.update(unpacked[1:])
    gameState = unpacked[:1]
    #print(gameState)
    #print(int.from_bytes(unpacked[7], byteorder='big'))
    print('Sending next move')
    sock.send(struct.pack('c', b'\x32'))
    #message = b'This is the message. It will be repeated.'
    #print('sending {!r}'.format(message))
    #sock.sendall(message)

    #amount_received = 0
    #amount_expected = len(message)

    #while amount_received < amount_expected:
    #    data = sock.recv(512)
    #    amount_received += len(data)
    #    print('Received: ', len(data))
    #    print('received {!r}'.format(data))
except Exception as e:
    print('Shit', e)
finally:
    print('closing socket')
    sock.close()

#import socket


#TCP_IP = '127.0.0.1'
#TCP_PORT = 1337
#BUFFER_SIZE = 1024
#MESSAGE = "Hello, World!"

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((TCP_IP, TCP_PORT))
#s.send(MESSAGE)
#data = s.recv(BUFFER_SIZE)
#s.close()

#print("received data:", data)