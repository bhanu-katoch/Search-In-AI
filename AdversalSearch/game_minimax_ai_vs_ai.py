from grid_minimax import TicTacToe_minimax
from grid_alphaBeta import TicTacToe_alphaBeta
import tkinter as tk

class TicTacToeAIvsAI:
    def __init__(self, root, n=3):
        self.root = root
        self.n = n
        self.root.title(f"🤖 AI vs AI Tic Tac Toe ({self.n}x{self.n}) 🤖")
        self.root.config(bg="#1e1e2f")  # dark background

        self.game = TicTacToe_alphaBeta(self.n, "X", "O")
        self.state = self.game.grid
        self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]

        self.build_grid()

        self.info = tk.Label(
            self.root,
            text="AI vs AI running...",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        self.info.grid(row=self.n, column=0, columnspan=self.n, pady=10)

        # start loop after 1 second
        self.root.after(1000, self.play_turn)

    def build_grid(self):
        for i in range(self.n):
            for j in range(self.n):
                b = tk.Button(
                    self.root,
                    text=" ",
                    width=6,
                    height=3,
                    font=("Arial", 20, "bold"),
                    bg="#2e2e3e",
                    fg="white",
                    disabledforeground="white",
                    relief="ridge",
                    state="disabled"
                )
                b.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons[i][j] = b

        for i in range(self.n):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def play_turn(self):
        if self.game.terminal(self.state):
            self.end_game()
            return

        current = self.game.pturn
        move = self.game.best_move(self.state, current)

        if move:
            i, j = move
            self.state[i][j] = current
            self.buttons[i][j].config(
                text=current,
                bg="#3e3e5e" if current == "X" else "#5e3e3e"
            )

        # switch player
        self.game.pturn = self.game.p1 if current == self.game.p2 else self.game.p2

        if not self.game.terminal(self.state):
            self.root.after(800, self.play_turn)  # smoother (0.8s)
        else:
            self.end_game()

    def end_game(self):
        score = self.game.utility(self.state)

        # Highlight winning cells
        winner_cells = self.find_winner_cells()
        if winner_cells:
            for (i, j) in winner_cells:
                self.buttons[i][j].config(bg="#4CAF50")  # green highlight

        if score == 1:
            self.info.config(text="🎉 AI X wins!", fg="#00ff88")
        elif score == -1:
            self.info.config(text="🎉 AI O wins!", fg="#ff4444")
        else:
            self.info.config(text="🤝 It's a Draw!", fg="orange")

    def find_winner_cells(self):
        """Finds winning line for any n"""
        s = self.state
        n = self.n

        # Rows
        for i in range(n):
            if s[i][0] != "0" and all(s[i][j] == s[i][0] for j in range(n)):
                return [(i, j) for j in range(n)]

        # Cols
        for j in range(n):
            if s[0][j] != "0" and all(s[i][j] == s[0][j] for i in range(n)):
                return [(i, j) for i in range(n)]

        # Main diagonal
        if s[0][0] != "0" and all(s[i][i] == s[0][0] for i in range(n)):
            return [(i, i) for i in range(n)]

        # Anti diagonal
        if s[0][n - 1] != "0" and all(s[i][n - 1 - i] == s[0][n - 1] for i in range(n)):
            return [(i, n - 1 - i) for i in range(n)]

        return None


if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeAIvsAI(root, n=3)  # change n here (e.g., 4, 5, ...)
    root.mainloop()
