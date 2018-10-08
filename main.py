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


server_address = ('localhost', 1337)

BUFFER_SIZE = 64

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    board = Board()
    #board.output(1)
    #print(board.get_valid_moves(1))
    #print(board.slot_has_valid_move(2, 0, 2))
    #sys.exit()

    game_is_active = True
    try:
        # Wait to receive the player_id from the server.
        data = sock.recv(1)
        player_id = bytes_to_int(data)
        #print('Received the id', player_id)

        #time.sleep(5)

        while game_is_active:
            # print("\n - Beginning turn (id", player_id, ") -\n")
            data = sock.recv(BUFFER_SIZE)
            unpacked = struct.unpack('17c', data)
            board.update(unpacked[1:], player_id)
            #print(unpacked[1:])
            #print('Received board, player id =', player_id)
            # board.output(player_id)
            gameState = bytes_to_int(unpacked[:1][0])
            # Interpret game state
            # print('GameState:', gameState)
            if gameState & player_id == player_id:
                print('I won as player', player_id)
                board.output(player_id)
                game_is_active = False
            if gameState & 4 == 4:
                # print('DRAW')
                game_is_active = False
            if gameState & 8 == 8:
                if gameState & 16 == 16:
                    # print('No move, skipping turn')
                    continue
            else:
                # print('SHIT I LOST?!')
                game_is_active = False
            my_turn = True
            while game_is_active and my_turn:
                valid_moves = board.get_valid_moves(player_id)
                # print(valid_moves)
                if valid_moves == None:
                    # print('I don\'t have any active moves?!')
                    sys.exit()
                next_move = random.choice(valid_moves)
                #next_move = [6, 5]
                #print('Sending next move', next_move)
                move = 0
                move += next_move[0] << 4
                move += next_move[1]
                sock.send(struct.pack('c', bytes([move])))
                data = sock.recv(1)
                if bytes_to_int(data) == 1:
                    #print('good move')
                    my_turn = False
                    # print(" - Ended turn - ")
                else:
                    # print(board.board)
                    # print('bad move, try another move')
                    #print(bytes_to_int(data))
                    #board.output(player_id)
                    sys.exit()
    except Exception as e:
        print(traceback.format_exc())
        #sys.exit()
    finally:
        #print('closing socket')
        sock.close()