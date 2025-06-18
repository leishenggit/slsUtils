library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Process rma2info summerized report file(s)')

parser$add_argument('fs', metavar='file', nargs='+', help='rma2info summerized report files')
parser$add_argument('--min', type="integer", help='feature reads最大数的下限, default=0', default=0)
parser$add_argument('--out', help='输出文件名', required='True')

args <- parser$parse_args()

print(args)

lst = lapply(args$fs, read_tsv, col_names = F)
names(lst) <- args$fs

raw_data = bind_rows(lst, .id = "Sample")
names(raw_data) <- c('Sample', 'Taxid', 'Reads')

df = raw_data %>%
		spread(Sample, Reads, fill = 0) %>%
		filter_at(-1, any_vars(.>=args$min))

write_tsv(df, args$out)

