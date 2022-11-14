import random

score_dict = {"Q": 10, "B": 3, "R": 5, "N": 3, "P": 1, "K": 0}

knight_score = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
]

piece_position ={"N": knight_score}

DEPTH = 3


def find_best_move(gs, valid_moves):
    global next_move, counter
    counter = 0
    next_move = None
    random.shuffle(valid_moves)
    find_nega_max_alpha_beta(gs, valid_moves, DEPTH, -1000, 1000, 1 if gs.white else -1)
    print (counter)
    return next_move


def minimax(gs, valid_moves, depth, isminimax):
    global next_move

    if depth == 0:
        return find_score(gs.board)

    if isminimax:
        maxScore = -1000
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = minimax(gs, next_moves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return maxScore

    else:
        minScore = 1000
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = minimax(gs, next_moves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return minScore


def find_nega_max(gs, valid_moves, depth, turn):
    global counter
    global next_move

    counter += 1

    if depth == 0:
        return turn * score_board(gs)

    max_score = -1000
    for move in valid_moves:
        gs.make_move(move)

        next_moves = gs.get_valid_moves()
        score = -find_nega_max(gs, next_moves, depth - 1, -turn)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move

        gs.undo_move()
    return max_score


def find_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn):
    global next_move, counter
    counter += 1

    if depth == 0:
        return turn * score_board(gs)

    max_score = -1000
    for move in valid_moves:
        gs.make_move(move)

        next_moves = gs.get_valid_moves()
        score = -find_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move

        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def score_board(gs):
    if gs.check_mate:
        if gs.white:
            return -1000
        else:
            return 1000

    score = 0

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]

            piece_position_score = 0
            if square[1] == "N":
                piece_position_score = piece_position["N"][row][col]

            if square[0] == "w":
                score += score_dict[square[1]] + piece_position_score
            elif square[1] == "b":
                score -= score_dict[square[1]] + piece_position_score


    return score


def find_score(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += score_dict[square[1]]
            elif square[1] == "b":
                score -= score_dict[square[1]]
    return score


def find_best_score(gs, depth):
    print("here")
    print(minimax(gs, depth, False))
