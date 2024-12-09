import tkinter as tk
import PIL
from PIL import Image, ImageTk
import os

PIECE_IMAGES = {
    'K': 'khun_w.png',
    'Q': 'met_w.png',
    'R': 'rua_w.png',
    'N': 'ma_w.png',
    'B': 'khon_w.png',
    'P': 'bia_w.png',
    'Qp': 'biangai_w.png',

    'k': 'khun_b.png',
    'q': 'met_b.png',
    'r': 'rua_b.png',
    'n': 'ma_b.png',
    'b': 'khon_b.png',
    'p': 'bia_b.png',
    'qp': 'biangai_b.png',
}

BOARD_SETUP = [
    ['r','n','b','q','k','b','n','r'],
    ['.','.','.','.','.','.','.','.'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['P','P','P','P','P','P','P','P'],
    ['.','.','.','.','.','.','.','.'],
    ['R','N','B','Q','K','B','N','R']
]

class MakrukGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Makruk (Thai Chess) 😏")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.msg_label = tk.Label(self.top_frame, text="Welcome to Makruk!", font=("Arial",16,"italic"), bg="lightyellow")
        self.msg_label.pack(side=tk.LEFT, padx=10)

        self.cell_size = 80
        self.canvas = tk.Canvas(self.root, width=8*self.cell_size, height=8*self.cell_size)
        self.canvas.pack()
        self.images = {}
        self.load_images()

        self.board = [row[:] for row in BOARD_SETUP]
        self.selected_piece = None
        self.selected_moves = []
        self.turn = 'White'  
        self.capture_log = {'White': [], 'Black': []}

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

    def load_images(self):
        for code, filename in PIECE_IMAGES.items():
            path = os.path.join("assets", filename)
            img = Image.open(path).convert("RGBA")
            img = img.resize((self.cell_size-10, self.cell_size-10), PIL.Image.LANCZOS)
            self.images[code] = ImageTk.PhotoImage(img)

    def is_white(self, piece):
        return piece.isupper()

    def is_black(self, piece):
        return piece.islower()

    def forward_direction(self, piece):
        return -1 if piece.isupper() else 1

    def on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_piece:
            if (row, col) in self.selected_moves:
                sr, sc = self.selected_piece
                self.selected_piece = None
                self.selected_moves = []
                self.animate_move(sr, sc, row, col)
                return
            else:
                self.selected_piece = None
                self.selected_moves = []
                self.draw_board()
                self.draw_pieces()

        else:

            piece = self.board[row][col]
            if piece != '.' and ((self.turn == 'White' and self.is_white(piece)) or (self.turn == 'Black' and self.is_black(piece))):
                self.selected_piece = (row, col)
                self.selected_moves = self.legal_moves(row, col)
                self.draw_board()
                self.draw_pieces()
                self.highlight_selection(row, col)
                self.highlight_moves(self.selected_moves)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                x1 = c*self.cell_size
                y1 = r*self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#DDB88C" if (r+c)%2==0 else "#A66D4F"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '.':
                    img_key = piece.upper()

                    if piece.upper() == 'Q' and ((piece.isupper() and r == 0) or (piece.islower() and r == 7)):
                        img_key = 'Qp' if piece.isupper() else 'qp'
                    elif piece.upper() == 'P':

                        img_key = 'P' if piece.isupper() else 'p'

                    if piece.isupper():
                        img = self.images[img_key]
                    else:
                        img_key = img_key.lower()
                        img = self.images[img_key]

                    x = c*self.cell_size + self.cell_size/2
                    y = r*self.cell_size + self.cell_size/2
                    self.canvas.create_image(x, y, image=img)

    def highlight_selection(self, r, c):
        x1 = c*self.cell_size
        y1 = r*self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)

    def highlight_moves(self, moves):
        for (r, c) in moves:
            x1 = c*self.cell_size
            y1 = r*self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=3)

    def move_piece(self, sr, sc, tr, tc):
        piece = self.board[sr][sc]
        target = self.board[tr][tc]

        if target != '.':

            capt_side = 'White' if piece.isupper() else 'Black'
            captured_piece = target.upper() if self.is_black(target) else target
            self.capture_log[capt_side].append(captured_piece)
            self.show_message(f"{self.turn} captured a {('Black' if self.is_black(target) else 'White')} {self.piece_name(target)}!")

        self.board[sr][sc] = '.'
        self.board[tr][tc] = piece

        if piece.upper() == 'P':
            if (piece.isupper() and tr == 0) or (piece.islower() and tr == 7):
                self.board[tr][tc] = 'Q' if piece.isupper() else 'q'


        self.turn = 'Black' if self.turn == 'White' else 'White'

    def animate_move(self, sr, sc, tr, tc):
        piece = self.board[sr][sc]
        target = self.board[tr][tc]

        img_key = piece.upper()
        if piece.upper() == 'Q' and ((piece.isupper() and sr == 0) or (piece.islower() and sr == 7)):
            img_key = 'Qp' if piece.isupper() else 'qp'
        elif piece.upper() == 'P':
            img_key = 'P' if piece.isupper() else 'p'

        if piece.isupper():
            anim_img = self.images[img_key]
        else:
            anim_img = self.images[img_key.lower()]

        start_x = sc*self.cell_size + self.cell_size/2
        start_y = sr*self.cell_size + self.cell_size/2
        end_x = tc*self.cell_size + self.cell_size/2
        end_y = tr*self.cell_size + self.cell_size/2

        steps = 10
        dx = (end_x - start_x)/steps
        dy = (end_y - start_y)/steps

        self.board[sr][sc] = '.'
        self.draw_board()
        self.draw_pieces()
        anim_id = self.canvas.create_image(start_x, start_y, image=anim_img)

        def step_move(i=0):
            if i < steps:
                self.canvas.move(anim_id, dx, dy)
                self.root.after(20, step_move, i+1)
            else:
                self.canvas.delete(anim_id)
                self.board[sr][sc] = piece
                self.move_piece(sr, sc, tr, tc)
                self.draw_board()
                self.draw_pieces()
                self.check_game_state()

        step_move()

    def piece_name(self, piece):
        name_map = {
            'K':'Khun (King)',
            'Q':'Met (Queen)',
            'R':'Rua (Rook)',
            'N':'Ma (Knight)',
            'B':'Khon (Bishop)',
            'P':'Bia (Pawn)'
        }
        return name_map[piece.upper()]

    def show_message(self, text):
        self.msg_label.config(text=text)

    def same_color(self, p1, p2):
        if p2 == '.':
            return False
        return (p1.isupper() and p2.isupper()) or (p1.islower() and p2.islower())

    def legal_moves(self, r, c):
        piece = self.board[r][c]
        moves = []
        if piece == '.':
            return moves
        if piece.upper() == 'K':
            directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'Q':  
            directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'R':
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
            for dr, dc in directions:
                nr, nc = r, c
                while True:
                    nr += dr
                    nc += dc
                    if not self.on_board(nr,nc):
                        break
                    if self.board[nr][nc] == '.':
                        moves.append((nr,nc))
                    else:
                        if not self.same_color(piece, self.board[nr][nc]):
                            moves.append((nr,nc))
                        break
        elif piece.upper() == 'N':
            knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
            for dr, dc in knight_moves:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'B':
            d = self.forward_direction(piece)
            directions = [(d,-1),(d,1)]
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'P':
            d = self.forward_direction(piece)
            fr, fc = r+d, c
            if self.on_board(fr,fc) and self.board[fr][fc] == '.':
                moves.append((fr,fc))
            for dcapt in [-1,1]:
                nr, nc = r+d, c+dcapt
                if self.on_board(nr,nc) and self.board[nr][nc] != '.' and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))

        legal = []
        for (mr, mc) in moves:
            if self.move_is_safe(r,c,mr,mc):
                legal.append((mr,mc))
        return legal

    def move_is_safe(self, sr, sc, tr, tc):
        piece = self.board[sr][sc]
        captured = self.board[tr][tc]
        self.board[tr][tc] = piece
        self.board[sr][sc] = '.'
        king_pos = self.find_king(piece.isupper())
        safe = not self.is_in_check(piece.isupper(), king_pos)
        self.board[sr][sc] = piece
        self.board[tr][tc] = captured
        return safe

    def find_king(self, white):
        target = 'K' if white else 'k'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r,c)
        return None

    def is_in_check(self, white, king_pos):
        if king_pos is None:
            return False
        (kr, kc) = king_pos
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != '.' and (self.is_white(p) != white):
                    moves = self.pseudo_legal_moves(r,c)
                    if king_pos in moves:
                        return True
        return False

    def pseudo_legal_moves(self, r, c):
        piece = self.board[r][c]
        moves = []
        if piece == '.':
            return moves
        if piece.upper() == 'K':
            dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'Q':
            dirs = [(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'R':
            dirs = [(-1,0),(1,0),(0,-1),(0,1)]
            for dr, dc in dirs:
                nr, nc = r, c
                while True:
                    nr += dr
                    nc += dc
                    if not self.on_board(nr,nc):
                        break
                    if self.board[nr][nc] == '.':
                        moves.append((nr,nc))
                    else:
                        if not self.same_color(piece, self.board[nr][nc]):
                            moves.append((nr,nc))
                        break
        elif piece.upper() == 'N':
            km = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
            for dr, dc in km:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'B':
            d = self.forward_direction(piece)
            dirs = [(d,-1),(d,1)]
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if self.on_board(nr,nc) and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        elif piece.upper() == 'P':
            d = self.forward_direction(piece)
            fr, fc = r+d, c
            if self.on_board(fr,fc) and self.board[fr][fc] == '.':
                moves.append((fr,fc))
            for dcapt in [-1,1]:
                nr, nc = r+d, c+dcapt
                if self.on_board(nr,nc) and self.board[nr][nc] != '.' and not self.same_color(piece, self.board[nr][nc]):
                    moves.append((nr,nc))
        return moves

    def check_game_state(self):
        white_turn = (self.turn == 'White')
        king_pos = self.find_king(white_turn)


        if king_pos is None:

            winner = "Black" if white_turn else "White"
            self.end_game(f"The {self.turn} player's king is gone! {winner} wins!")
            return

        in_check = self.is_in_check(white_turn, king_pos)
        moves_exist = False
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != '.' and ((white_turn and p.isupper()) or (not white_turn and p.islower())):
                    if self.legal_moves(r,c):
                        moves_exist = True
                        break
            if moves_exist:
                break

        if not moves_exist:
            if in_check:
                winner = "Black" if white_turn else "White"
                self.end_game(f"Checkmate! {self.turn} is checkmated. {winner} wins!")
            else:
                self.end_game("Stalemate! It's a draw, babe.")


    def end_game(self, message):
        self.show_message(message)
        self.canvas.unbind("<Button-1>")
        self.show_scoreboard(message)

    def show_scoreboard(self, message):
        top = tk.Toplevel(self.root)
        top.title("Game Over Stats")
        tk.Label(top, text=message, font=("Arial",18,"bold")).pack(pady=10)

        frame = tk.Frame(top)
        frame.pack(pady=10)

        tk.Label(frame, text="White captured:", font=("Arial",14,"bold")).grid(row=0, column=0, padx=5)
        tk.Label(frame, text=" ".join([self.piece_name(p) for p in self.capture_log['White']]) if self.capture_log['White'] else "None", font=("Arial",12)).grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Black captured:", font=("Arial",14,"bold")).grid(row=1, column=0, padx=5)
        tk.Label(frame, text=" ".join([self.piece_name(p) for p in self.capture_log['Black']]) if self.capture_log['Black'] else "None", font=("Arial",12)).grid(row=1, column=1, padx=5)

        tk.Button(top, text="Close", command=top.destroy, font=("Arial",12,"bold")).pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = MakrukGame()
    game.run()
