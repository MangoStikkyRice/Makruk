# pieces.py

class Piece:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.abbreviation = ''
        self.name = 'Piece'  # Default name

    def get_possible_moves(self, board, position):
        raise NotImplementedError("This method should be overridden by subclasses.")

class Khun(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'K' if color == 'white' else 'k'
        self.name = 'Khun'

    def get_possible_moves(self, board, position):
        # Khun moves one square in any direction
        possible_moves = []
        x, y = position
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_on_board(nx, ny):
                target = board.grid[nx][ny]
                if target is None or target.color != self.color:
                    possible_moves.append((nx, ny))
        return possible_moves

class Met(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'Q' if color == 'white' else 'q'
        self.name = 'Met'

    def get_possible_moves(self, board, position):
        # Met moves one square diagonally
        possible_moves = []
        x, y = position
        directions = [(-1, -1), (-1, 1),
                      (1, -1),  (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_on_board(nx, ny):
                target = board.grid[nx][ny]
                if target is None or target.color != self.color:
                    possible_moves.append((nx, ny))
        return possible_moves

class Rua(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'R' if color == 'white' else 'r'
        self.name = 'Rua'

    def get_possible_moves(self, board, position):
        # Rua moves any number of squares horizontally or vertically
        possible_moves = []
        x, y = position
        directions = [(-1, 0), (1, 0),
                      (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if not board.is_on_board(nx, ny):
                    break
                target = board.grid[nx][ny]
                if target is None:
                    possible_moves.append((nx, ny))
                elif target.color != self.color:
                    possible_moves.append((nx, ny))
                    break
                else:
                    break
        return possible_moves

class Ma(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'N' if color == 'white' else 'n'
        self.name = 'Ma'

    def get_possible_moves(self, board, position):
        # Ma moves in an L-shape (similar to the Knight in chess)
        possible_moves = []
        x, y = position
        moves = [(-2, -1), (-2, 1),
                 (-1, -2), (-1, 2),
                 (1, -2),  (1, 2),
                 (2, -1),  (2, 1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if board.is_on_board(nx, ny):
                target = board.grid[nx][ny]
                if target is None or target.color != self.color:
                    possible_moves.append((nx, ny))
        return possible_moves

class Khon(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'B' if color == 'white' else 'b'
        self.name = 'Khon'

    def get_possible_moves(self, board, position):
        # Khon moves one square forward or diagonally forward
        possible_moves = []
        x, y = position
        direction = -1 if self.color == 'white' else 1
        moves = [(direction, -1), (direction, 0), (direction, 1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if board.is_on_board(nx, ny):
                target = board.grid[nx][ny]
                if target is None or target.color != self.color:
                    possible_moves.append((nx, ny))
        return possible_moves

class Bia(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = 'P' if color == 'white' else 'p'
        self.name = 'Bia'

    def get_possible_moves(self, board, position):
        # Bia moves one square forward, captures diagonally forward
        possible_moves = []
        x, y = position
        direction = -1 if self.color == 'white' else 1
        # Forward move
        nx, ny = x + direction, y
        if board.is_on_board(nx, ny) and board.grid[nx][ny] is None:
            possible_moves.append((nx, ny))
        # Diagonal captures
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if board.is_on_board(nx, ny):
                target = board.grid[nx][ny]
                if target is not None and target.color != self.color:
                    possible_moves.append((nx, ny))
        return possible_moves
