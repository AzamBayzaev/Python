import tkinter as tk
from tkinter import messagebox
import copy


BOARD_SIZE = 8
CELL_SIZE = 100
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + 30
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + 30
COORD_MARGIN = 30
COORD_BG = "#00FF00"
COORD_FG = "#000000"
BOARD_BG = "#F0D9B5"


white_pieces = {
    'pawn': '♙', 'rook': '♖', 'knight': '♘', 'bishop': '♗', 'queen': '♕', 'king': '♔'
}
black_pieces = {
    'pawn': '♟', 'rook': '♜', 'knight': '♞', 'bishop': '♝', 'queen': '♛', 'king': '♚'
}

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BOARD_BG)
        self.canvas.pack()
        self.selected = None
        self.pieces = {}
        self.current_turn = "white"
        self.game_over = False
        self.init_board()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.update_title()

    def init_board(self):
        for col, piece in enumerate(['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']):
            self.pieces[(col, 0)] = ('black', piece)
        for col in range(BOARD_SIZE):
            self.pieces[(col, 1)] = ('black', 'pawn')

        for col, piece in enumerate(['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']):
            self.pieces[(col, 7)] = ('white', piece)
        for col in range(BOARD_SIZE):
            self.pieces[(col, 6)] = ('white', 'pawn')

    def draw_board(self):
        self.canvas.delete("all")


        self.canvas.create_rectangle(0, 0, COORD_MARGIN, BOARD_SIZE * CELL_SIZE, fill=COORD_BG, outline=COORD_BG)

        self.canvas.create_rectangle(COORD_MARGIN, BOARD_SIZE * CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, fill=COORD_BG, outline=COORD_BG)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = COORD_MARGIN + col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        if self.selected is not None:
            col, row = self.selected
            x1 = COORD_MARGIN + col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

        for (col, row), (color, piece) in self.pieces.items():
            x = COORD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            symbol = white_pieces[piece] if color == 'white' else black_pieces[piece]
            self.canvas.create_text(x, y, text=symbol, font=("Arial", 36))

        for col in range(BOARD_SIZE):
            letter = chr(ord('a') + col)
            x = COORD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_SIZE * CELL_SIZE + (COORD_MARGIN // 2)
            self.canvas.create_text(x, y, text=letter, font=("Arial", 16, "bold"), fill=COORD_FG)

        for row in range(BOARD_SIZE):
            number = str(8 - row)
            x = COORD_MARGIN // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(x, y, text=number, font=("Arial", 16, "bold"), fill=COORD_FG)

    def update_title(self):
        title = f"Шахматы на Python. Ход: {self.current_turn.capitalize()}"
        if self.is_in_check(self.current_turn):
            title += " (Шах!)"
        self.root.title(title)

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.update_title()
        if self.is_in_check(self.current_turn):
            if self.is_checkmate(self.current_turn):
                messagebox.showinfo("Мат",
                                    f"Мат! Победили {'white' if self.current_turn == 'black' else 'black'}!\nКонец раунда.")
                self.game_over = True

    def path_clear(self, start, end):
        sc, sr = start
        ec, er = end
        dc = ec - sc
        dr = er - sr

        step_c = (dc // abs(dc)) if dc != 0 else 0
        step_r = (dr // abs(dr)) if dr != 0 else 0

        c, r = sc + step_c, sr + step_r
        while (c, r) != (ec, er):
            if (c, r) in self.pieces:
                return False
            c += step_c
            r += step_r
        return True

    def is_valid_move(self, start, end):
        if start not in self.pieces:
            return False
        piece_color, piece_type = self.pieces[start]
        sc, sr = start
        ec, er = end
        dx = ec - sc
        dy = er - sr

        if dx == 0 and dy == 0:
            return False

        if end in self.pieces:
            target_color, _ = self.pieces[end]
            if target_color == piece_color:
                return False

        if piece_type == 'pawn':
            if piece_color == 'white':

                if dx == 0 and dy == -1 and end not in self.pieces:
                    return True

                if sr == 6 and dx == 0 and dy == -2 and ((sc, sr - 1) not in self.pieces) and (end not in self.pieces):
                    return True

                if abs(dx) == 1 and dy == -1 and end in self.pieces:
                    return True
            else:

                if dx == 0 and dy == 1 and end not in self.pieces:
                    return True

                if sr == 1 and dx == 0 and dy == 2 and ((sc, sr + 1) not in self.pieces) and (end not in self.pieces):
                    return True

                if abs(dx) == 1 and dy == 1 and end in self.pieces:
                    return True
            return False

        elif piece_type == 'knight':
            return (abs(dx), abs(dy)) in [(2, 1), (1, 2)]

        elif piece_type == 'rook':
            if dx == 0 or dy == 0:
                return self.path_clear(start, end)
            return False

        elif piece_type == 'bishop':
            if abs(dx) == abs(dy):
                return self.path_clear(start, end)
            return False

        elif piece_type == 'queen':
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                return self.path_clear(start, end)
            return False

        elif piece_type == 'king':
            return max(abs(dx), abs(dy)) == 1

        return False

    def move_leaves_king_safe(self, start, end):
        board_copy = copy.deepcopy(self.pieces)
        piece_moved = board_copy[start]
        if end in board_copy:
            del board_copy[end]
        del board_copy[start]
        board_copy[end] = piece_moved

        original = self.pieces
        self.pieces = board_copy
        check_status = self.is_in_check(self.current_turn)
        self.pieces = original

        return not check_status

    def is_in_check(self, color):
        king_pos = None
        for pos, (piece_color, piece_type) in self.pieces.items():
            if piece_color == color and piece_type == "king":
                king_pos = pos
                break
        if king_pos is None:
            return False

        for (col, row), (piece_color, piece_type) in self.pieces.items():
            if piece_color != color:
                if self.is_valid_move((col, row), king_pos):
                    return True
        return False

    def is_checkmate(self, color):
        for start, (piece_color, piece_type) in self.pieces.items():
            if piece_color == color:
                for col in range(BOARD_SIZE):
                    for row in range(BOARD_SIZE):
                        end = (col, row)
                        if self.is_valid_move(start, end):
                            if self.move_leaves_king_safe(start, end):
                                return False
        return True

    def on_click(self, event):
        if self.game_over:
            return

        if event.x < COORD_MARGIN or event.x > COORD_MARGIN + BOARD_SIZE * CELL_SIZE or event.y < 0 or event.y > BOARD_SIZE * CELL_SIZE:
            return

        col = (event.x - COORD_MARGIN) // CELL_SIZE
        row = event.y // CELL_SIZE
        pos = (col, row)

        if self.selected is None:
            if pos in self.pieces and self.pieces[pos][0] == self.current_turn:
                self.selected = pos
        else:
            if pos == self.selected:
                self.selected = None
            else:
                if self.is_valid_move(self.selected, pos) and self.move_leaves_king_safe(self.selected, pos):
                    self.pieces[pos] = self.pieces[self.selected]
                    del self.pieces[self.selected]
                    self.selected = None
                    self.switch_turn()
                else:
                    if pos in self.pieces and self.pieces[pos][0] == self.current_turn:
                        self.selected = pos

        self.draw_board()

def main():
    root = tk.Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    game = ChessGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
