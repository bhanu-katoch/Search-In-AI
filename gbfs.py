from maze import Maze,HeapFrontier
import sys
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve(HeapFrontier(),True)
print("DFS States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image(f"output/{sys.argv[1][:-4]}_gbfs.png", show_explored=True,show_heuristic=True)