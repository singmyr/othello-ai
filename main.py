import socket
import struct
import traceback
import random
import sys

from board import Board


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder='big')

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
    player_id = bytes_to_int(data)
    print('Received the id', player_id)
    data = sock.recv(BUFFER_SIZE)
    unpacked = struct.unpack('17c', data)
    board.update(unpacked[1:])
    gameState = unpacked[:1]
    valid_moves = board.get_valid_moves(player_id)
    print(valid_moves)
    print('next move:', random.choice(valid_moves))
    #print(int.from_bytes(unpacked[7], byteorder='big'))
    print('Sending next move')
    sock.send(struct.pack('c', b'\x32'))
    data = sock.recv(1)
    if bytes_to_int(data) == 1:
        print('good move')
    else:
        print('bad move')
except Exception as e:
    print(traceback.format_exc())
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