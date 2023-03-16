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
        print(f'A = {self.A}')
        print(f'b = {self.b}')
        print(f'c = {self.c}')
        return ''
        
    def solve(self):
        pass
    
    def fase_1(self):
        # Si z = 0 y quedan variables artificiales
        # La cambiamos por una variable de la base
        # como son dos 0, no hay problema
        # Una solución es basica si una B es invertible (no es condición suficiente)
        
        new_C = np.asarray([0 for i in range(self.n)] + [1 for i in range(self.m)])
        
        I = np.identity(self.m)
        new_A = np.concatenate((self.A.copy(), I), axis=1)
        
        i_B = [self.n + i for i in range(self.m)]
        i_N = [i for i in range(self.n)]
        X_B = self.b
        z = sum(X_B)
    
    def fase_2(self, i_B, i_N, X_B, z):
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

            theta, _p, p = self.calculate_theta_and_p(i_B, X_B, db)

            self.swap_Victor(i_B, i_N, _q, _p)
            B, An, z, cb, cn =  self.actualize_variables(i_N, i_B, X_B, z, theta, db, rn, _q, _p)
            ninv_B = self.actualize_inverse2(inv_B, db, _p)
            inv_B = self.actualize_inverse(B)
            print(f"inversa: \n {inv_B} \n new inv:\n {ninv_B}")
            
            print(f'-------------- Iteration: {iteration} --------------\n')
            iteration += 1
    
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
        
    def calculate_theta_and_p(self, i_B, X_B, db):
        theta = np.inf
        p = np.inf
        i_p = np.inf
        
        for i, x in enumerate(db):
            if x < 0:
                new_theta = - X_B[i]/x
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
    
    def swap(self,i_B, i_N, _q, _p):
        i_N[_q], i_B[_p] = i_B[_p], i_N[_q]
        i_N.sort()
        print(f"Indexs. \n i_B: {i_B} \n i_N: {i_N} \n")
        
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

    def actualize_variables(self, i_N, i_B, X_B, z,theta, db, rn, q, p):
        X_B = X_B + theta * db
        X_B[p] = theta
        B = self.A.take(i_B, axis=1)
        An = self.A.take(i_N, axis=1)
        cn = self.c[i_N]
        cb = self.c[i_B]

        z += theta * rn[q]

        print(f"Actualize variables. \n XB: {X_B} \n B: {B} \n An: {An} \n z: {z} \n")
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

i_B = [0, 1]
i_N = [2, 3]

B = A.take(i_B, axis=1)

inv_B = np.linalg.inv(B)

X_B = inv_B.dot(b)

z = -3

P = Problem(A, b, c).fase_1()
# P = Problem(A, b, c).fase_2(i_B, i_N, X_B, z)
