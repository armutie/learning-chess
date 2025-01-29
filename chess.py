import pygame

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
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect()
        self.active = False
        self.legal_image = pygame.image.load("imgs/legal_move.png")

    def draw(self, window):
        row, column = self.position
        self.rect.x = column * 64
        self.rect.y = row * 64

        window.blit(self.image, (self.rect.x, self.rect.y))
    
    def legal_moves(self, board):
        pass

    def draw_legal(self, window, squares):
        for square in squares:
            y = square[0] * 64
            x = square[1] * 64
            window.blit(self.legal_image, (x, y))

    def move(self, board, move):
        current_position = self.position
        row, column = move
        print(row, column)
        show_board(board)
        board[row][column] = self
        print("\n")
        show_board(board)
        board[current_position[0]][current_position[1]] = None
        self.position = [row, column]


class Rook(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

class Knight(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board):
        pass

class Bishop(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

class Queen(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

class King(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

class Pawn(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.first_move = True

    def legal_moves(self, board):
        legal = []
        row, column = self.position
        if self.color == "white":
            if board[row-1][column] == None:
                legal.append([row-1, column])
            if self.first_move and board[row-2][column] == None:
                legal.append([row-2, column])
        else:
            if board[row+1][column] == None:
                legal.append([row+1, column])
            if self.first_move and board[row+2][column] == None:
                legal.append([row+2, column])
        return legal
    
    def move(self, board, move):
        super().move(board, move)
        self.first_move = False

# More efficient method coming
b_p = [Rook("black", [0, 0], "imgs/black_rook.png"), Knight("black", [0, 1], "imgs/black_knight.png"), 
       Bishop("black", [0, 2], "imgs/black_bishop.png"), Queen("black", [0, 3], "imgs/black_queen.png"), 
       King("black", [0, 4], "imgs/black_king.png"), Bishop("black", [0, 5], "imgs/black_bishop.png"), 
       Knight("black", [0, 6], "imgs/black_knight.png"), Rook("black", [0, 7], "imgs/black_rook.png")]
for row in range(8):
    b_p.append(Pawn("black", [1, row], "imgs/black_pawn.png"))

w_p = [Rook("white", [7, 0], "imgs/white_rook.png"), Knight("white", [7, 1], "imgs/white_knight.png"), 
       Bishop("white", [7, 2], "imgs/white_bishop.png"), Queen("white", [7, 3], "imgs/white_queen.png"), 
       King("white", [7, 4], "imgs/white_king.png"), Bishop("white", [7, 5], "imgs/white_bishop.png"), 
       Knight("white", [7, 6], "imgs/white_knight.png"), Rook("white", [7, 7], "imgs/white_rook.png")]
for row in range(8):
    w_p.append(Pawn("white", [6, row], "imgs/white_pawn.png"))

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
        column = int(x / 64)
        row = int(y / 64)
        #if column % 64 != 0 and row % 0 != 0:
        return [row, column]

    def play(self, window):
        run = True
        active_piece = 0
        while run:
            pos = pygame.mouse.get_pos()
            # buttons = pygame.mouse.get_pressed()
            
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    for piece in self.turn: # make for all
                        if type(piece) == Pawn:
                            if piece.rect.collidepoint(pos):
                                if active_piece != 0:
                                    active_piece.active = False
                                    piece.active = True
                                    active_piece = piece
                                    print('ACTIVE')
                                else:
                                    piece.active = True
                                    active_piece = piece
                    
                    if active_piece != 0 and self.mouse_to_square(pos) in active_piece.legal_moves(self.board):
                        active_piece.move(self.board, self.mouse_to_square(pos))
                        active_piece.active = False
                        active_piece = 0
                        if self.turn == w_p:
                            self.turn = b_p
                        else:
                            self.turn = w_p

            self.redraw_board(window)


x = Game()

pygame.init()
WIDTH, HEIGHT = 512, 512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

x.play(WIN)

pygame.quit()