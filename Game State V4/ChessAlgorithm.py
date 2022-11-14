score_dict = {"Q": 10, "B": 3, "R": 4, "N":3, "P": 1}

def minimax(gs, valid_move, depth, isminimax):

    if gs.check_mate or gs.stalemate:
        return 100
    else:
        return find_score



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
    best_score = -99999
    current_move = ""

    valid_moves = gs.get_valid_moves()

    for x in range(len(valid_moves)):
        score = minimax(gs, valid_moves[x], depth, False)

        if score > best_score:
            best_score = score
            current_move = valid_moves[x]

    return current_move
