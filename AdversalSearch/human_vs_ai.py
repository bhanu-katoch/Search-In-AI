from grid import TicTacToe
def human_vs_ai():
    g = TicTacToe(3,"X","O")
    state = g.grid
    human = "O"
    ai = "X"

    g.print_board(state)
    while not g.terminate(state):
        if g.pturn == human:
            # human plays
            i,j = map(int,input("Enter row col: ").split())
            if state[i][j]!="0":
                print("Invalid move, try again.")
                continue
            state = g.result(state,(i,j),human)
            g.pturn = ai
        else:
            # AI plays
            move = g.best_move(state,ai)
            state = g.result(state,move,ai)
            print(f"AI plays {move}")
            g.pturn = human
        g.print_board(state)

    # game over
    score = g.utility(state)
    if score==1:
        print("AI (X) wins!")
    elif score==-1:
        print("You (O) win!")
    else:
        print("Draw!")
if __name__=="__main__":
    human_vs_ai()