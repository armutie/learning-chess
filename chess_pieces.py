TILE_SIZE = 64
legal_image = None
capture_image = None

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
    
    def legal_moves(self, board, previous_move=None):
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

    def legal_moves(self, board, previous_move=None):
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

    def legal_moves(self, board, previous_move=None):
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

    def legal_moves(self, board, previous_move=None):
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

    def legal_moves(self, board, previous_move=None):
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

    def legal_moves(self, board, previous_move=None):
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
                if 0 <= (diagonal) <= 7:
                    if board[path][diagonal] != None and board[path][diagonal].color != self.color:
                        legal['captures'].append([path, diagonal])

                    if previous_move != None and type(previous_move[0]) == Pawn and abs(previous_move[2][0] - previous_move[1][0]) == 2:
                        if previous_move[0].position == [row, diagonal]:
                            legal['captures'].append([path, diagonal])

        return legal

class Queen(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)

    def legal_moves(self, board, previous_move=None):
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
