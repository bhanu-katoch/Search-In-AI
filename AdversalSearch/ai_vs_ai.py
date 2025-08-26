import time
from grid import TicTacToe
def ai_vs_ai():
    game = TicTacToe(3,"X","O")
    state = game.grid

    print("Initial Board:")
    game.print_board(state)

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
        time.sleep(1)

    score = game.utility(state)
    if score == 1:
        print("AI X wins!")
    elif score == -1:
        print("AI O wins!")
    else:
        print("Draw!")

if __name__=="__main__":
    ai_vs_ai()