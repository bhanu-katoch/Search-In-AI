import random
class Grid:
    def __init__(self,n,p1="X",p2="O"):
        self.n = n
        self.grid = [["0" for _ in range(n)] for _ in range(n)]
        self.turns = 0
        if p1==p2:
            raise Exception("Symbols can't be same")
        self.p1 = p1
        self.p2 = p2
        self.pturn = random.choice([p1,p2])

    def get_state(self):
        return self.grid.copy()
    
    def populate(self,filename):
        with open(filename) as f:
            content = f.read()
        content = content.splitlines()
        for i in range(self.n):
            for j in range(self.n):
                self.grid[i][j] = content[i][j]

    def print(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.grid[i][j],end=" ")
            print()

    def result(self,action):
        (i,j),p = action
        self.grid[i][j] = p

    def terminal(self):
        if self.turns==self.n:
            return True
        for i in range(self.n):
            count =1
            for j in range(1,self.n):
                if self.grid[i][j]!=self.grid[i][j-1]:
                    break
                if self.grid[i][j]!="0":
                    count+=1
            if count==self.n:
                return True
        for i in range(self.n):
            count =1
            for j in range(1,self.n):
                if self.grid[j][i]!=self.grid[j-1][i]:
                    break
                if self.grid[j][i]!="0":
                    count+=1
            if count==self.n:
                return True
        count =1
        for i in range(1,self.n):
            if self.grid[i][i]!=self.grid[i-1][i-1]:
                break
            if self.grid[i][i]!="0":
                count+=1
        if count==self.n:
            return True
        count =1
        for i in range(1,self.n):
            if self.grid[i][self.n-i-1]!=self.grid[i-1][self.n-i]:
                break
            if self.grid[i][self.n-1-i]!="0":
                count+=1
        if count==self.n:
            return True
        return False
    def player(self):
        if self.turns==self.n:
            return None
        if self.pturn==self.p1:
            return self.p2 
        else:
            return self.p1
        



