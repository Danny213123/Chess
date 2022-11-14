import copy

class GameState:
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

        self.enpassant_possible = ()

        self.pins = []
        self.checks = []

        self.white = True
        self.move_log = []

        self.current_castling_rights = castle_rights(True, True, True, True)
        self.castling_rights_log = [castle_rights(self.current_castling_rights.wks, self.current_castling_rights.wqs,
                                                  self.current_castling_rights.bks, self.current_castling_rights.bqs)]

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.pieceMoved
        self.move_log.append(move)
        self.white = not self.white

        if move.pieceMoved == "wK":
            self.white_king = (move.end_row, move.end_col)
        elif move.pieceMoved == "bK":
            self.black_king = (move.end_row, move.end_col)

        if move.pawn_promotion:
            self.board[move.end_row][move.end_col] = move.pieceMoved[0] + "Q"

        if move.enpassant_move:
            self.board[move.start_row][move.end_col] = "--"

        if move.pieceMoved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant_possible = ()

        if move.isCastleMove:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:  # Queen side
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"

        self.update_castle_rights(move)
        self.castling_rights_log.append(
            castle_rights(self.current_castling_rights.wks, self.current_castling_rights.wqs,
                          self.current_castling_rights.bks, self.current_castling_rights.bqs))

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

            if move.enpassant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.pieceEnd
                self.enpassant_possible = (move.end_row, move.end_col)

            if move.pieceMoved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()

            self.castling_rights_log.pop()
            self.current_castling_rights = copy.deepcopy(self.castling_rights_log[-1])

            if move.isCastleMove:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # Queen side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"

    def update_castle_rights(self, move):

        if move.pieceEnd == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.pieceEnd == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

        if move.pieceMoved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.pieceMoved == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.pieceMoved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False
        elif move.pieceMoved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False

    def get_valid_moves(self):

        #log = self.castling_rights_log[-1]
        #print (log.wks, log.wqs, log.bks, log.bks, end = "\n")

        temp_empassant_possible = self.enpassant_possible
        temp_castle = castle_rights(self.current_castling_rights.wks, self.current_castling_rights.wqs,
                                    self.current_castling_rights.bks, self.current_castling_rights.bqs)

        moves = self.get_possible_moves()

        if self.white:
            self.get_castle_moves(self.white_king[0], self.white_king[1], moves)
        else:
            self.get_castle_moves(self.black_king[0], self.black_king[1], moves)

        for x in range(len(moves) - 1, -1, -1):
            self.make_move(moves[x])

            self.white = not self.white
            if self.is_check():
                moves.remove(moves[x])
            self.white = not self.white
            self.undo_move()

        if len(moves) == 0:
            if self.is_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        self.current_castling_rights = temp_castle
        self.enpassant_possible = temp_empassant_possible
        return moves

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
                elif (row - 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, enpassant_move=True))

            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, enpassant_move=True))

        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, enpassant_move=True))

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, enpassant_move=True))

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
        ally = "w" if self.white else "b"
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

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
        ally = "w" if self.white else "b"
        for x in range(8):
            end_row = row + directions[x][0]
            end_col = col + directions[x][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return
        if (self.white and self.current_castling_rights.wks) or (not self.white and self.current_castling_rights.bks):
            self.get_king_side_castle_moves(row, col, moves)
        if (self.white and self.current_castling_rights.wqs) or (not self.white and self.current_castling_rights.bqs):
            self.get_queen_side_castle_moves(row, col, moves)

    def get_king_side_castle_moves(self, row, col, moves):
        if self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--":
            if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

    def get_queen_side_castle_moves(self, row, col, moves):
        if self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" and self.board[row][col - 3]:
            if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove=True))


class castle_rights:
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs


class Move:

    def __init__(self, start_sq, end_sq, board, enpassant_move=False, isCastleMove=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        self.pawn_promotion = False

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        self.pieceMoved = board[self.start_row][self.start_col]
        self.pieceEnd = board[self.end_row][self.end_col]

        if (self.pieceMoved == "wP" and self.end_row == 0) or (self.pieceMoved == "bP" and self.end_row == 7):
            self.pawn_promotion = True

        self.enpassant_move = enpassant_move

        if self.enpassant_move:
            self.pieceEnd = "bP" if self.pieceMoved[0] == "w" else "wP"

        self.isCastleMove = isCastleMove

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def print(self):
        print(self.pieceMoved, self.pieceEnd, (self.start_row, self.start_col), (self.end_row, self.end_col),
              self.moveID)
