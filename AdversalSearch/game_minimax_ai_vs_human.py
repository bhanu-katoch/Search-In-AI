from grid_minimax import TicTacToe_minimax
from grid_alphaBeta import TicTacToe_alphaBeta
import tkinter as tk

class TicTacToeGUI:
    def __init__(self, root, n=3):
        self.root = root
        self.n = n
        self.root.title(f"Tic Tac Toe ({self.n}x{self.n}) - Minimax AI")
        self.root.config(bg="#1e1e2f")

        self.game = TicTacToe_minimax(self.n, "X", "O")  # AI = X, Human = O
        self.state = self.game.grid
        self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]

        self.build_grid()

        self.info = tk.Label(
            self.root,
            text="Your turn (O)",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        self.info.grid(row=self.n, column=0, columnspan=self.n, pady=10)

    def build_grid(self):
        for i in range(self.n):
            for j in range(self.n):
                b = tk.Button(
                    self.root,
                    text=" ",
                    width=6,
                    height=3,
                    font=("Arial", 80, "bold"),  # <-- THIS LINE CONTROLS TEXT SIZE
                    bg="#2e2e3e",
                    fg="white",
                    disabledforeground="white",
                    relief="ridge",
                    command=lambda i=i,j=j:self.human_move(i,j)
                )
                b.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons[i][j] = b

        for i in range(self.n):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def human_move(self, i, j):
        if self.state[i][j] != "0" or self.game.terminate(self.state):
            return
        self.state[i][j] = self.game.p2
        self.buttons[i][j].config(text="O", bg="#5e3e3e", state="disabled")
        if self.game.terminate(self.state):
            self.end_game()
            return
        self.root.after(500, self.ai_move)

    def ai_move(self):
        move = self.game.best_move(self.state, self.game.p1)
        if move:
            i, j = move
            self.state[i][j] = self.game.p1
            self.buttons[i][j].config(text="X", bg="#dc1b1b", state="disabled")
        if self.game.terminate(self.state):
            self.end_game()

    def end_game(self):
        score = self.game.utility(self.state)

        # Highlight winning cells
        winner_cells = self.find_winner_cells()
        if winner_cells:
            for (i, j) in winner_cells:
                self.buttons[i][j].config(bg="#4CAF50")  # green highlight

        if score == 1:
            self.info.config(text="🎉 AI (X) wins!", fg="#00ff88")
        elif score == -1:
            self.info.config(text="🎉 You (O) win!", fg="#ff4444")
        else:
            self.info.config(text="🤝 Draw!", fg="orange")

        # disable all buttons
        for i in range(self.n):
            for j in range(self.n):
                self.buttons[i][j].config(state="disabled")

    def find_winner_cells(self):
        """Finds winning line for any n"""
        s = self.state
        n = self.n

        # Rows
        for i in range(n):
            if s[i][0] != "0" and all(s[i][j] == s[i][0] for j in range(n)):
                return [(i, j) for j in range(n)]

        # Columns
        for j in range(n):
            if s[0][j] != "0" and all(s[i][j] == s[0][j] for i in range(n)):
                return [(i, j) for i in range(n)]

        # Main diagonal
        if s[0][0] != "0" and all(s[i][i] == s[0][0] for i in range(n)):
            return [(i, i) for i in range(n)]

        # Anti-diagonal
        if s[0][n-1] != "0" and all(s[i][n-1-i] == s[0][n-1] for i in range(n)):
            return [(i, n-1-i) for i in range(n)]

        return None


if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root, n=3)  # change n for bigger board
    root.mainloop()
