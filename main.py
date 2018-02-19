import socket
import struct
import traceback
import random
import string
import sys
import time

from board import Board


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder='big')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 1337)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

BUFFER_SIZE = 64

board = Board()
#board.output()
#print(board.get_valid_moves(1))
#print(board.slot_has_valid_move(5, 4, 2))
#sys.exit()

game_is_active = True
try:
    name = random_generator()
    print('Bot name:', name)
    sock.send(bytes(name, 'utf-8'))
    data = sock.recv(1)
    player_id = bytes_to_int(data)
    print('Received the id', player_id)

    while game_is_active:
        data = sock.recv(BUFFER_SIZE)
        unpacked = struct.unpack('17c', data)
        board.update(unpacked[1:])
        gameState = unpacked[:1]
        # Interpret game state
        my_turn = True
        while my_turn:
            valid_moves = board.get_valid_moves(player_id)
            print(valid_moves)
            next_move = random.choice(valid_moves)
            print('Sending next move', next_move)
            move = 0
            move += next_move[0] << 4
            move += next_move[1]
            print(move)
            sock.send(struct.pack('c', bytes([move])))
            data = sock.recv(1)
            if bytes_to_int(data) == 1:
                print('good move')
                my_turn = False
            else:
                print('bad move, try another move')
                board.output()
                sys.exit()
            time.sleep(1)
    print('wtf')
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