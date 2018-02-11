class Board:
    def __init__(self):
        self.board = [[0] * 8 for i in range(8)]
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        print('created board')

    def __str__(self):
        return str(self.board)

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
