#!/bin/sh
set -e
NCOV_FOLDER=$5

#echo "augur align --sequences $1 --reference-sequence ref/wuhan-hu-1.fasta --fill-gaps --output $2 --remove-reference"
augur align --sequences $1 --reference-sequence $4 --fill-gaps --output $2 --remove-reference
python ${NCOV_FOLDER}/scripts/mask-alignment.py --alignment $2 --mask-from-beginning 130 --mask-from-end 15 --mask-sites 18529 --output $3
