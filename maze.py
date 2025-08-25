from collections import deque
from PIL import Image, ImageDraw, ImageFont
import heapq

class Node():
    def __init__(self, state, parent, action,heu=None,cost=1):
        self.state = state
        self.parent = parent
        self.action = action
        self.heu = heu
        self.cost =cost
    def __lt__(self, other):
        """ for heap """
        return self.heu < other.heu   # compare by heuristic
    
class StackFrontier:
    def __init__(self):
        self.frontier = []
    def add(self,node):
        self.frontier.append(node)
    def empty(self):
        return len(self.frontier)==0
    def remove(self):
        if self.empty():
            raise Exception("frontier is empty")
        node = self.frontier.pop()
        return node
    def contains_state(self,state):
        return any(node.state==state for node in self.frontier)
class QueueFrontier:
    def __init__(self):
        self.frontier = deque([])
    def add(self,node):
        self.frontier.append(node)
    def empty(self):
        return len(self.frontier)==0
    def remove(self):
        if self.empty():
            raise Exception("frontier is empty")
        node = self.frontier.popleft()
        return node
    def contains_state(self,state):
        return any(node.state==state for node in self.frontier)
class HeapFrontier:
    def __init__(self):
        self.frontier = []
    def add(self,node):
        heapq.heappush(self.frontier,node)
    def empty(self):
        return len(self.frontier)==0
    def remove(self):
        if self.empty():
            raise Exception("frontier is empty")
        return heapq.heappop(self.frontier)
    def contains_state(self,state):
        return any(node.state==state for node in self.frontier)
    
class Maze:
    def __init__(self,filename):
        with open(filename) as f:
            contents = f.read()
    
        if contents.count("A")!=1:
            raise Exception("Must contain start!")
        if contents.count("B")!=1:
            raise Exception("Must contain goal!")
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max( len(line) for line in contents)

        self.walls =[]
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j]=="A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j]=="B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j]==" ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.heuristic = {}
        for i in range(self.height):
            for j in range(self.width):
                if not self.walls[i][j]:
                    self.heuristic[(i,j)]=(abs(i-self.goal[0])+abs(j-self.goal[1]))
        self.solution = None
    
    def get_heuristic(self,state):
        r,c = state
        if not self.walls[r][c]:
            return self.heuristic[(r,c)]
        
    def neighbors(self, state):
        row,col = state
        result=[]
        moves = (
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))
        )
        for action,(r,c) in moves:
            if 0<=r<self.height and 0<=c<self.width and not self.walls[r][c]:
                result.append((action,(r,c)))
        return result
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def solve(self,frontier,is_heuristic = False, is_cost = False):
        self.explored = set()
        self.num_explored = 0
        if is_heuristic:
            start = Node(self.start,None,None,self.get_heuristic(self.start))
        else:
            start = Node(self.start,None,None)
        self.frontier =frontier
        self.frontier.add(start)
        while True:
            if self.frontier.empty():
                raise Exception("No Solution")
            node = self.frontier.remove()
            self.num_explored+=1

            if node.state == self.goal:
                actions =[]
                cells =[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            
            self.explored.add(node.state)
            for action,state in self.neighbors(node.state):
                if not self.frontier.contains_state(start) and state not in self.explored:
                    if is_heuristic and is_cost:
                        self.heuristic[state] += node.cost 
                        child = Node(state,node,action,self.get_heuristic(state),node.cost+1)
                    elif is_heuristic:
                        child = Node(state,node,action,self.get_heuristic(state))
                    else:
                        child = Node(state,node,action)
                    self.frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False,show_heuristic = False):
        cell_size = 50
        cell_border = 2

       # Extra space at bottom for text
        extra_height = 50

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size + extra_height),
            "black"
        )
        draw = ImageDraw.Draw(img)
        font_path = "/Library/Fonts/Arial.ttf"  # Mac example, adjust for Windows/Linux
        font = ImageFont.truetype(font_path, 20)  # bigger font size


        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

                 # Example: write variable value in cell
                if show_heuristic:
                    if (i,j) == self.goal:
                        h = "B"
                    elif (i,j) == self.start:
                        h = "A"
                    else:
                        h = self.get_heuristic((i,j))
                    variable_value = f"{h}"  # you can replace this with any variable
                    text_x = j * cell_size + cell_size // 4
                    text_y = i * cell_size + cell_size // 4
                    draw.text((text_x, text_y), variable_value, fill="black", font=font)

        # Draw separate text below the maze
        text_x = 10
        text_y = self.height * cell_size + 10  # slightly below maze
        draw.text((text_x, text_y), f"path : {len(solution)}", fill="white", font=font)
        draw.text((text_x+100, text_y), f"explored : {self.num_explored}", fill="white", font=font)

        img.save(filename)



            
        