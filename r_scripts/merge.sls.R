library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='merge summarized taxid_reads file(s)')

parser$add_argument('--input', nargs='+', help='gene score files', required='True')
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)

lst = lapply(args$input, read_tsv, col_names = F)
names(lst) <- args$input

raw_data = bind_rows(lst, .id = "filename")
names(raw_data) <- c('filename','gene', 'score')

res <- raw_data %>% separate(filename, into = c('method', 'cancer', 'network'), sep = '_', remove = F)

write_tsv(res, args$out)

