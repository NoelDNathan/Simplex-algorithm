import numpy as np
from read_file_pero_mucho_mejor import *

A, b, c, z, vb = read_file(file='./Code/Inputs/34.1.txt')
print(len(A), len(A[0]), len(b), len(c))

A = np.asmatrix(A)
b = np.asarray(b)
c = np.asarray(c)

B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
N = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

def simplex():
    
    # costes reducidos
    # r = Cn - Cb * B ^ - 1 * 
    
    pass


def get_non_basis_variables(vb):
    non_basis_variables = []
    for i in range(1, len(vb) + 1):
        if i not in vb:
            non_basis_variables.append(i)
    return non_basis_variables


def calculate_reduced_costs(Cn, Cb, B):
    B_inv = np.linalg.inv(B)
    r = Cn - Cb.dot(B_inv)
    return r