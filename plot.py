import plotly.graph_objects as go
import os
import sys

from utils import perm, extract_from_list, get_gene_list
from params import html_folder, base_folder


# initialize plot lists
mono_list = []
mono_list.append(([[x] for x in perm(1)],"All Mononucleotides" ,"All"))
for seq in perm(1):
    mono_list.append(([[seq]], seq, seq))

di_list = []
withC = []
withoutC = []
di_list.append(([[x] for x in perm(2)], "All Dinucleotides", "All"))
for seq in perm(2):
    if "C" in seq:
        withC.append(seq)
    else:
        withoutC.append(seq)
di_list.append(([withC],"Dinucleotides with C", "with_C"))
di_list.append(([withoutC], "Dinucleotides without C", "without_C"))

tri_list = []
withC = []
withoutC = []
tri_list.append(([[x] for x in perm(3)], "All Trinucleotides", "All"))
for seq in perm(3):
    if "C" in seq:
        withC.append(seq)
    else:
        withoutC.append(seq)
tri_list.append(([withC], "Trinucleotides with C", "with_C"))
tri_list.append(([withoutC], "Trinucleotides without C", "without_C"))


def plot_with_dict(gene, count_dict_list, plot_list, perm_list, name_prefix):

    for trace_list, name, file_name in plot_list:

        fig = go.Figure()
        x = []
        count = []
        count_all_list = []

        for seq in perm_list:
            x.append([])

            count.append([])
            for _ in range(7):
                count[-1].append(0)

        for _ in range(7):
            count_all_list.append(0)

        for count_dict, info in count_dict_list:

            count_all = 0

            for seq in perm_list:
                count_all += count_dict[seq]

            count_all_list.append(count_all)

            for i in range(len(trace_list)):
                seq_list = trace_list[i]
                x[i].append(info)
                count[i].append(0)
                for seq in seq_list:
                    count[i][-1] += count_dict[seq]

        for _ in range(7):
            for i in range(len(trace_list)):
                count[i].append(0)

        y = []

        for i in range(len(trace_list)):
            y.append([])
            for j in range(7, len(count[0])-7):
                if sum(count_all_list[j-7:j+8]) == 0:
                    y[-1].append(0)
                else:
                    y[-1].append(sum(count[i][j-7:j+8])/sum(count_all_list[j-7:j+8]))

        for i in range(len(trace_list)):
            fig.add_trace(go.Scatter(x=x[i], y=y[i], name=perm_list[i]))

        if not os.path.exists(f"{html_folder}/plots/{gene}/{name_prefix}/"):
            os.makedirs(f"{html_folder}/plots/{gene}/{name_prefix}/")

        fig.update_layout(
            title=f"{name}" if gene == "Whole" else f"{name} - {gene} Gene",
            yaxis_title="Percentage",
            xaxis_title="Date",
            title_font_size=20
        )

        fig.write_html(f"{html_folder}/plots/{gene}/{name_prefix}/{file_name}.html")


def plot(gene):
    if not os.path.exists(f"{base_folder}/fasta_info_count/{gene}"):
        return -1
        
    count_dict_list = []

    with open(f"{base_folder}/fasta_info_count/{gene}", "r") as fp:
        for line in fp:
            line = line.strip().split()
            count_dict_list.append((extract_from_list(line[3:]), f"{line[0][-2:]}.{line[1]}.{line[2]}"))

    plot_with_dict(gene, count_dict_list, mono_list, perm(1), "mono")
    plot_with_dict(gene, count_dict_list, di_list, perm(2), "di")
    plot_with_dict(gene, count_dict_list, tri_list, perm(3), "tri")

    

def main():

    if not os.path.exists(f"{html_folder}/plots"):
        os.mkdir(f"{html_folder}/plots")

    gene_list = get_gene_list()

    for gene in gene_list:
        plot(gene)

if __name__ == "__main__":
    main()
