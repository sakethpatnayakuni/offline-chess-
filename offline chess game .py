#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk

# Unicode chess symbols
PIECES = {
    "wP": "♙", "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔",
    "bP": "♟", "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚"
}

# Initial board setup
START_BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["wP"] * 8,
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

TILE_SIZE = 80
BOARD_SIZE = 8


class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Two Player Chess Game - Tkinter")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * TILE_SIZE, height=BOARD_SIZE * TILE_SIZE)
        self.canvas.pack()
        self.board = [row[:] for row in START_BOARD]
        self.selected = None
        self.turn = "w"
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = col * TILE_SIZE, row * TILE_SIZE
                x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text(
                        x1 + TILE_SIZE // 2, y1 + TILE_SIZE // 2,
                        text=PIECES[piece], font=("Arial", 36)
                    )

        if self.selected:
            r, c = self.selected
            x1, y1 = c * TILE_SIZE, r * TILE_SIZE
            x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def on_click(self, event):
        col = event.x // TILE_SIZE
        row = event.y // TILE_SIZE

        if self.selected:
            if (row, col) != self.selected and self.valid_move(self.selected, (row, col)):
                self.move_piece(self.selected, (row, col))
            self.selected = None
        else:
            piece = self.board[row][col]
            if piece and piece.startswith(self.turn):
                self.selected = (row, col)

        self.draw_board()

    def move_piece(self, src, dst):
        sr, sc = src
        dr, dc = dst
        self.board[dr][dc] = self.board[sr][sc]
        self.board[sr][sc] = ""
        self.turn = "b" if self.turn == "w" else "w"

    def valid_move(self, src, dst):
        sr, sc = src
        dr, dc = dst
        piece = self.board[sr][sc]
        target = self.board[dr][dc]
        dx, dy = dc - sc, dr - sr

        if target and target.startswith(self.turn):
            return False

        # Pawn
        if piece[1] == "P":
            direction = -1 if piece[0] == "w" else 1
            start_row = 6 if piece[0] == "w" else 1

            if sc == dc and not target:
                if dr == sr + direction:
                    return True
                if sr == start_row and dr == sr + 2 * direction and not self.board[sr + direction][sc]:
                    return True
            elif abs(dc - sc) == 1 and dr == sr + direction and target:
                return True

        # Rook
        elif piece[1] == "R":
            if sr == dr or sc == dc:
                return self.clear_path(sr, sc, dr, dc)

        # Bishop
        elif piece[1] == "B":
            if abs(dx) == abs(dy):
                return self.clear_path(sr, sc, dr, dc)

        # Queen
        elif piece[1] == "Q":
            if sr == dr or sc == dc or abs(dx) == abs(dy):
                return self.clear_path(sr, sc, dr, dc)

        # Knight
        elif piece[1] == "N":
            return (abs(dx), abs(dy)) in [(1, 2), (2, 1)]

        # King
        elif piece[1] == "K":
            return max(abs(dx), abs(dy)) == 1

        return False

    def clear_path(self, sr, sc, dr, dc):
        step_r = (dr - sr) // max(1, abs(dr - sr)) if sr != dr else 0
        step_c = (dc - sc) // max(1, abs(dc - sc)) if sc != dc else 0
        r, c = sr + step_r, sc + step_c

        while (r, c) != (dr, dc):
            if self.board[r][c]:
                return False
            r += step_r
            c += step_c

        return True


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()


# In[ ]:




