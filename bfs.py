from maze import Maze,QueueFrontier
import sys
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve(QueueFrontier())
print("BFS States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image(f"{sys.argv[1][:-4]}_bfs.png", show_explored=True)