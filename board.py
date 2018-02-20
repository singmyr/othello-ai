class Board:
    def __init__(self):
        self.board = [[0] * 8 for i in range(8)]
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        #self.board = [
        #    [2, 1, 1, 1, 1, 1, 1, 1],
        #    [2, 1, 1, 1, 1, 1, 2, 1],
        #    [2, 1, 2, 2, 1, 1, 1, 1],
        #    [2, 1, 2, 1, 1, 2, 2, 1],
        #    [2, 1, 2, 2, 2, 1, 2, 1],
        #    [2, 1, 2, 2, 2, 1, 2, 1],
        #    [2, 2, 2, 2, 1, 2, 2, 1],
        #    [2, 1, 1, 1, 1, 2, 2, 0]
        #]

    def __str__(self):
        return str(self.board)

    def update(self, boardData):
        row = 0
        col = 0
        for data in boardData:
            # Convert the byte string to integer.
            data = int.from_bytes(data, byteorder='big')

            # Find a prettier way to extract the data.
            first = (data & 0xC0) >> 6
            second = (data & 0x30) >> 4
            third = (data & 0x0C) >> 2
            fourth = (data & 0x03)

            # Find a better way to insert the data.
            self.board[row][col] = first
            self.board[row][col + 1] = second
            self.board[row][col + 2] = third
            self.board[row][col + 3] = fourth

            col += 4
            if col >= 8:
                col = 0
                row += 1
        self.output()

    def get_valid_moves(self, player_id):
        board = self.board

        def check_north(_x, _y):
            return True if _y > 0 and board[_y - 1][_x] > 0 and board[_y - 1][_x] != player_id else False

        def check_nort_east(_x, _y):
            return True if _x < 6 and _y > 0 and board[_y - 1][_x + 1] > 0 and board[_y - 1][_x + 1] != player_id else False

        def check_east(_x, _y):
            return True if _x < 6 and board[_y][_x + 1] > 0 and board[_y][_x + 1] != player_id else False

        def check_south_east(_x, _y):
            return True if _x < 6 and _y < 6 and board[_y + 1][_x + 1] > 0 and board[_y + 1][_x + 1] != player_id else False

        def check_south(_x, _y):
            return True if _y < 6 and board[_y + 1][_x] > 0 and board[_y + 1][_x] != player_id else False

        def check_south_west(_x, _y):
            return True if _x > 0 and _y < 6 and board[_y + 1][_x - 1] > 0 and board[_y + 1][_x - 1] != player_id else False

        def check_west(_x, _y):
            return True if _x > 0 and board[_y][_x - 1] > 0 and board[_y][_x - 1] != player_id else False

        def check_north_west(_x, _y):
            return True if _x > 0 and _y > 0 and board[_y - 1][_x - 1] > 0 and board[_y - 1][_x - 1] != player_id else False

        potentials = []

        for _y, row in enumerate(self.board):
            for _x, col in enumerate(row):
                if col == 0 and (check_north(_x, _y) or
                   check_nort_east(_x, _y) or
                   check_east(_x, _y) or
                   check_south_east(_x, _y) or
                   check_south(_x, _y) or
                   check_south_west(_x, _y) or
                   check_west(_x, _y) or
                   check_north_west(_x, _y)):
                    potentials.append([_x, _y])

        valid_moves = []
        for move in potentials:
            if self.slot_has_valid_move(move[0], move[1], player_id):
                valid_moves.append(move)

        return valid_moves

    def slot_has_valid_move(self, pos_x, pos_y, player_id):
        # Check north
        if pos_y > 1:
            opponent_found = False
            for _y in reversed(range(0, pos_y, 1)):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][pos_x] != 0 and self.board[_y][pos_x] != player_id))\
                    else False
                if opponent_found and self.board[_y][pos_x] == player_id:
                    return True
                if self.board[_y][pos_x] == 0 or self.board[_y][pos_x] == player_id:
                    break

        # Check north east
        if pos_x < 6 and pos_y > 1:
            opponent_found = False
            for _x, _y in zip(range(pos_x + 1, 7, 1), reversed(range(0, pos_y, 1))):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][_x] != 0 and self.board[_y][_x] != player_id)) \
                    else False
                if opponent_found and self.board[_y][_x] == player_id:
                    return True
                if self.board[_y][_x] == 0 or self.board[_y][_x] == player_id:
                    break

        # Check east
        if pos_x < 6:
            opponent_found = False
            for _x in range(pos_x + 1, 7, 1):
                opponent_found = True if (opponent_found or
                                          (self.board[pos_y][_x] != 0 and self.board[pos_y][_x] != player_id))\
                    else False
                if opponent_found and self.board[pos_y][_x] == player_id:
                    return True
                if self.board[pos_y][_x] == 0 or self.board[pos_y][_x] == player_id:
                    break

        # Check south east
        if pos_x < 6 and pos_y < 6:
            opponent_found = False
            for _x, _y in zip(range(pos_x + 1, 7, 1), range(pos_y + 1, 7, 1)):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][_x] != 0 and self.board[_y][_x] != player_id)) \
                    else False
                if opponent_found and self.board[_y][_x] == player_id:
                    return True
                if self.board[_y][_x] == 0 or self.board[_y][_x] == player_id:
                    break

        # Check south
        if pos_y < 6:
            opponent_found = False
            for _y in range(pos_y + 1, 7, 1):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][pos_x] != 0 and self.board[_y][pos_x] != player_id))\
                    else False
                if opponent_found and self.board[_y][pos_x] == player_id:
                    return True
                if self.board[_y][pos_x] == 0 or self.board[_y][pos_x] == player_id:
                    break

        # Check south west
        if pos_x > 1 and pos_y < 6:
            opponent_found = False
            for _x, _y in zip(reversed(range(0, pos_x, 1)), range(pos_y + 1, 7, 1)):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][_x] != 0 and self.board[_y][_x] != player_id)) \
                    else False
                if opponent_found and self.board[_y][_x] == player_id:
                    return True
                if self.board[_y][_x] == 0 or self.board[_y][_x] == player_id:
                    break

        # Check west
        if pos_x > 1:
            opponent_found = False
            for _x in reversed(range(0, pos_x, 1)):
                opponent_found = True if (opponent_found or
                                          (self.board[pos_y][_x] != 0 and self.board[pos_y][_x] != player_id))\
                    else False
                if opponent_found and self.board[pos_y][_x] == player_id:
                    return True
                if self.board[pos_y][_x] == 0 or self.board[pos_y][_x] == player_id:
                    break

        # Check north west
        if pos_x > 1 and pos_y < 6:
            opponent_found = False
            for _x, _y in zip(reversed(range(0, pos_x, 1)), reversed(range(0, pos_y, 1))):
                opponent_found = True if (opponent_found or
                                          (self.board[_y][_x] != 0 and self.board[_y][_x] != player_id)) \
                    else False
                if opponent_found and self.board[_y][_x] == player_id:
                    return True
                if self.board[_y][_x] == 0 or self.board[_y][_x] == player_id:
                    break

        return False

    def output(self):
        #var scores = this.board.getScores();
        #console.log(this.players.map((p) = > {
        #return `${p.name}(${scores[p.id]})`;}).join(' vs '));
        for row in self.board:
            output = ''
            for col in row:
                if col == 1:
                    output += '\x1b[33m\u2588\x1b[0m '
                elif col == 2:
                    output += '\x1b[32m\u2588\x1b[0m '
                else:
                    output += '\x1b[2m\x1b[37m\u2588\x1b[0m\x1b[0m '

            print(output)
