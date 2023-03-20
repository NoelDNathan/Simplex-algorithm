import numpy as np
from read_file_pero_mucho_mejor import *


class Problem():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c 
        
        self.m = len(self.A)
        self.n = len(self.c)
        
    def __repr__(self):
        print(f'A = \n{self.__print_matrix__(self.A)}')
        print(f'b = {self.b}')
        print(f'c = {self.c}')
        return ''
        
    def __print_matrix__(self, matrix):
        s = [[str(e) for e in row] for row in matrix.tolist()]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)
    
    def solve(self):
        print("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! FASE 1 ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! \n")
        i_B, i_N, x_B, z = self.fase_1()
        print("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! FASE 2 ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! \n")
        i_B, i_N, x_B, z = self.fase_2(i_B, i_N, x_B, z)
        return i_B, i_N, x_B, z
    
    def fase_1(self):
        # Si z = 0 y quedan variables artificiales
        # La cambiamos por una variable de la base
        # como son dos 0, no hay problema
        # Una solución es basica si una B es invertible (no es condición suficiente)
        
        copy_A = self.A.copy()
        copy_c = self.c.copy()
        
        new_c = np.array([0 for i in range(self.n)] + [1 for i in range(self.m)])
        self.c = new_c
        
        I = np.identity(self.m)
        new_A = np.concatenate((self.A.copy(), I), axis=1)
        self.A = new_A
        
        i_B = [self.n + i for i in range(self.m)]
        i_N = [i for i in range(self.n)]
        x_B = self.b
        z = sum(x_B)
        
        i_B, i_N, x_B, z = self.fase_2(i_B, i_N, x_B, z) 
    
        self.A = copy_A
        self.c = copy_c
        
        return i_B, i_N, x_B, z
    
    def fase_2(self, i_B, i_N, x_B, z):
        # No puede haber z < 0
        # No puede haber variables negativas
        # z = 0, hay degeneración -> implementar la regla de Bland
        # Ojo no acotación
    
        print(self)
        cb = self.c[i_B]
        cn = self.c[i_N]
        An = self.A.take(i_N, axis=1)
        B = self.A.take(i_B, axis=1)
        inv_B = np.linalg.inv(B)

        iteration = 1
        while True:
            print(f'-------------- Iteration: {iteration} --------------\n')
            
            rn, stop = self.reduced_costs(cn, cb, inv_B, An)

            if stop:
                break

            _q, q = self.calculate_input_variable(i_N, rn)
            db = self.calculate_db(inv_B, q)

            if all(db >= 0):
                print("Problema no acotado")
                break

            theta, _p, p = self.calculate_theta_and_p(i_B, x_B, db)

            self.swap_Victor(i_B, i_N, _q, _p)
            B, An, z, cb, cn =  self.actualize_variables(i_N, i_B, x_B, z, theta, db, rn, _q, _p)
            ninv_B = self.actualize_inverse2(inv_B, db, _p)
            inv_B = self.actualize_inverse(B)
            print(f"inversa: \n {self.__print_matrix__(inv_B)} \n new inv:\n {self.__print_matrix__(ninv_B)}")
            
            print(f'-------------- Iteration: {iteration} --------------\n')
            iteration += 1
            
        return i_B, i_N, x_B, z
    
    def reduced_costs(self, cn, cb, inv_B, An):
        rn = cn - cb.dot(inv_B).dot(An)
        print(f"Reduced cost: {rn}")
        if all(rn >= 0):
            print("\nOptim!!!")
            return rn, True
        return rn, False
    
    def calculate_input_variable(self, i_N, rn):
        for _q, x in enumerate(rn):
            if x < 0:
                q = i_N[_q]
                print(f"Input variable: {q}")
                return _q, q

    def calculate_db(self, inv_B, q):
        db = - inv_B.dot(self.A.take(q, axis=1))
        print(f"Db: {db}")
        return db
        
    def calculate_theta_and_p(self, i_B, x_B, db):
        theta = np.inf
        p = np.inf
        i_p = np.inf
        
        for i, x in enumerate(db):
            if x < 0:
                new_theta = - x_B[i]/x
                new_p = i_B[i]

                if new_theta < theta:
                    theta = new_theta
                    p = i_B[i]
                    i_p = i

                if new_theta == theta:
                    if new_p < p:
                        p = new_p
                        i_p = i

        print(f"Theta: {theta} and output variable: {p}")
        return theta, i_p, p
    
    def swap_Victor(self, i_B, i_N, _q, _p):
        into = i_N[_q]
        outof = i_B[_p]
        i_B[_p] = into
        del i_N[_q]

        for i, x in enumerate(i_N):
            if x > outof:
                i_N.insert(i, outof)
                break
            
        print(f"\nSwap input and output \n i_B: {i_B} \n i_N: {i_N} \n")

    def actualize_variables(self, i_N, i_B, x_B, z,theta, db, rn, q, p):
        x_B = x_B + theta * db
        x_B[p] = theta
        B = self.A.take(i_B, axis=1)
        An = self.A.take(i_N, axis=1)
        cn = self.c[i_N]
        cb = self.c[i_B]

        z += theta * rn[q]

        print(f"Actualize variables. \n XB: {x_B} \n B: {self.__print_matrix__(B)} \n An: {self.__print_matrix__(An)} \n z: {z} \n")
        return B, An, z, cb, cn

    def actualize_inverse(self, B):
        inv_B = np.linalg.inv(B)
        return inv_B
    
    def actualize_inverse2(self, inv_B, db, p):
        Np = - db / db[p]
        Np[p] = - 1 / db[p]
        E = np.eye(len(inv_B))
        E[:, p] = Np
        new_inv_b = E.dot(inv_B)
        return new_inv_b


A = np.array([[2, 1, 1, 0], [1, 1, 0, 1]])
b = np.array([3, 2])
c = np.array([-1, -2, 0, 0])

# A, b, c, z, vb = read_file(file='./Code/Inputs/34.1.txt')
# A = np.array(A)
# b = np.array(b)
# c = np.array(c)

P = Problem(A, b, c).solve()
# P = Problem(A, b, c).fase_2(i_B, i_N, x_B, z)
