import sys
import os
import subprocess
import shlex
from datetime import date
from params import base_folder

today = str(date.today())

def clean_folder(folder):
    
    p = subprocess.Popen(shlex.split(f"ls {base_folder}/{folder}/temp/"), stdout=subprocess.PIPE)
    fwf = open(f"{base_folder}/{folder}/{today}.fasta", "a")
    fwi = open(f"{base_folder}/{folder}/{today}.info", "a")

    for line in p.stdout:
        line = line.decode("utf-8").strip()
        file_name = f"{base_folder}/{folder}/temp/{line}"
        if ".fasta" in line:
            with open(f"{base_folder}/{folder}/temp/{line}", "r") as fr:
                for line in fr:
                    fwf.write(f"{line.strip()}\n")

        else:
            fwi.write(f"{line[:-5]}\n")
            with open(f"{base_folder}/{folder}/temp/{line}", "r") as fr:
                for line in fr:
                    fwi.write(f"{line.strip()}\n")

        os.remove(file_name)

def clear_folder(folder):

    p = subprocess.Popen(shlex.split(f"ls {base_folder}/{folder}/"), stdout=subprocess.PIPE)

    for line in p.stdout:
        line = line.decode("utf-8").strip()
        file_name = f"{base_folder}/{folder}/{line}"
        os.remove(file_name)

def main():
    clean_folder("processed_fasta")
    clean_folder("backup_fasta")
    clear_folder("aligned_fasta")

if __name__ == "__main__":
    main()