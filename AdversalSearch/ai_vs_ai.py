from grid_minimax import TicTacToe_minimax
from grid_alphaBeta import TicTacToe_alphaBeta
import time

def ai_vs_ai():
    game = TicTacToe_minimax(3,"X","O") # replace code here for aplha beta
    state = game.grid

    print("Initial Board:")
    game.print_board(state)

    time1 = time.time()

    while not game.terminate(state):
        player = game.pturn
        move = game.best_move(state,player)
        if not move:
            break
        i,j = move
        state[i][j] = player
        print(f"Player {player} moves at {move}")
        game.print_board(state)

        # switch player
        game.pturn = game.p1 if player==game.p2 else game.p2
        # time.sleep(1)

    score = game.utility(state)
    if score == 1:
        print("AI X wins!")
    elif score == -1:
        print("AI O wins!")
    else:
        print("Draw!")
    print("Minimax time : ",round(time.time()-time1,2),"s")

if __name__=="__main__":
    ai_vs_ai()