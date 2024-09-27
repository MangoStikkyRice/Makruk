# board.py

import copy
from pieces import Khun, Met, Rua, Ma, Khon, Bia

class Board:
    def __init__(self):
        # Initialize an 8x8 board
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        self.last_move = None  # Tracks the last move made
        self.captured_pieces = {'white': [], 'black': []}  # Tracks captured pieces

    def is_on_board(self, x, y):
        """Check if the given coordinates are on the board."""
        return 0 <= x < 8 and 0 <= y < 8

    def setup_pieces(self):
        """Set up the initial positions of all pieces."""
        # Place White Bia (Pawns)
        for y in range(8):
            self.grid[5][y] = Bia('white')
        # Place White Rooks, Ma, Khon, Met, and Khun
        self.grid[7][0] = Rua('white')
        self.grid[7][1] = Ma('white')
        self.grid[7][2] = Khon('white')
        self.grid[7][3] = Met('white')
        self.grid[7][4] = Khun('white')
        self.grid[7][5] = Khon('white')
        self.grid[7][6] = Ma('white')
        self.grid[7][7] = Rua('white')

        # Place Black Bia (Pawns)
        for y in range(8):
            self.grid[2][y] = Bia('black')
        # Place Black Rooks, Ma, Khon, Met, and Khun
        self.grid[0][0] = Rua('black')
        self.grid[0][1] = Ma('black')
        self.grid[0][2] = Khon('black')
        self.grid[0][3] = Met('black')
        self.grid[0][4] = Khun('black')
        self.grid[0][5] = Khon('black')
        self.grid[0][6] = Ma('black')
        self.grid[0][7] = Rua('black')

    def move_piece(self, from_pos, to_pos):
        """
        Move a piece from from_pos to to_pos.
        Args:
            from_pos (tuple): (x, y) coordinates of the piece to move.
            to_pos (tuple): (x, y) coordinates of the destination.
        Returns:
            Tuple: (success (bool), result (str or dict))
        """
        x1, y1 = from_pos
        x2, y2 = to_pos
        piece = self.grid[x1][y1]
        target_piece = self.grid[x2][y2]

        if piece is None:
            return False, "No piece at the source position."

        possible_moves = piece.get_possible_moves(self, (x1, y1))
        if (x2, y2) not in possible_moves:
            return False, "Invalid move for that piece."

        # Move the piece
        self.grid[x2][y2] = piece
        self.grid[x1][y1] = None

        # Handle capture
        captured = None
        if target_piece is not None:
            # Add to captured pieces
            self.captured_pieces[target_piece.color].append(target_piece)
            captured = target_piece

        # Handle promotion for Bia
        if isinstance(piece, Bia):
            promotion_row = 0 if piece.color == 'white' else 7
            if x2 == promotion_row:
                self.grid[x2][y2] = Met(piece.color)

        # Update last_move
        self.last_move = (from_pos, to_pos)

        return True, {"message": "Move executed.", "captured": captured}

    def display(self):
        """Display the current state of the board."""
        print("\n  a b c d e f g h")
        for x in range(8):
            print(8 - x, end=' ')
            for y in range(8):
                piece = self.grid[x][y]
                if piece is None:
                    print('.', end=' ')
                else:
                    print(piece.abbreviation, end=' ')
            print(8 - x)
        print("  a b c d e f g h\n")

    def get_board_state(self):
        """
        Generate a unique identifier for the current board state.
        Returns:
            tuple: A tuple of tuples representing the board.
        """
        state = []
        for row in self.grid:
            state_row = []
            for piece in row:
                if piece is None:
                    state_row.append('.')
                else:
                    state_row.append(piece.abbreviation)
            state.append(tuple(state_row))
        return tuple(state)

    def evaluate_board(self):
        """
        Evaluate the board state from White's perspective.
        Returns:
            float: Evaluation score.
        """
        piece_values = {
            Khun: 1000,
            Met: 9,
            Rua: 5,
            Ma: 3,
            Khon: 3,
            Bia: 1
        }
        total = 0
        for x in range(8):
            for y in range(8):
                piece = self.grid[x][y]
                if piece is not None:
                    value = piece_values.get(type(piece), 0)

                    if 2 <= x <= 5 and 2 <= y <= 5:
                        value += 0.1

                    elif x == 0 or x == 7 or y == 0 or y == 7:
                        value -= 0.1

                    moves = piece.get_possible_moves(self, (x, y))
                    value += 0.05 * len(moves)
                    if piece.color == 'white':
                        total += value
                    else:
                        total -= value
        return total

    def get_all_possible_moves(self, color):
        """
        Get all possible moves for the given color.
        Args:
            color (str): 'white' or 'black'.
        Returns:
            list: List of moves, each move is ((x1, y1), (x2, y2)).
        """
        moves = []
        for x in range(8):
            for y in range(8):
                piece = self.grid[x][y]
                if piece is not None and piece.color == color:
                    positions = piece.get_possible_moves(self, (x, y))
                    for pos in positions:
                        moves.append(((x, y), pos))
        return moves

    def get_possible_moves_excluding_reverse(self, color):
        """
        Get all possible moves for the given color, excluding moves that reverse the last move.
        Args:
            color (str): 'white' or 'black'.
        Returns:
            list: Filtered list of moves.
        """
        all_moves = self.get_all_possible_moves(color)
        if not self.last_move:
            return all_moves
        reversed_last_move = (self.last_move[1], self.last_move[0])

        filtered_moves = [move for move in all_moves if move != reversed_last_move]
        return filtered_moves

    def minimax(self, depth, maximizing_player):
        """
        Minimax algorithm without alpha-beta pruning.
        Args:
            depth (int): Depth to search.
            maximizing_player (bool): True if the current layer is maximizing.
        Returns:
            tuple: (evaluation score, best move)
        """
        game_over, winner = self.is_game_over()
        if depth == 0 or game_over:
            return self.evaluate_board(), None

        color = 'white' if maximizing_player else 'black'
        possible_moves = self.get_possible_moves_excluding_reverse(color)

        if not possible_moves:
            return self.evaluate_board(), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_board = copy.deepcopy(self)
                success, result = new_board.move_piece(move[0], move[1])
                if not success:
                    continue  # Skip invalid moves
                eval, _ = new_board.minimax(depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_board = copy.deepcopy(self)
                success, result = new_board.move_piece(move[0], move[1])
                if not success:
                    continue  # Skip invalid moves
                eval, _ = new_board.minimax(depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def is_game_over(self):
        """
        Check if the game has ended.
        Returns:
            tuple: (True/False, winner ('white' or 'black') or None)
        """
        white_khun_exists = False
        black_khun_exists = False
        for row in self.grid:
            for piece in row:
                if isinstance(piece, Khun):
                    if piece.color == 'white':
                        white_khun_exists = True
                    elif piece.color == 'black':
                        black_khun_exists = True
        if not white_khun_exists:
            return True, 'black'
        if not black_khun_exists:
            return True, 'white'
        return False, None

    def get_captured_pieces(self, color):
        """
        Get the list of captured pieces for the given color.
        Args:
            color (str): 'white' or 'black'.
        Returns:
            list: List of captured Piece instances.
        """
        return self.captured_pieces[color]
