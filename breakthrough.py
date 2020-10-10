import random


class Breakthrough:
    White = 0
    Black = 1
    Opponent = [Black, White]

    class Board:
        NoPce = -1

        def __init__(self, cols, rows):
            assert (cols >= 2)
            assert (rows >= 4)
            self._cols = cols
            self._rows = rows
            self._board = [self.NoPce for _ in range(self._rows*self._cols)]
            self._hash_key = 0
            self._hash_board = [[random.getrandbits(64) for _ in range(self._rows*self._cols)] for _ in range(2)]
            return

        def cols(self):
            return self._cols

        def rows(self):
            return self._rows

        def sqr(self, c, r):
            assert(0 <= c < self.cols())
            assert(0 <= r < self.rows())
            return r * self.cols() + c

        def col(self, sqr):
            assert(0 <= sqr < self.rows() * self.cols())
            return sqr % self.cols()

        def row(self, sqr):
            assert(0 <= sqr < self.rows() * self.cols())
            return sqr // self.cols()

        def clear(self):
            self._board = [self.NoPce for _ in range(self._rows*self._cols)]
            self._hash_key = 0
            return

        def set(self, sqr, pce):
            assert(0 <= sqr < self.rows() * self.cols())
            if self._board[sqr] != self.NoPce:
                self._hash_key ^= self._hash_board[self._board[sqr]][sqr]
            self._hash_key ^= self._hash_board[pce][sqr]
            self._board[sqr] = pce
            return

        def set2d(self, c, r, pce):
            assert (0 <= c < self.cols())
            assert (0 <= r < self.rows())
            self.set(self.sqr(c, r), pce)

        def get(self, sqr):
            assert(0 <= sqr < self.rows() * self.cols())
            return self._board[sqr]

        def get2d(self, c, r):
            assert(0 <= c < self.cols())
            assert(0 <= r < self.rows())
            return self.get(self.sqr(c, r))

        def get_key(self):
            return self._hash_key

    def __init__(self, cols, rows):
        self._board = self.Board(cols, rows)
        self._to_move = self.White
        self._pce_count = [0, 0]
        self._hash_side = random.getrandbits(64)
        self.setup()
        return

    def __repr__(self):
        s = ""
        for r in range(self._board.rows()-1, -1, -1):
            for c in range(self._board.cols()):
                pce = self._board.get2d(c, r)
                if pce == self.White:
                    s += 'w'
                elif pce == self.Black:
                    s += 'b'
                else:
                    s += '.'
            s += '\n'
        if self._to_move == self.White:
            s += 'W'
        else:
            s += 'B'
        s += ' ' + str(self._pce_count[0]) + ' ' + str(self._pce_count[1])
        return s

    def get_to_move(self):
        return self._to_move

    def get_pce_count(self):
        return self._pce_count

    def get_board(self):
        return self._board

    def setup(self):
        self._to_move = self.White
        self._board.clear()
        for c in range(self._board.cols()):
            self._board.set2d(c, 0, self.White)
            self._board.set2d(c, 1, self.White)
            self._board.set2d(c, self._board.rows()-2, self.Black)
            self._board.set2d(c, self._board.rows()-1, self.Black)
        self._pce_count[0] = self._pce_count[1] = 2 * self._board.cols()
        return

    def is_terminal(self):
        if self._pce_count[0] == 0 or self._pce_count[1] == 0:
            return True
        for c in range(self._board.cols()):
            if self._board.get2d(c, 0) == self.Black or self._board.get2d(c, self._board.rows()-1) == self.White:
                return True
        return False

    def generate(self, shuffle=False):
        moves = []
        if self._to_move == self.White:
            for r in range(self._board.rows()-1):
                for c in range(self._board.cols()):
                    if self._board.get2d(c, r) == self.White:
                        if c > 0 and self._board.get2d(c-1, r+1) != self.White:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c-1, r+1), self._board.NoPce])
                        if self._board.get2d(c, r+1) == self._board.NoPce:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c, r+1), self._board.NoPce])
                        if c < self._board.cols() - 1 and self._board.get2d(c+1, r+1) != self.White:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c+1, r+1), self._board.NoPce])
        else:
            for r in range(self._board.rows()-1, 0, -1):
                for c in range(self._board.cols()):
                    if self._board.get2d(c, r) == self.Black:
                        if c > 0 and self._board.get2d(c-1, r-1) != self.Black:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c-1, r-1), self._board.NoPce])
                        if self._board.get2d(c, r-1) == self._board.NoPce:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c, r-1), self._board.NoPce])
                        if c < self._board.cols() - 1 and self._board.get2d(c+1, r-1) != self.Black:
                            moves.append([self._board.sqr(c, r), self._board.sqr(c+1, r-1), self._board.NoPce])
        if shuffle:
            random.shuffle(moves)
        return moves

    def make(self, move):
        sqr_from, sqr_to, _ = move
        pce = self._board.get(sqr_to)
        move[2] = pce
        if pce != self._board.NoPce:
            self._pce_count[self.Opponent[self._to_move]] -= 1
        self._board.set(sqr_to, self._board.get(sqr_from))
        self._board.set(sqr_from, self._board.NoPce)
        self._to_move = self.Opponent[self._to_move]
        return

    def retract(self, move):
        sqr_from, sqr_to, pce = move
        self._to_move = self.Opponent[self._to_move]
        self._board.set(sqr_from, self._board.get(sqr_to))
        self._board.set(sqr_to, pce)
        if pce != self._board.NoPce:
            self._pce_count[self.Opponent[self._to_move]] += 1
        return

    def get_key(self):
        if self._to_move == self.White:
            return self._board.get_key()
        else:
            return self._board.get_key() ^ self._hash_side
