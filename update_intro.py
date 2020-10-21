import sys
import os
import subprocess
import shlex
from datetime import date
from params import html_folder, base_folder

today = date.today()
p = subprocess.Popen(shlex.split(f"wc -l {base_folder}/fasta_info/Whole"), stdout=subprocess.PIPE)
count, _ = p.communicate()
count = count.decode("utf-8").strip().split()[0]

print(str(today), count)

with open(f"{html_folder}/script.js", "w") as f:
    f.write(f"function getDateAndCount(){{return ['{str(today)}', {count}]}}")


