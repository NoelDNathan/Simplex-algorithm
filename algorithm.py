import pandas as pd
import numpy as np

c = [8, -5, 6, 77, -77, 96, -74, -37, 91, -100, -10, -59, 28, 85, 0, 0, 0, 0]
c = np.array(c)
c.where(0)
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