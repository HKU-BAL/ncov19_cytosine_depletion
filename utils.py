import os

def perm(length):
    base = "ACGT"
    array = []

    if length > 1:
        for i in range(4):
            for item in perm(length-1):
                array.append(base[i] + item)

    if length == 1:
        for i in range(4):
            array.append(base[i])

    return array

def extract_from_list(seq_list):
    return_dict = {}
    index = 0
    for i in range(3):
        for seq in perm(i+1):
            return_dict[seq] = int(seq_list[index])
            index += 1

    return return_dict

replace_dict = {
    "Y": "C",
    "M": "C",
    "S": "C",
    "B": "C",
    "V": "C",
    "R": "G",
    "K": "G",
    "D": "G",
    "H": "G",
    "W": "A"
}

def replace_by_dict(string):
    for i, j in replace_dict.items():
        string = string.replace(i, j)
    return string

    
def days_in_month(month, year):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month != 2:
        return 30
    elif year%100 == 0:
        return 28
    elif year%4 == 0:
        return 29
    else:
        return 28

def get_gene_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    gene_list = []
    with open(f"{dir_path}/data/gene", "r") as fp:
        for line in fp:
            line = line.strip().split()
            gene_list.append(line[0])

    return gene_list