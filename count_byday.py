import os
import sys
import subprocess
import shlex
from utils import perm, extract_from_list, days_in_month
from params import base_folder
from math import ceil

def count_and_output(info_path, output_path):
    f = open(info_path, "r")
    day_count = {}

    f2 = open(output_path, "w")
    
    for line in f:
        line = line.strip().split()
        #ID year month date host location a c g t aa ac ag	at ca ... aaa aac aag ...
        if len(line[6:]) < 84:
            #print(line)
            continue
        ID, YEAR, MONTH, DATE, HOST, LOCATION = line[:6]
        count_dict = extract_from_list(line[6:])

        if HOST != "Human":
            continue

        if DATE == "*" or MONTH == "*":
            continue

        if DATE == "XX":
            continue

        YEAR = int(YEAR)
        MONTH = int(MONTH)
        DATE = int(DATE)

        if YEAR < 2019:
            continue
        
        if YEAR not in day_count:
            day_count[YEAR] = {}

        if MONTH not in day_count[YEAR]:
            day_count[YEAR][MONTH] = {}

        '''
        if PART not in day_count[YEAR][MONTH]:
            day_count[YEAR][MONTH][PART] = {}
            for i in range(1,4):
                for seq in perm(i):
                    day_count[YEAR][MONTH][PART][seq] = 0
        '''

        if DATE not in day_count[YEAR][MONTH]:
            day_count[YEAR][MONTH][DATE] = {}
            for i in range(1,4):
                for seq in perm(i):
                    day_count[YEAR][MONTH][DATE][seq] = 0

        for i in range(1,4):
            for seq in perm(i):
                day_count[YEAR][MONTH][DATE][seq] += count_dict[seq]

    first_year = sorted(day_count.keys())[0]
    last_year = sorted(day_count.keys())[-1]
    first_month = sorted(day_count[first_year].keys())[0]
    last_month = sorted(day_count[last_year].keys())[-1]
    first_day = sorted(day_count[first_year][first_month].keys())[0]
    last_day = sorted(day_count[last_year][last_month].keys())[-1]

    for YEAR in sorted(day_count.keys()):
        for MONTH in sorted(day_count[YEAR].keys()):
            for DATE in range(1, days_in_month(MONTH, YEAR)+1):
                if YEAR == first_year and MONTH == first_month and DATE < first_day:
                    continue
                if YEAR == last_year and MONTH == last_month and DATE > last_day:
                    continue
                string = ""
                if DATE in day_count[YEAR][MONTH].keys():
                    for i in range(1,4):
                        for seq in perm(i):
                            string += str(day_count[YEAR][MONTH][DATE][seq]) + "\t"
                else:
                    for i in range(1,4):
                        for seq in perm(i):
                            string += "0" + "\t"

                f2.write(f"{YEAR}\t{MONTH}\t{DATE}\t{string}\n")

    f.close()
    f2.close()

def main():

    if not os.path.exists(f"{base_folder}/fasta_info_count"):
        os.mkdir(f"{base_folder}/fasta_info_count")

    p = subprocess.Popen(shlex.split(f"ls {base_folder}/fasta_info"), stdout=subprocess.PIPE)
    for line in p.stdout:
        line = line.decode("utf-8").strip().split()
        for gene in line:
            info_path = f"{base_folder}/fasta_info/{gene}"
            output_path = f"{base_folder}/fasta_info_count/{gene}"
            count_and_output(info_path, output_path)

        
if __name__ == "__main__":
    main()
