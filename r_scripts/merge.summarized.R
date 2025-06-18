library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='merge summarized taxid_reads file(s)')

parser$add_argument('fs', metavar='file', nargs='+', help='summarized taxid_reads files')
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)

lst = lapply(args$fs, read_tsv, col_names = F)
names(lst) <- args$fs

raw_data = bind_rows(lst, .id = "sample")
names(raw_data) <- c('sample','taxid','reads')

df = raw_data %>%
		mutate(sample = str_replace(sample, '[.].*','')) %>%
		spread(sample, reads, fill = 0)

write_tsv(df, args$out)
