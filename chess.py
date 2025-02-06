import pygame

TILE_SIZE = 64
FPS = 60

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

class Piece:
    def __init__(self, color, position, image):
        self.color = color
        self.image = image
        self.position = position
        self.rect = self.image.get_rect()
        self.active = False
        self.legal_image = pygame.image.load("imgs/legal_move.png")
        self.capture_image = pygame.image.load("imgs/capturable.png")

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
        print(row, column)
        board[row][column] = self

        board[current_position[0]][current_position[1]] = None
        self.position = [row, column]
        show_board(board)
        print("\n")


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
        return legal

class Pawn(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.first_move = True

    def legal_moves(self, board):
        legal = {"moves": [],
                "captures": []}
        row, column = self.position
        if self.color == "white":
            if board[row-1][column] == None:
                legal["moves"].append([row-1, column])
                if self.first_move and board[row-2][column] == None:
                    legal["moves"].append([row-2, column])

            if (column-1) >= 0 and board[row-1][column-1] != None and board[row-1][column-1].color != self.color:
                    legal['captures'].append([row-1, column-1])
            if (column+1) <= 7 and board[row-1][column+1] != None and board[row-1][column+1].color != self.color:
                    legal['captures'].append([row-1, column+1])
        
        else:
            if board[row+1][column] == None:
                legal["moves"].append([row+1, column])
                if self.first_move and board[row+2][column] == None:
                    legal["moves"].append([row+2, column])

            if board[row+1][column-1] != None and board[row+1][column-1].color != self.color:
                    legal['captures'].append([row+1, column-1])
            if board[row+1][column+1] != None and board[row+1][column+1].color != self.color:
                    legal['captures'].append([row+1, column+1])

        return legal
    
    def move(self, board, move):
        super().move(board, move)
        self.first_move = False

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
                        moves = element.legal_moves(self.board)
                        element.draw_legal(window, moves)

        pygame.display.update()

    def mouse_to_square(self, pos):
        x, y = pos
        column = int(x / TILE_SIZE)
        row = int(y / TILE_SIZE)
        #if column % 64 != 0 and row % 0 != 0:
        return [row, column]

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
                                print('ACTIVE')
                            else:
                                piece.active = True
                                active_piece = piece
                    
                    if active_piece != 0:
                        legals = active_piece.legal_moves(self.board)
                        move = self.mouse_to_square(pos)
                        if move in legals["moves"] or move in legals["captures"]:
                            if move in legals['moves']:
                                if self.turn == w_p:
                                    self.turn = b_p
                                else:
                                    self.turn = w_p

                            elif move in legals["captures"]:
                                captured = self.board[move[0]][move[1]]
                                if self.turn == w_p:
                                    b_p.remove(captured)
                                    self.turn = b_p
                                else:
                                    w_p.remove(captured)
                                    self.turn = w_p

                            active_piece.move(self.board, self.mouse_to_square(pos))
                            active_piece.active = False
                            active_piece = 0

            self.redraw_board(window)


x = Game()

pygame.init()
WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

x.play(WIN)

pygame.quit()
print(len(w_p))
print(len(b_p))