# ncov19_cytosine_attenuation

## Installation with conda

 ```
 git clone https://github.com/HKU-BAL/ncov19_cytosine_attenuation.git
 cd ncov19_cytosine_attenuation/
 conda env create -f environment.yml
 conda activate ncov19-ca
 npm install
 ```
 
 [Nextstrain](https://github.com/nextstrain/ncov) is also required, please follow the installation guide in the page.

## Basic Usage

 - Use `crawler.ts` to download fasta from GISAID.
 - Run `align_fasta.py`, `cleanup.py`, `count_byday.py`, `plot.py`, `update_intro.py` and `concat_fasta.py` in order for processing the downloaded fasta.

## Important notes

 - All scripts modify files under the `base_folder`, which is defined and if needed, should be modified in both `params.py` and `crawler.ts`. Default is inside `download_data/` under this directory.
 - The repository of [Nextstrain/ncov](https://github.com/nextstrain/ncov) need to be referenced in `params.py` after the `ncov_folder` variable.
 - `base_folder/fasta/` stores the `.fasta` and `.info` retrieved directly from GISAID.
 - `base_folder/aligned_fasta/` stores the aligned fasta against the reference.
 - `base_folder/processed_fasta/` stores the raw sequence from `fasta` that is qualified (sequence length>29k, N<5%), while `base_folder/backup_fasta/` stores those that is not.
