from grid import Grid
class Agent:
    def __init__(self,p):
        self.p = p
        self.model = []
    def percieve(self,env):
        self.model = env.get_state()
        