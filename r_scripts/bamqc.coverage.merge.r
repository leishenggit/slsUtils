library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='merge qualimap bamqc genome_fraction_coverage.txt files')

parser$add_argument('fs', metavar='file', nargs='+', help='genome_fraction_coverage.txt files')
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)

lst = lapply(args$fs, read_tsv)
names(lst) <- args$fs

raw_data = bind_rows(lst, .id = "Sample")

write_tsv(raw_data, args$out)

