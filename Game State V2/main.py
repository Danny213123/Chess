import pygame as py
import ChessEngine

width = height = 512
dimension = 8
square_size = height // dimension

chess_images = {}

def load_images ():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        chess_images[piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (square_size, square_size))

def main():
    py.init()
    screen = py.display.set_mode((width, height))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    gs = ChessEngine.GameState()
    load_images()

    valid_moves = gs.get_valid_moves()
    made_move = False

    square_selected = ()
    player_clicks = []

    running = True
    while running:
        for e in py.event.get():
            #print (e)
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                col = location[0] // square_size
                row = location[1] // square_size
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append((row, col))
                if (len (player_clicks) == 2):
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    if move in valid_moves:
                        gs.make_move(move)
                        made_move = True
                        square_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [square_selected]

            elif e.type == py.KEYDOWN:
                if e.key == py.K_z:
                    gs.undo_move()
                    made_move = True

        if (made_move):
            valid_moves = gs.get_valid_moves()
            made_move = False
        draw_game_state(screen, gs)
        clock.tick(15)
        py.display.flip()

def draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)

def draw_board(screen):
    colours = [py.Color("white"), py.Color("brown")]
    for x in range(dimension):
        for y in range (dimension):
            colour = colours[((x+y) % 2)]
            py.draw.rect(screen, colour, py.Rect(y*square_size, x*square_size, square_size, square_size))

def draw_pieces(screen, board):
    for x in range (dimension):
        for y in range (dimension):
            piece = board[x][y]
            if piece != "--":
                screen.blit(chess_images[piece], py.Rect(y*square_size,x*square_size,square_size,square_size))

main()