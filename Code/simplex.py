import numpy as np
from read_file import *

NO_ACOTADO = -9999999

class Problem():
    def __init__(self, A, b, c) -> None:
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)

        self.n = len(self.c)
        self.m = len(self.A)

        self.iteration_info = {}
        self.output = ""

    def print(self, text):
        self.output += text + '\n'
        print(text)

    def __repr__(self) -> str:
        A = f'A: \n{self.__repr_matrix(self.A)}'
        b = f'b: \n{self.__repr_list(self.b)}'
        c = f'c: \n{self.__repr_list(self.c)}'
        n = f'Variables: {self.n}'
        m = f'Restrictions: {self.m}'

        return A + '\n\n' + b + '\n\n' + c + '\n\n' + n + '\n\n' + m + '\n\n'

    def __repr_matrix(self, matrix) -> str:
        s = [[str(round(e, 2)) for e in row] for row in matrix.tolist()]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)
    
    def __repr_list(self, array) -> str:
        string = ''
        for i in array:
            string += str(round(i, 2)) + '  '
        return string
    
    def _print_iter(self):
        string = f''
        for key, item in self.iteration_info.items():
            string += f'{key}: {item}  '
        return string
    
    def solve(self, verbose=0):
        if verbose: self.print(' - - - - - - - - - - - - - - F A S E: 1 - - - - - - - - - - - - - - - - - - - - - \n')
        
        i_B, i_N, x_B, z = self.fase_1(verbose)

        if  z == NO_ACOTADO:
            return None
                                   
        if verbose: self.print('\n - - - - - - - - - - - - - - F A S E: 2 - - - - - - - - - - - - - - - - - - - - - \n')
        
        i_B, i_N, x_B, z = self.fase_2(i_B, i_N, x_B, z, verbose)

        return i_B, i_N, x_B, z
    
    def fase_1(self, verbose=0):
        copy_A = self.A.copy()
        copy_c = self.c.copy()

        self.A = np.concatenate((self.A.copy(), np.identity(self.m)), axis=1)
        self.c = np.array([0 for i in range(self.n)] + [1 for i in range(self.m)])
        i_B = [self.n + i for i in range(self.m)]
        i_N = [i for i in range(self.n)]
        x_B = self.b
        z = sum(x_B)

        i_B, i_N, x_B, z = self.fase_2(i_B, i_N, x_B, z, verbose)
        
        if round(z, 10) > 0:
            if verbose: self.print('Problema no factible')
            return i_B, i_N, x_B, NO_ACOTADO
        
        self.A = copy_A
        self.c = copy_c
        z = self.c[i_B].dot(x_B)
        
        return i_B, i_N, x_B, z
    
    def fase_2(self, i_B, i_N, x_B, z, verbose=0, inverse=False):
        if verbose == 2: self.print(self)

        cb = self.c[i_B]
        cn = self.c[i_N]
        An = self.A.take(i_N, axis=1)
        B = self.A.take(i_B, axis=1)
        inv_B = np.linalg.inv(B)

        if verbose == 2: 
            self.print(f'Base inicial: {self.__repr_list(i_B)}')
            self.print(f'Z inicial: {z} \n\n')

        iteration = 1
        while True:
            self.iteration_info['Iteration'] = iteration
            if verbose == 2: print(f' - Iteration {iteration}')

            rn, stop = self.reduced_costs(cn, cb, inv_B, An, verbose)
            if stop: 
                self.print('Optim solution:')
                self.print(f'vb = {self.__repr_list(i_B)}')
                self.print(f'xb = {self.__repr_list(x_B)}')
                self.print(f'z = {z}')
                self.print(f'r = {self.__repr_list(rn)}')
                break

            _q, q = self.input_variable(i_N, rn, verbose)
            db = self.calculate_db(inv_B, q, verbose)

            if all(db >= 0):
                self.print('Problema no acotado')
                break
        
            theta, _p, p = self.theta_and_p(i_B, x_B, db, verbose)

            self.swap(i_B, i_N, _q, _p, verbose)
            B, An, z, cb, cn, x_B = self.actualize_variables(i_N, i_B, x_B, z, theta, db, rn, _q, _p, verbose)
            inv_B = self.actualize_inverse_better(inv_B, db, _p) if inverse \
                    else self.actualize_inverse(B)

            if verbose == 1: self.print(self._print_iter())
            iteration += 1

        return i_B, i_N, x_B, z

    def reduced_costs(self, cn, cb, inv_B, An, verbose=0):
        rn = cn - cb.dot(inv_B).dot(An)
        if verbose == 2: self.print(f"Reduced cost: {self.__repr_list(rn)}")

        if all(rn >= 0):
            if verbose: self.print("\nOptim!!!\n\n")
            return rn, True
        
        return rn, False
    
    def input_variable(self, i_N, rn, verbose=0):
        for _q, x in enumerate(rn):
            if x < 0:
                q = i_N[_q]
                self.iteration_info['q'] = q
                if verbose == 2: self.print(f"q: {_q} Input variable: {q}")
                return _q, q
            
    def calculate_db(self, inv_B, q, verbose=0):
        db = - inv_B.dot(self.A.take(q, axis=1))
        if verbose == 2: self.print(f"Db: {self.__repr_list(db)}")
        return db
    
    def theta_and_p(self, i_B, x_B, db, verbose=0):
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

        self.iteration_info['p'] = p
        self.iteration_info['Theta'] = theta
        if verbose == 2: self.print(f"Theta: {theta} and output variable: {p}")
        return theta, i_p, p

    def swap(self, i_B, i_N, _q, _p, verbose=0):
        into = i_N[_q]
        outof = i_B[_p]
        i_B[_p] = into
        del i_N[_q]

        for i, x in enumerate(i_N):
            if x > outof:
                i_N.insert(i, outof)
                break
            
        if verbose == 2: 
            self.print(f"\nSwap input and output \n i_B: {self.__repr_list(i_B)} \n i_N: {self.__repr_list(i_N)} \n")

    def actualize_variables(self, i_N, i_B, x_B, z,theta, db, rn, q, p, verbose=0):
        x_B = x_B + theta * db
        x_B[p] = theta
        B = self.A.take(i_B, axis=1)
        An = self.A.take(i_N, axis=1)
        cn = self.c[i_N]
        cb = self.c[i_B]

        z += theta * rn[q]

        self.iteration_info['z'] = z
        if verbose== 2: self.print(f'X_B: {self.__repr_list(x_B)} \nZ = {z}\n\n')
        if verbose == 3: self.print(f'B: \n{self.__repr_matrix(B)} \nAn: \n{self.__repr_matrix(An)}\n\n')
        return B, An, z, cb, cn, x_B

    def actualize_inverse(self, B):
        inv_B = np.linalg.inv(B)
        return inv_B
    
    def actualize_inverse_better(self, inv_B, db, p):
        Np = - db / db[p]
        Np[p] = - 1 / db[p]
        E = np.eye(len(inv_B))
        E[:, p] = Np
        new_inv_b = E.dot(inv_B)
        return new_inv_b

A = [[2, 1, 1, 0], [1, 1, 0, 1]]
b = [3, 2]
c = [-1, -2, 0, 0]


input_folder = './Code/Inputs/'
problem_name = '34.3'
filename = input_folder + problem_name + '.inp'

A, b, c = read_file(file=filename)

P = Problem(A, b, c)
P.solve(verbose=1)


output_folder = './Code/Outputs/'
filename = output_folder + problem_name + '.out'

file = open(filename, "w")
file.write(P.output)



