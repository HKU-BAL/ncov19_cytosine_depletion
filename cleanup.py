import sys
import os
import subprocess
import shlex
from utils import replace_by_dict, perm
from params import base_folder

def fasta_qualify(string):
    if len(string) < 20000:
        return False
    if string.count("N") / len(string) > 0.05:
        return False

    return True

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fastas = set()
    infos = set()
    aligned_fastas = set()

    p = subprocess.Popen(shlex.split(f"ls {base_folder}/fasta"), stdout=subprocess.PIPE)

    for line in p.stdout:
        line = line.decode("utf-8").strip().split()
        for item in line:
            if ".fasta" in item:
                fastas.add(item)
            else:
                infos.add(item)

    p.stdout.close()

    p = subprocess.Popen(shlex.split(f"ls {base_folder}/aligned_fasta"), stdout=subprocess.PIPE)

    for line in p.stdout:
        line = line.decode("utf-8").strip().split()
        for item in line:
            if ".masked.fasta" in item:
                aligned_fastas.add(item)

    p.stdout.close()
            
    fasta_list = list(fastas)
    for fasta in fasta_list:
        if (fasta[:-6] + ".info") not in infos:
            fastas.remove(fasta)

    p = open(f"{dir_path}/data/gene", "r")
    gene_dict = {}
    gene_write_string_dict = {}
    for line in p:
        line = line.strip().split()
        gene_dict[line[0]] = (int(line[1]), int(line[2]))
        gene_write_string_dict[line[0]] = []

    p.close()

    if not os.path.exists(f"{base_folder}/processed_fasta/temp"):
        os.makedirs(f"{base_folder}/processed_fasta/temp")

    if not os.path.exists(f"{base_folder}/backup_fasta/temp"):
        os.makedirs(f"{base_folder}/backup_fasta/temp")

    if not os.path.exists(f"{base_folder}/fasta_info"):
        os.mkdir(f"{base_folder}/fasta_info")

    count = 0

    fasta_list = list(fastas)
    for fasta in fasta_list:
        # check if the fasta is a valid fasta
        if (fasta[:-6] + ".masked.fasta") in aligned_fastas:
            # Get fasta string info
            p = subprocess.Popen(shlex.split(f"cat {base_folder}/aligned_fasta/{fasta[:-6]}.masked.fasta"), stdout=subprocess.PIPE)
            string = ""

            for line in p.stdout:
                line = line.decode("utf-8")
                if line[0] == ">":
                    continue
                else:
                    string += line.strip().upper()

            p.stdout.close()

            string = replace_by_dict(string,)

            # Extract fasta info
            info_string = ""
            p = open(f"{base_folder}/fasta/{fasta[:-6]}.info", "r")
            for line in p:
                info_string += line

            '''
                yyyy-mm-dd
                host
                region / country / city ...
            '''

            info_string = info_string.split('\n')
            date = info_string[0].strip().split("-")

            for i in range(3-len(date)):
                date.append("*")

            host = info_string[1].replace(" ", "_")

            location_list = [a.strip().replace(" ", "_") for a in info_string[2].split("/")]
            location = ".".join(location_list)

            p.close()

            # For each gene, count the number of existence of nucleotides in the sequence
            for gene, pos_pair in gene_dict.items():

                gene_seq = string[pos_pair[0]:pos_pair[1]]

                count_list = []
                for i in range(3):
                    count_list.append({})
                    for j in perm(i+1):
                        count_list[i][j] = 0


                for i in range(3):
                    for j in range(len(gene_seq)-i):
                        if gene_seq[j:j+i+1] in count_list[i]:
                            count_list[i][gene_seq[j:j+i+1]] += 1

                write_string = f"{fasta[:-6]}\t{date[0]}\t{date[1]}\t{date[2]}\t{host}\t{location}"

                for i in range(3):
                    for seq in perm(i+1):
                        write_string = f"{write_string}\t{count_list[i][seq]}"

                gene_write_string_dict[gene].append(write_string)

            p = subprocess.Popen(shlex.split(f"mv {base_folder}/fasta/{fasta[:-6]}.fasta {base_folder}/processed_fasta/temp"), stdout=subprocess.PIPE)
            p.communicate()
            p = subprocess.Popen(shlex.split(f"mv {base_folder}/fasta/{fasta[:-6]}.info {base_folder}/processed_fasta/temp"), stdout=subprocess.PIPE)
            p.communicate()

        else:
            p = subprocess.Popen(shlex.split(f"mv {base_folder}/fasta/{fasta[:-6]}.fasta {base_folder}/backup_fasta/temp"), stdout=subprocess.PIPE)
            p.communicate()
            p = subprocess.Popen(shlex.split(f"mv {base_folder}/fasta/{fasta[:-6]}.info {base_folder}/backup_fasta/temp"), stdout=subprocess.PIPE)
            p.communicate()

        count += 1
        if count % 100 == 0:
            print(f"Processed {count} fastas...")

    for gene, write_strings in gene_write_string_dict.items():
        fp = open(f"{base_folder}/fasta_info/{gene}", "a")
        for write_string in write_strings:
            fp.write(write_string+"\n")

if __name__ == "__main__":
    main()