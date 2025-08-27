import random
import copy

class TicTacToe_alphaBeta:
    def __init__(self,n,p1="X",p2="O"):
        self.n = n
        self.grid = [["0" for _ in range(n)] for _ in range(n)]
        if p1==p2:
            raise Exception("Symbols can't be same")
        self.p1 = p1 # max
        self.p2 = p2 # min
        self.pturn = random.choice([p1,p2])   # who starts
        self.wining_pos = []
        d1, d2 = [], []
        for i in range(n):
            row, col = [], []
            for j in range(n):
                row.append((i,j))
                col.append((j,i))
            d1.append((i,i))
            d2.append((i,n-1-i))
            self.wining_pos.append(row)
            self.wining_pos.append(col)
        self.wining_pos.append(d1)
        self.wining_pos.append(d2)

    def print_board(self, state=None):
        if state is None:
            state = self.grid

        # Colors
        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"

        print("\n" + "=" * (self.n * 4 - 1))
        for i in range(self.n):
            row = []
            for j in range(self.n):
                cell = state[i][j]
                if cell == self.p1:
                    row.append(RED + cell + RESET)
                elif cell == self.p2:
                    row.append(BLUE + cell + RESET)
                else:
                    row.append(" ")
            print(" | ".join(row))
            if i < self.n - 1:
                print("-" * (self.n * 4 - 1))
        print("=" * (self.n * 4 - 1) + "\n")

    def calculate_state(self,state):
        pos_p1, pos_p2, turns = [], [], 0
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j]==self.p1:
                    pos_p1.append((i,j))
                    turns+=1
                elif state[i][j]==self.p2:
                    pos_p2.append((i,j))
                    turns+=1
        return pos_p1,pos_p2,turns
    
    def terminal(self,state):
        pos_p1,pos_p2,turns = self.calculate_state(state)
        for pos in self.wining_pos:
            if all(elem in pos_p1 for elem in pos):
                return True
            if all(elem in pos_p2 for elem in pos):
                return True
        if turns == self.n*self.n:
            return True
        return False
    
    def utility(self,state):
        pos_p1,pos_p2,_ = self.calculate_state(state)
        for pos in self.wining_pos:
            if all(elem in pos_p1 for elem in pos):
                return 1   # p1 (max) wins
            if all(elem in pos_p2 for elem in pos):
                return -1  # p2 (min) wins
        return 0  # draw
    
    def actions(self,state):
        return [(i,j) for i in range(self.n) for j in range(self.n) if state[i][j]=="0"]

    def result(self,state,action,player):
        i,j = action
        new_state = copy.deepcopy(state)
        new_state[i][j] = player
        return new_state

    # ---- alpha-beta pruning ----
    def max_value(self, state, alpha=float('-inf'), beta=float('inf')):
        if self.terminal(state):
            return self.utility(state)
        v = float('-inf')
        for action in self.actions(state):
            v = max(v, self.min_value(self.result(state, action, self.p1), alpha, beta))
            if v >= beta:  # Beta cut-off
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha=float('-inf'), beta=float('inf')):
        if self.terminal(state):
            return self.utility(state)
        v = float('inf')
        for action in self.actions(state):
            v = min(v, self.max_value(self.result(state, action, self.p2), alpha, beta))
            if v <= alpha:  # Alpha cut-off
                return v
            beta = min(beta, v)
        return v

    def best_move(self, state, player):
        if player == self.p1:  # maximizing
            best_val = float('-inf')
            move = None
            alpha = float('-inf')
            beta = float('inf')
            for action in self.actions(state):
                val = self.min_value(self.result(state, action, player), alpha, beta)
                if val > best_val:
                    best_val = val
                    move = action
                alpha = max(alpha, best_val)
            return move
        else:  # minimizing
            best_val = float('inf')
            move = None
            alpha = float('-inf')
            beta = float('inf')
            for action in self.actions(state):
                val = self.max_value(self.result(state, action, player), alpha, beta)
                if val < best_val:
                    best_val = val
                    move = action
                beta = min(beta, best_val)
            return move
