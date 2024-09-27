# makruk_game.py

from board import Board
from pieces import *
import sys

DIFFICULTY_LEVELS = {
    1: 1,  # Easy
    2: 2,  # Medium
    3: 3   # Hard
}

def parse_square(square):
    """
    Convert algebraic notation to board coordinates.
    Args:
        square (str): Square in algebraic notation (e.g., 'e3').
    Returns:
        tuple or None: (x, y) coordinates or None if invalid.
    """
    files = 'abcdefgh'
    ranks = '87654321'
    if len(square) != 2:
        return None
    y = files.find(square[0].lower())
    x = ranks.find(square[1])
    if x == -1 or y == -1:
        return None
    return x, y

def get_ai_difficulty(player_color):
    """
    Prompt the user to select AI difficulty.
    Args:
        player_color (str): 'White' or 'Black'.
    Returns:
        int: Depth corresponding to the selected difficulty.
    """
    while True:
        difficulty = input(f"Select difficulty for {player_color} AI (1-Easy, 2-Medium, 3-Hard): ")
        if difficulty in ['1', '2', '3']:
            return DIFFICULTY_LEVELS[int(difficulty)]
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")

def main():
    board = Board()
    board.display()

    # Choose game mode
    while True:
        game_mode = input("Choose game mode:\n1. Human vs Human\n2. Human vs AI\n3. AI vs AI\nEnter 1, 2 or 3: ")
        if game_mode in ['1', '2', '3']:
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

    # Set AI difficulty levels
    ai_difficulties = {'white': None, 'black': None}
    if game_mode == '2':
        ai_difficulties['black'] = get_ai_difficulty('Black')
    elif game_mode == '3':
        ai_difficulties['white'] = get_ai_difficulty('White')
        ai_difficulties['black'] = get_ai_difficulty('Black')

    current_player = 'white'

    # Initialize move history
    board_history = {}
    max_repetitions = 3  # Number of allowed repetitions
    move_limit = 1000     # Maximum number of moves to prevent infinite games
    total_moves = 0

    # Add initial board state
    initial_state = board.get_board_state()
    board_history[initial_state] = 1

    while True:
        print(f"{current_player.capitalize()}'s turn")
        if ai_difficulties[current_player]:
            # AI move
            depth = ai_difficulties[current_player]
            print(f"{current_player.capitalize()} AI is thinking at depth {depth}...")
            _, ai_move = board.minimax(depth, current_player == 'white')
            if ai_move is None:
                print(f"{current_player.capitalize()} AI has no moves left. Game over.")
                break
            from_pos, to_pos = ai_move
            success, result = board.move_piece(from_pos, to_pos)
            if not success:
                print(f"AI attempted an invalid move: {result}")
                break
            move_message = f"{current_player.capitalize()} AI moved from {chr(from_pos[1]+97)}{8 - from_pos[0]} to {chr(to_pos[1]+97)}{8 - to_pos[0]}"
            if result['captured']:
                captured_piece = result['captured']
                move_message += f", capturing {captured_piece.color.capitalize()} {captured_piece.name}"
            print(move_message)
        else:
            # Human move
            move_input = input("Enter your move (e.g., e3e4 or 'exit' to quit): ")
            if move_input.lower() == 'exit':
                print("Game ended by user.")
                break
            if len(move_input) != 4:
                print("Invalid input format. Please enter moves like 'e3e4'.")
                continue
            from_square = move_input[:2]
            to_square = move_input[2:]
            from_pos = parse_square(from_square)
            to_pos = parse_square(to_square)
            if from_pos is None or to_pos is None:
                print("Invalid move coordinates.")
                continue
            piece = board.grid[from_pos[0]][from_pos[1]]
            if piece is None:
                print("No piece at the source position.")
                continue
            if piece.color != current_player:
                print("You cannot move your opponent's pieces.")
                continue
            success, result = board.move_piece(from_pos, to_pos)
            if not success:
                print(result)
                continue
            move_message = f"{current_player.capitalize()} moved from {from_square.lower()} to {to_square.lower()}"
            if result['captured']:
                captured_piece = result['captured']
                move_message += f", capturing {captured_piece.color.capitalize()} {captured_piece.name}"
            print(move_message)

        board.display()
        total_moves += 1

        # Check for game over
        game_over, winner = board.is_game_over()
        if game_over:
            if winner:
                print(f"{winner.capitalize()} wins the game!")
            else:
                print("The game is a draw.")
            break

        # Check for repetition
        current_state = board.get_board_state()
        if current_state in board_history:
            board_history[current_state] += 1
            if board_history[current_state] >= max_repetitions:
                print("The game is a draw due to repetition of board states.")
                break
        else:
            board_history[current_state] = 1

        # Check for move limit
        if total_moves >= move_limit:
            print("The game is a draw due to reaching the maximum number of moves.")
            break

        # Switch player
        current_player = 'black' if current_player == 'white' else 'white'

        # Optionally, display captured pieces
        # Uncomment the following lines to see captured pieces after each move
        # print(f"Captured pieces:")
        # print(f"White: {[piece.name for piece in board.get_captured_pieces('white')]}")
        # print(f"Black: {[piece.name for piece in board.get_captured_pieces('black')]}")

    # Display final captured pieces
    print("\nFinal Captured Pieces:")
    print(f"White has captured: {[piece.name for piece in board.get_captured_pieces('white')]}")
    print(f"Black has captured: {[piece.name for piece in board.get_captured_pieces('black')]}")

if __name__ == "__main__":
    main()
