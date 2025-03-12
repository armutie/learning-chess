import pygame

TILE_SIZE = 64
FPS = 60

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

legal_image = pygame.image.load("imgs/legal_move.png")
capture_image = pygame.image.load("imgs/capturable.png")


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

class Piece:
    def __init__(self, color, position, image):
        self.color = color
        self.image = image
        self.position = position
        self.rect = self.image.get_rect()
        self.active = False
        self.legal_image = legal_image
        self.capture_image = capture_image
        self.first_move = True

    def draw(self, window):
        row, column = self.position
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE

        window.blit(self.image, (self.rect.x, self.rect.y))
    
    def legal_moves(self, board):
        pass

    def draw_legal(self, window, squares):
        for square in squares["moves"]:
            y = square[0] * TILE_SIZE
            x = square[1] * TILE_SIZE
            window.blit(self.legal_image, (x, y))
        for square in squares["captures"]:
            y = square[0] * TILE_SIZE
            x = square[1] * TILE_SIZE
            window.blit(self.capture_image, (x, y))

    def move(self, board, move):
        current_position = self.position
        row, column = move
        board[row][column] = self

        board[current_position[0]][current_position[1]] = None
        self.position = [row, column]
        self.first_move = False

class Rook(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        positions = [[0, 1], [0, -1], [-1, 0], [1, 0]]
        for vector in positions:
            current_row = row + vector[0]
            current_column = column + vector[1]

            while 0 <= current_row <= 7 and 0 <= current_column <= 7:
                if board[current_row][current_column] != None:
                    if board[current_row][current_column].color != self.color:
                        legal["captures"].append([current_row, current_column]) 
                    break
                else:
                    legal['moves'].append([current_row, current_column])
                    current_row += vector[0]
                    current_column += vector[1]

        return legal

class Knight(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        positions = [[row-2, column+1], [row-2, column-1], [row+2, column+1], [row+2, column-1], 
                     [row-1, column-2], [row+1, column-2], [row-1, column+2], [row+1, column+2]]
        for position in positions:
            if 0 <= position[0] <= 7 and 0 <= position[1] <= 7:
                square = board[position[0]][position[1]]
                if square != None:
                    if square.color != self.color:
                        legal['captures'].append(position)
                else:
                    legal['moves'].append(position)
            
        return legal


class Bishop(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        positions = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        for vector in positions:
            current_row = row + vector[0]
            current_column = column + vector[1]

            while 0 <= current_row <= 7 and 0 <= current_column <= 7:
                if board[current_row][current_column] != None:
                    if board[current_row][current_column].color != self.color:
                        legal["captures"].append([current_row, current_column]) 
                    break
                else:
                    legal["moves"].append([current_row, current_column])
                    current_row += vector[0]
                    current_column += vector[1]

        return legal

class King(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        positions = [[0, 1], [-1, 1], [1, 0], [-1, -1], [0, -1], [1, -1], [-1, 0], [1, 1]]
        for position in positions:
            current_row = row + position[0]
            current_column = column + position[1]

            if 0 <= current_row <= 7 and 0 <= current_column <= 7:
                if board[current_row][current_column] != None:
                    if board[current_row][current_column].color != self.color:
                        legal['captures'].append([current_row, current_column])
                else:
                    legal['moves'].append([current_row, current_column])

        if self.first_move and board[row][column+1] == None and board[row][column+2] == None:
            right_rook = board[row][column+3]
            if type(right_rook) == Rook and right_rook.first_move:
                legal['moves'].append([row, column+2])

        if self.first_move and board[row][column-1] == None and board[row][column-2] == None and board[row][column-3] == None:
            left_rook = board[row][column-4]
            if type(left_rook) == Rook and left_rook.first_move:
                legal['moves'].append([row, column-2])

        return legal
    
    def move(self, board, move):
        row_old, column_old = self.position
        super().move(board, move)
        row, column = self.position
        if column - column_old == 2:
            right_rook = board[row][column+1]
            right_rook.move(board, [row, column-1])
        elif column - column_old == -2:
            left_rook = board[row][column-2]
            left_rook.move(board, [row, column+1])

class Pawn(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.en_passant_vulnerability = False

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        if self.color == "white":
            path = row-1
            first = row-2
        else:
            path = row+1
            first = row+2

        if 0 <= path <= 7:
            if board[path][column] == None:
                    legal["moves"].append([path, column])
                    if self.first_move and board[first][column] == None:
                        legal["moves"].append([first, column])

            diagonals = [column-1, column+1]
            for diagonal in diagonals:
                if 0 <= (diagonal) <= 7 and board[path][diagonal] != None and board[path][diagonal].color != self.color:
                        legal['captures'].append([path, diagonal])

        return legal
    
    # def move(self, board, move):
    #     before = self.first_move
    #     super().move(board, move)
    #     after = self.first_move
    #     if before != after:
    #         self.en_passant_vulnerability = True
    #     else:
    #         self.en_passant_vulnerability = False

class Queen(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        positions = [[-1, -1], [-1, 1], [1, -1], [1, 1], [0, 1], [0, -1], [-1, 0], [1, 0]]
        for vector in positions:
            current_row = row + vector[0]
            current_column = column + vector[1]

            while 0 <= current_row <= 7 and 0 <= current_column <= 7:
                if board[current_row][current_column] != None:
                    if board[current_row][current_column].color != self.color:
                        legal["captures"].append([current_row, current_column]) 
                    break
                else:
                    legal["moves"].append([current_row, current_column])
                    current_row += vector[0]
                    current_column += vector[1]
        
        return legal

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

types = [Rook, Knight, Bishop, Queen, King, Pawn]

class Game:
    board = [b_p[:8], 
             b_p[8:]
            ]
    for i in range(4):
        board.append([None for _ in range(8)])
    board.append(w_p[8:])
    board.append(w_p[:8])

    def __init__(self):
        self.turn = w_p
        self.image = pygame.image.load("imgs/Board.png")

    def redraw_board(self, window):
        window.fill((255, 255, 200))
        window.blit(self.image, (0, 0))
        for row in self.board:
            for element in row:
                if type(element) in types:
                    element.draw(window)

                    if element.active:
                        valid_moves = self.validated_moves(self.board, self.turn, element.legal_moves(self.board), element)
                        element.draw_legal(window, valid_moves)

        pygame.display.update()

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
            to_be_captured = board[move[0]][move[1]]
            saved_first = active.first_move

            self.opposite(side).remove(to_be_captured)
            active.move(board, move)
            if not self.in_check(board, side):
                validated_moves['captures'].append(move)

            active.move(board, current_pos)
            self.opposite(side).append(to_be_captured)
            board[move[0]][move[1]] = to_be_captured

            active.first_move = saved_first

        return validated_moves
    
    def in_check(self, board, side):
        for piece in side:
            if type(piece) == King:
                king = piece

        opposite_side = self.opposite(side)

        for piece in opposite_side:
            all_potential_moves = piece.legal_moves(board)
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
            valid = self.validated_moves(board, side, piece.legal_moves(board), piece)
            if valid['moves'] != [] or valid['captures'] != []:
                return 0
            
        if self.in_check(board, side):
            return 1
        else:
            return 0.5


    def play(self, window):
        run = True
        active_piece = 0
        while run:
            pos = pygame.mouse.get_pos()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    for piece in self.turn:
                        if piece.rect.collidepoint(pos):
                            if active_piece != 0:
                                active_piece.active = False
                            piece.active = True
                            active_piece = piece
                    
                    if active_piece != 0:
                        
                        legals = active_piece.legal_moves(self.board)
                        legals = self.validated_moves(self.board, self.turn, legals, active_piece)
                        move = self.mouse_to_square(pos)
                        if move in legals["moves"] or move in legals["captures"]:
                            if move in legals["captures"]:
                                captured = self.board[move[0]][move[1]]
                                self.opposite(self.turn).remove(captured)
                            
                            self.turn = self.opposite(self.turn)
                            active_piece.move(self.board, move)

                            if type(active_piece) == Pawn and (active_piece.position[0] == 0 or active_piece.position[0] == 7):
                                choice = input("What would you like to promote to? ")
                                self.pawn_promotion(self.board, self.opposite(self.turn), active_piece, choice)

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

            self.redraw_board(window)


x = Game()

pygame.init()
WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

x.play(WIN)

pygame.quit()
