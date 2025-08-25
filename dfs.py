from maze import Maze,StackFrontier
import sys
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve(StackFrontier())
print("DFS States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image(f"{sys.argv[1][:-4]}_dfs.png", show_explored=True)