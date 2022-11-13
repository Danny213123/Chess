class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_function = {
            'P': self.get_pawn_moves, 'R': self.get_rook_moves, "N": self.get_knight_moves,
            'B': self.get_bishop_moves, 'Q': self.get_queen_moves, "K": self.get_king_moves

        }

        self.white_king = (7, 4)
        self.black_king = (0, 4)

        self.check_mate = False
        self.stale_mate = False
        self.in_check = False

        self.pins = []
        self.checks = []

        self.white = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.pieceMoved
        self.move_log.append(move)
        self.white = not self.white

        if move.pieceMoved == "wK":
            self.white_king = (move.end_row, move.end_col)
        elif move.pieceMoved == "bK":
            self.black_king = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) < 1:
            pass
        else:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.pieceMoved
            self.board[move.end_row][move.end_col] = move.pieceEnd
            self.white = not self.white

            if move.pieceMoved == "wK":
                self.white_king = (move.start_row, move.start_col)
            elif move.pieceMoved == "bK":
                self.black_king = (move.start_row, move.start_col)

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()

        if self.white:
            king_row, king_col = self.white_king[0], self.white_king[1]
        else:
            king_row, king_col = self.black_king[0], self.black_king[1]

        if self.in_check:
            if self.checks == 1:
                moves = self.get_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for x in range(1, 8):
                        valid_square = (king_row + check[2] * x, king_col + check[3] * x)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                for x in range(len(moves) - 1, -1, -1):
                    if moves[x].pieceMoved[1] != "K":
                        if not (moves[x].end_row, moves[x].end_col) in valid_squares:
                            moves.remove(moves[x])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_possible_moves()

        return moves

    def check_for_pins_and_checks(self):
        pins, checks = [], []
        in_check = False

        if self.white:
            enemy, ally, start_row, start_col = "b", "w", self.white_king[0], self.white_king[1]
        else:
            enemy, ally, start_row, start_col = "w", "b", self.black_king[0], self.black_king[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1))
        for x in range(len(directions)):
            d = directions[x]
            possible_pin = ()
            for y in range(1, 8):
                end_row = start_row + d[0] * y
                end_col = start_col + d[1] * y
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally:
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy:
                        type = end_piece[1]
                        if (0 <= x <= 3 and type == "R") or (4 <= x <= 7 and type == "B") or \
                                (y == 1 and type == "P" and ((enemy == "w" and 6 <= x <= 7) or (enemy == "b" and 4 <= x <= 5))) or \
                                (type == "Q") or (y == 1 and type == "K"):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy and end_piece[0] == "N":
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))

        return in_check, pins, checks

    def is_check(self):
        if self.white:
            return self.square_under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.square_under_attack(self.black_king[0], self.black_king[1])

    def square_under_attack(self, row, col):
        self.white = not self.white
        enemy_moves = self.get_possible_moves()
        self.white = not self.white
        for move in enemy_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def get_possible_moves(self):
        moves = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                turn = self.board[x][y][0]
                if (turn == "w" and self.white) or (turn == "b" and not self.white):
                    piece = self.board[x][y][1]
                    self.move_function[piece](x, y, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = "b" if self.white else "w"
        for d in directions:
            for x in range(1, 8):
                end_row = row + d[0] * x
                end_col = col + d[1] * x
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (-1, -2), (1, -2))
        enemy = "b" if self.white else "w"
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_piece[0] == enemy:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    break
                else:
                    break
            else:
                break

    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (1, 1), (-1, 1), (1, -1))
        enemy = "b" if self.white else "w"
        for d in directions:
            for x in range(1, 8):
                end_row = row + d[0] * x
                end_col = col + d[1] * x
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1))
        enemy = "b" if self.white else "w"
        for d in directions:
            for x in range(8):
                end_row = row + d[0]
                end_col = col + d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break


class Move():

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        self.pieceMoved = board[self.start_row][self.start_col]
        self.pieceEnd = board[self.end_row][self.end_col]

    def __eq__(self, other):
        if (isinstance(other, Move)):
            return self.moveID == other.moveID
        return False

    def print(self):
        print(self.pieceMoved, self.pieceEnd, (self.start_row, self.start_col), (self.end_row, self.end_col),
              self.moveID)
