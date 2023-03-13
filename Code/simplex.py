import numpy as np

class Problem():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.B = None
        
    def __repr__(self):
        pass
        
    def solve(self):
        pass
    
    def fase_1(self):
        pass
    
    def fase_2(self):
        r = self.reduced_costs()
        if r > 0:
            return 
        
    def actualize_inverse(self):
        pass
    
    def reduced_costs(self):
        pass