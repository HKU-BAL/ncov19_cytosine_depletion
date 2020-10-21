import sys
import os
import subprocess
import shlex
from datetime import date
from params import base_folder

today = str(date.today())

def clear_folder(folder):
    
    p = subprocess.Popen(shlex.split(f"ls {base_folder}/{folder}/temp/"), stdout=subprocess.PIPE)
    fwf = open(f"{base_folder}/{folder}/{today}.fasta", "a")
    fwi = open(f"{base_folder}/{folder}/{today}.info", "a")

    for line in p.stdout:
        line = line.decode("utf-8").strip()
        if ".fasta" in line:
            with open(f"{base_folder}/{folder}/temp/{line}", "r") as fr:
                for line in fr:
                    fwf.write(f"{line.strip()}\n")

        else:
            fwi.write(f"{line[:-5]}\n")
            with open(f"{base_folder}/{folder}/temp/{line}", "r") as fr:
                for line in fr:
                    fwi.write(f"{line.strip()}\n")

    print(f"rm {base_folder}/{folder}/temp/*")
    os.system(f"rm {base_folder}/{folder}/temp/*")

def main():
    clear_folder("processed_fasta")
    clear_folder("backup_fasta")
    

if __name__ == "__main__":
    main()