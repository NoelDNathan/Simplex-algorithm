def read_file(file):
    
    # Read the file and remove '\n' and empty lines
    with open(file) as f:
        input = f.readlines()
        input = [i.replace('\n', '') for i in input]
        input = list(filter(lambda a: a != '', input))
        
    # Find in which lines starts each section
    lines = {}
    for line, text in enumerate(input):
        if '=' in text:
            lines[text[:text.find('=')]] = line

    # Separate the input in the various sections
    sections = {}
    prev_key = None
    for key in lines.keys():
        if prev_key is not None:
            start = lines[prev_key] + 1
            end = lines[key]
            sections[prev_key] = input[start:end]
        prev_key = key
    start = lines[prev_key] + 1
    sections[prev_key] = input[start:len(input)]

    # Read each setcion
    A = read_section(sections['A'])
    b = read_section(sections['b'])
    c = read_section(sections['c'])
    z = read_section(sections['z*'])
    vb = read_section(sections['vb*'])
    
    return A, b, c, z, vb


def read_section(section):
    columns_idx = [i for i, s in enumerate(section) if 'Columns' in s]

    if columns_idx:
        columns_idx += [len(section)]
        sections = [section[columns_idx[i]+1:columns_idx[i+1]] for i in range(len(columns_idx) - 1)]
        
        new_section = []
        for i in range(len(sections[0])):
            new_section.append(sections[0][i].split() + sections[1][i].split())
        
        if len(new_section) > 1:
            section = [[float(i) for i in j] for j in new_section]
        else:
            section = [float(i) for i in new_section[0]]
    
    else:   
        section = section[0].split()
        section = [float(i) for i in section]
    
    return section
