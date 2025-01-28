import pygame

class Rook():
    def __init__(self, color):
        self.color = color
class Knight():
    def __init__(self, color):
        self.color = color
class Bishop():
    def __init__(self, color):
        self.color = color
class Queen():
    def __init__(self, color):
        self.color = color
class King():
    def __init__(self, color):
        self.color = color
class Pawn():
    def __init__(self, color):
        self.color = color
        self.first_move = True

    def legal_moves(self, position, board):
        legal = []
        row, column = position
        if self.color == "white":
            if board[row-1][column] == None:
                legal.append([row-1, column])
            if self.first_move and board[row-2][column] == None:
                legal.append([row-2, column])
        return legal


b_p = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")]
for row in range(8):
    b_p.append(Pawn("black"))

w_p = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]
for row in range(8):
    w_p.append(Pawn("white"))

back_rank = b_p
class Game:
    board = [b_p[:8], 
             b_p[8:]
            ]
    empty = [None for i in range(8)]
    for i in range(4):
        board.append(empty)
    board.append(w_p[8:])
    board.append(w_p[:8])

    def __init__(self):
        self.turn = "white"

    def pawn_move_check(self, move_made):
        row_dict = {"a": 0,
                    "b": 1}
        
        piece_exists = False

        for row in self.board:
            piece = self.board[row][move_made[0] - 'a']
            if type(piece) == Pawn and self.turn == piece.color:
                piece_exists = True
                break
        
        if piece_exists:
            pass

    def play(self):
        while True:
            move = input(f"{self.turn}'s move: ")
            if move[0].islower() and '1' <= move[1] <= '8':
                self.pawn_move_check()


x = Game()
moves = x.board[6][4].legal_moves([6, 4], x.board)
for i, row in enumerate(x.board):
    to_print = []
    for j, element in enumerate(row):
        piece = type(element)
        if piece == Rook:
            to_print.append('R')
        elif piece == Knight:
            to_print.append('N')
        elif piece == Bishop:
            to_print.append('B')
        elif piece == Queen:
            to_print.append('Q')
        elif piece == King:
            to_print.append('K')
        elif piece == Pawn:
            to_print.append('p')
        else:
            position = [i, j]
            if position in moves:
                to_print.append('O')
            else:
                to_print.append('.')

    print(to_print)

pygame.init()