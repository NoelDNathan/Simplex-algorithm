from simplex import Simplex
from read_file import read_file


input_folder = './Inputs/'
problem_name = '34.4'
ext = '.inp'
filename = input_folder + problem_name + ext

A, b, c = read_file(file=filename)

P = Simplex(A, b, c)
P.solve(verbose=1)


output_folder = './Outputs/'
filename = output_folder + problem_name + '.out'

file = open(filename, "w")
file.write(P.output)
