import pygame
from chess_pieces import Rook, Knight, Bishop, Queen, Pawn, King
import chess_pieces

TILE_SIZE = 64
FPS = 60

pygame.init()
WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

chess_pieces.legal_image = pygame.image.load("imgs/legal_move.png")
chess_pieces.capture_image = pygame.image.load("imgs/capturable.png")

black_rook = pygame.image.load("imgs/black_rook.png")
black_knight = pygame.image.load("imgs/black_knight.png")
black_bishop = pygame.image.load("imgs/black_bishop.png")
black_queen = pygame.image.load("imgs/black_queen.png")
black_king = pygame.image.load("imgs/black_king.png")
black_pawn = pygame.image.load("imgs/black_pawn.png")

white_rook = pygame.image.load("imgs/white_rook.png")
white_knight = pygame.image.load("imgs/white_knight.png")
white_bishop = pygame.image.load("imgs/white_bishop.png")
white_queen = pygame.image.load("imgs/white_queen.png")
white_king = pygame.image.load("imgs/white_king.png")
white_pawn = pygame.image.load("imgs/white_pawn.png")

promotion_white = pygame.image.load("imgs/promotion_white.png")
promotion_black = pygame.image.load("imgs/promotion_black.png")

# For testing purposes
def show_board(board):
    for row in board:
        output = []
        for element in row:
            if type(element) == Pawn:
                output.append('p')
            elif type(element) == Knight:
                output.append('N')
            elif type(element) == Bishop:
                output.append('B')
            elif type(element) == Queen:
                output.append('Q')
            elif type(element) == King:
                output.append('K')
            elif type(element) == Rook:
                output.append('R')
            else:
                output.append('.')
        print(output)
    print("\n")

b_p = [Rook("black", [0, 0], black_rook), Knight("black", [0, 1], black_knight), 
       Bishop("black", [0, 2], black_bishop), Queen("black", [0, 3], black_queen), 
       King("black", [0, 4], black_king), Bishop("black", [0, 5], black_bishop), 
       Knight("black", [0, 6], black_knight), Rook("black", [0, 7], black_rook)]
for row in range(8):
    b_p.append(Pawn("black", [1, row], black_pawn))

w_p = [Rook("white", [7, 0], white_rook), Knight("white", [7, 1], white_knight), 
       Bishop("white", [7, 2], white_bishop), Queen("white", [7, 3], white_queen), 
       King("white", [7, 4], white_king), Bishop("white", [7, 5], white_bishop), 
       Knight("white", [7, 6], white_knight), Rook("white", [7, 7], white_rook)]
for row in range(8):
    w_p.append(Pawn("white", [6, row], white_pawn))

class Game:
    board = [b_p[:8], 
             b_p[8:]
            ]
    for i in range(4):
        board.append([None for _ in range(8)])
    board.append(w_p[8:])
    board.append(w_p[:8])

    def __init__(self, window):
        self.turn = w_p
        self.last_move = None
        self.renderer = Renderer(window)

    def opposite(self, side):
        if side == w_p:
            return b_p
        return w_p

    def mouse_to_square(self, pos):
        x, y = pos
        column = int(x / TILE_SIZE)
        row = int(y / TILE_SIZE)
        #if column % 64 != 0 and row % 0 != 0:
        return [row, column]

    def validated_moves(self, board, side, moves, active):
        validated_moves = {'moves': [], 'captures': []}

        for move in moves['moves']:
            current_pos = active.position
            saved_first = active.first_move
            if type(active) != King or (type(active) == King and abs(move[1]-current_pos[1]) != 2):
                active.move(board, move)
                if not self.in_check(board, side):
                    validated_moves['moves'].append(move)
                active.move(board, current_pos)
            else:
                if move[1] == current_pos[1]+2:
                    if not self.in_check(board, side):
                        active.move(board, [current_pos[0], current_pos[1]+1])
                        if not self.in_check(board, side):
                            active.move(board, [current_pos[0], current_pos[1]+2])
                            if not self.in_check(board, side):
                                validated_moves['moves'].append(move)
                    for i in range(2):
                        active.move(board, [current_pos[0], 5-i])
                else:
                    if not self.in_check(board, side):
                        active.move(board, [current_pos[0], current_pos[1]-1])
                        if not self.in_check(board, side):
                            active.move(board, [current_pos[0], current_pos[1]-2])
                            if not self.in_check(board, side):
                                validated_moves['moves'].append(move)
                    for i in range(2):
                        active.move(board, [current_pos[0], 3+i])
            active.first_move = saved_first

        for move in moves['captures']:
            current_pos = active.position
            captured_pos = move
            to_be_captured = board[captured_pos[0]][captured_pos[1]]
            
            saved_first = active.first_move

            if to_be_captured == None and type(active) == Pawn and type(self.last_move[0]) == Pawn:
                pawn_row, pawn_column = self.last_move[2]
                to_be_captured = board[pawn_row][pawn_column]
                captured_pos = self.last_move[2]

            self.opposite(side).remove(to_be_captured)
            active.move(board, move)
            if not self.in_check(board, side):
                validated_moves['captures'].append(move)

            active.move(board, current_pos)
            self.opposite(side).append(to_be_captured)
            board[captured_pos[0]][captured_pos[1]] = to_be_captured

            active.first_move = saved_first

        return validated_moves
    
    def in_check(self, board, side):
        for piece in side:
            if type(piece) == King:
                king = piece

        opposite_side = self.opposite(side)

        for piece in opposite_side:
            all_potential_moves = piece.legal_moves(board, previous_move=self.last_move)
            if king.position in all_potential_moves['moves'] or king.position in all_potential_moves['captures']:
                return True
            
        return False
    
    def pawn_promotion(self, board, side, pawn, promote_to):
        if side == w_p:
            color = "white"
        else: 
            color = "black"
        coords = pawn.position

        side.remove(pawn)
        if promote_to.lower() == "queen":
            new_piece = Queen(color, coords, pygame.image.load(f"imgs/{color}_queen.png"))
        elif promote_to.lower() == "bishop":
            new_piece = Bishop(color, coords, pygame.image.load(f"imgs/{color}_bishop.png"))
        elif promote_to.lower() == "knight":
            new_piece = Knight(color, coords, pygame.image.load(f"imgs/{color}_knight.png"))
        elif promote_to.lower() == "rook":
            new_piece = Rook(color, coords, pygame.image.load(f"imgs/{color}_rook.png"))
            
        side.append(new_piece)
        board[coords[0]][coords[1]] = new_piece
                          
        
    
    def checkmate(self, board, side):
        for piece in side:
            valid = self.validated_moves(board, side, piece.legal_moves(board, previous_move=self.last_move), piece)
            if valid['moves'] != [] or valid['captures'] != []:
                return 0
            
        if self.in_check(board, side):
            return 1
        else:
            return 0.5


    def play(self):
        run = True
        active_piece = 0
        legals = {"moves": [], "captures": []}
        promoting_pawn = None
        promote_coords = None
        while run:
            pos = pygame.mouse.get_pos()
            move = None
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    move = self.mouse_to_square(pos)
                    if promoting_pawn == None:
                        for piece in self.turn:
                            if piece.rect.collidepoint(pos):
                                if active_piece != 0:
                                    active_piece.active = False
                                piece.active = True
                                active_piece = piece
                    else:
                        pos_x, pos_y = pos
                        final_choice = None
                        if promote_coords[0] <= pos_x <= promote_coords[0] + TILE_SIZE:
                            starting_y = promote_coords[1]
                            choices = ["queen", "rook", "bishop", "knight"]
                            final_choice = None
                            for choice in choices:
                                if starting_y <= pos_y <= starting_y + TILE_SIZE:
                                    final_choice = choice
                                    break
                                starting_y += TILE_SIZE

                        if final_choice != None:
                            self.pawn_promotion(self.board, self.opposite(self.turn), promoting_pawn, final_choice)
                            promoting_pawn = None
                    
            if active_piece != 0 and move != None and promoting_pawn == None:
                legals = active_piece.legal_moves(self.board, previous_move=self.last_move)
                legals = self.validated_moves(self.board, self.turn, legals, active_piece)
                
                if move in legals["moves"] or move in legals["captures"]:
                    if move in legals["captures"]:
                        captured = self.board[move[0]][move[1]]
                        captured_pos = move
                        if captured == None:
                            captured_pos = self.last_move[2]
                            captured = self.board[captured_pos[0]][captured_pos[1]]
                        self.opposite(self.turn).remove(captured)
                        self.board[captured_pos[0]][captured_pos[1]] = None
                    
                    previous_pos = active_piece.position
                    self.turn = self.opposite(self.turn)
                    active_piece.move(self.board, move)
                    self.last_move = (active_piece, previous_pos, active_piece.position)

                    if type(active_piece) == Pawn and (active_piece.position[0] == 0 or active_piece.position[0] == 7):
                            promoting_pawn = active_piece

                    show_board(self.board)
                    active_piece.active = False
                    active_piece = 0

            game_state = self.checkmate(self.board, self.turn)
            if game_state == 1:
                run = False
                print(f"{self.opposite(self.turn)} wins!")
            elif game_state == 0.5:
                run = False
                print("Stalemate.")


            self.renderer.redraw_board(self.board, active_piece, legals)
            if promoting_pawn != None:
                promote_coords = self.renderer.render_promotion(promoting_pawn)

            pygame.display.update()

class Renderer:
    def __init__(self, window):
        self.window = window
        self.board_image = pygame.image.load("imgs/Board.png")

    def redraw_board(self, board, active, active_moves,):
        self.window.fill((255, 255, 200))
        self.window.blit(self.board_image, (0, 0))
        for row in board:
            for element in row:
                if element != None:
                    element.draw(self.window)

                    if element == active:
                        element.draw_legal(self.window, active_moves)
        
    def render_promotion(self, promoting_pawn):
        if promoting_pawn != None:
            if promoting_pawn.position[1] == 7:
                promote_image_coords = [promoting_pawn.rect.x - TILE_SIZE/2, promoting_pawn.rect.y + TILE_SIZE/2]
            else:
                promote_image_coords = [promoting_pawn.rect.x + TILE_SIZE/2, promoting_pawn.rect.y + TILE_SIZE/2]

            if promoting_pawn.color == "black":
                promote_image_coords[1] -= TILE_SIZE * 4
                self.window.blit(promotion_black, promote_image_coords)
            else:
                self.window.blit(promotion_white, promote_image_coords)


        if promote_image_coords != None:
            return promote_image_coords

x = Game(WIN)

x.play()

pygame.quit()
