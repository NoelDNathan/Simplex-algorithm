# Leer los datos del archivo de texto

import numpy as np

file = '34.1.txt'
with open(file, 'r') as f:
    input = f.readlines()

# Input
"""
c=

 Columns 1 to 18

    8   -5    6   77  -77   96  -74  -37   91 -100  -10  -59   28   85    0    0    0    0 

 Columns 19 to 20

    0    0 

A=

 Columns 1 to 18

  -67   13  -26   24  -32   36  -36   46   11   77  -64  -86   90   42    0    0    0    0 
  -42  -70   30  -74   59   35  -13    6   86  -54   12   91   68   82    0    0    0    0 
   97   80  -70   45   45  -34   22   55  -39  -20   70   31   58  -27    0    0    0    0 
  -45  -33  -35   44   34    6  100  -65   30   56   38  -25   -5  -46    0    0    0    0 
   59   60   92   58   83   75   74   87   70   59   63   97   52   85    1    0    0    0 
  -40   89   -9   79   32    3   44  -36   25  -86   30  -33   24  -84    0    1    0    0 
   82  -24 -100   30  -74    1   95  -57  -49   55  -89   90   45   50    0    0   -1    0 
   92   97  -44   35   35   48   77  -17   -9   74   16   70  -59   29    0    0    0    1 
   70   22    2   69    4   92  -74  -83   56  -69   88   69   32   69    0    0    0    0 
  -42   30   98   94    8  -46   70  -50  -14  -38   30   51   86   25    0    0    0    0 

 Columns 19 to 20

    0    0 
    0    0 
    0    0 
    0    0 
    0    0 
    0    0 
    0    0 
    0    0 
    1    0 
    0    1 

b=
   28  216  313   54 1015   39   54  445  348  303 

z*=
 -787.4866 

vb*=
  8 19  1 10 12  3  7  5 16 20 
"""

# Where the word columns appear, replace this line with a blank line
size_matrix = {}
text = ""
element = ""
for line in input:
    if "=" in line:

        pos = line.find("=") - 1
    
        element = line[pos]


    if 'Columns' in line:
        size = line.split()[3]
        size_matrix[element] = int(size)
        continue
    
    text += line

print(size_matrix)
text = text.replace('\n', ' ')

section_c = []
section_a = []
section_b = []

i = 0
n = len(text)
counter = 0
aux = []
selected_matrix = []
new_number = True
isA = False

while i < n:
    current = text[i]
    if current == '=':
        selected_matrix = selected_matrix[:-1]
        counter = 0
        limit = size_matrix.get(text[i - 1])

        previous = text[i - 1]
        isA = False
        if previous == 'c':
            selected_matrix = section_c
        elif previous == 'A':
            selected_matrix = section_a
            isA = True
        elif previous == 'b':
            selected_matrix = section_b
       
        

    i += 1
    if not current.isdigit(): 
        new_number = True
        continue

    if not new_number:
        continue

    counter += 1
    if not isA:
        selected_matrix.append(int(current))
    else:
        aux.append(int(current))
        if counter == limit - 1:
            selected_matrix.append(aux)
            aux = []
            counter = 0





# Print the read sections
print('Section c:', section_c)
print('Section A:', section_a)
print('Section b:', section_b)






 
