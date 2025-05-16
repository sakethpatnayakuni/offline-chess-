import tkinter as tk
from PIL import Image, ImageTk
import chess
import chess.engine
import io
import os
import sys
import cairosvg
from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Set your Stockfish executable path
STOCKFISH_PATH = resource_path("C:/Users/saket/stockfish/stockfish.exe")  # Change if needed

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI vs Player Chess")
        self.board = chess.Board()
        self.square_size = 64
        self.selected_square = None
        self.images = {}

        self.canvas = tk.Canvas(root, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.load_images()
        self.draw_board()

        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    def load_images(self):
        pieces = ['r', 'n', 'b', 'q', 'k', 'p']
        colors = ['w', 'b']
        for color in colors:
            for piece in pieces:
                filename = resource_path(f"assets/{color}{piece}.svg")
                png_data = cairosvg.svg2png(url=filename, output_width=self.square_size, output_height=self.square_size)
                image = Image.open(io.BytesIO(png_data))
                self.images[color + piece] = ImageTk.PhotoImage(image)

    def draw_board(self):
        self.canvas.delete("all")
        color_flag = True
        for row in range(8):
            color_flag = not color_flag
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#EEEED2" if color_flag else "#769656"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                color_flag = not color_flag

                piece = self.get_piece_at(row, col)
                if piece:
                    self.canvas.create_image(x1, y1, anchor='nw', image=self.images[piece])

    def get_piece_at(self, row, col):
        square = chess.square(col, 7 - row)
        piece = self.board.piece_at(square)
        if piece:
            color = 'w' if piece.color == chess.WHITE else 'b'
            return color + piece.symbol().lower()
        return None

    def on_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size
        square = chess.square(col, 7 - row)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
                self.check_game_status()
                self.root.after(500, self.ai_move)
            else:
                self.selected_square = None
                self.draw_board()

    def ai_move(self):
        if self.board.is_game_over():
            return
        result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
        self.board.push(result.move)
        self.draw_board()
        self.check_game_status()

    def check_game_status(self):
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            messagebox.showinfo("Checkmate", f"{winner} wins by checkmate!")
            self.reset_board()
        elif self.board.is_stalemate():
            messagebox.showinfo("Stalemate", "It's a draw by stalemate.")
            self.reset_board()
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Draw", "Draw due to insufficient material.")
            self.reset_board()
        elif self.board.is_check():
            print("Check!")

    def reset_board(self):
        self.board.reset()
        self.selected_square = None
        self.draw_board()

    def quit(self):
        self.engine.quit()

# ✅ Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.quit(), root.destroy()))
    root.mainloop()
