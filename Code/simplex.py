import numpy as np
from read_file_pero_mucho_mejor import *

class Problem():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        
        self.i_B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.B = A[self.i_B]
        self.inv_B = np.linalg.inv(self.B)
        self.C_B = c[self.i_B]
        self.X_B = None
        
        self.i_N = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        self.C_N = c[self.i_N]
        
    def __repr__(self):
        return f'A = {self.A}\nb = {self.b}\nc={self.c}'
        
    def solve(self):
        pass
    
    def fase_1(self):
        pass
    
    def fase_2(self):
        
        Xb = self.inv_B.dot(b)
        
        r = self.reduced_costs()
        if r > 0:
            return 
        
    def actualize_inverse(self):
        pass
    
    def reduced_costs(self):
        pass

A, b, c, z, vb = read_file(file='./Code/Inputs/34.1.txt')

# A = (2 1 1 0)
#     (1 1 0 1)     n = 4
# b = (3 2)         m = 2
# c = (-1 -2 0 0)
#
# B = {1, 2} --> B = (2 1) --> B^-1 = ( 1 -1) --> C_B = (-1 2) 
#                    (1 1)            (-1  2)
# N = {3, 4} --> X_N = (0 0) --> C_N = (0 0)
# 
# X_B = B^-1 * b 

P = Problem(A, b, c)