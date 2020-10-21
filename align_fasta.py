import sys
import os
import subprocess
import shlex
from multiprocessing import Pool
from params import base_folder, ref_file, thread, ncov_folder

def align_fasta(fasta):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    p = subprocess.Popen(shlex.split(f"sh {dir_path}/scripts/align.sh {base_folder}/fasta/{fasta} {base_folder}/aligned_fasta/{fasta} {base_folder}/aligned_fasta/{fasta[:-6]+'.masked.fasta'} {ref_file} {ncov_folder}"), stdout=subprocess.PIPE)
    p.communicate()

def replace_by_dict(string, dic):
    for i, j in dic.items():
        string = string.replace(i, j)
    return string

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

def fasta_qualify(string):
    if len(string) < 29000:
        return False
    if string.count("N") / len(string) > 0.05:
        return False

    return True

fastas = set()
infos = set()

p = subprocess.Popen(shlex.split(f"ls {base_folder}/fasta"), stdout=subprocess.PIPE)

for line in p.stdout:
    line = line.decode("utf-8").strip().split()
    for item in line:
        if ".fasta" in item:
            fastas.add(item)
        else:
            infos.add(item)

p.stdout.close()

fasta_list = list(fastas)
for fasta in fasta_list:
    if (fasta[:-6] + ".info") not in infos:
        fastas.remove(fasta)

if not os.path.exists(f"{base_folder}/aligned_fasta"):
    os.mkdir(f"{base_folder}/aligned_fasta")

fasta_list = list(fastas)
fasta_pool = []
for fasta in fasta_list:
    p = open(f"{base_folder}/fasta/{fasta}", "r")
    string = ""

    for line in p:
        if line[0] == ">":
            continue
        else:
            string += line.strip().upper()

    p.close()

    if fasta_qualify(string):
        fasta_pool.append(fasta)
        
with Pool(thread) as p:
    p.map(align_fasta, fasta_pool)
