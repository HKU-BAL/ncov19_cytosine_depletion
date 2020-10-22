# ncov19_cytosine_attenuation

## Installation with conda

 ```
 git clone https://github.com/HKU-BAL/ncov19_cytosine_attenuation.git
 cd ncov19_cytosine_attenuation/
 conda env create -f environment.yml
 npm install
 ```
 
 [https://github.com/nextstrain/ncov](Nextstrain) is also required, please follow the installation guide in the github page.

## Basic Usage

 - Use `crawler.ts` to download fasta from GISAID.
 - Run `align_fasta.py`, `cleanup.py`, `count_byday.py`, `plot.py`, `update_intro.py` and `concat_fasta.py` in order for processing the downloaded fasta.

## Important notes

 - All scripts modify files under the `base_folder`, which is defined and if needed, should be modified in both `params.py` and `crawler.ts`. Default is inside `download_data/` of this directory.
 - The repository of [https://github.com/nextstrain/ncov](Nextstrain/ncov) need to be referenced in `params.py` after the `ncov_folder` variable.
 - `fasta/` stores the `.fasta` and `.info` retrieved directly from GISAID.
 - `aligned_fasta/` stores the aligned fasta against the reference.
 - `processed_fasta/` stores the raw sequence from `fasta` that is qualified (sequence length>29k, N<5%), while `backup_fasta/` stores those that is not.
