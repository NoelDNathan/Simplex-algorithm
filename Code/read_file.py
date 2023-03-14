import numpy as np


def read_file(file, verbose=0):
    with open(file, 'r') as f:
        input = f.readlines()

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

    if verbose: print(size_matrix)
    
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

    if verbose:
        print('Section A:', section_a)
        print('Section b:', section_b)
        print('Section c:', section_c)
        
    return section_a, section_b, section_c