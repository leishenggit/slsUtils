library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Process taxmaps report file(s)')

parser$add_argument('fs', metavar='file', nargs='+', help='taxmaps report files')
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)

lst = lapply(args$fs, read_tsv, col_names = F)
names(lst) <- args$fs

raw_data = bind_rows(lst, .id = "sample")
names(raw_data) <- c('sample', 'taxid', 'rank', 'level', 'path', 'tax_name', 'reads', 'abundance')

tax = raw_data %>%
		select(-4, -5, -8) %>%
		mutate(sample = str_replace(sample, '[.]tbl','')) %>%
		mutate(sample = str_replace(sample, '.*[/]','')) %>%
		spread(sample, reads, fill = 0) 

df = tax %>% mutate(row_sum = rowSums(tax[,-c(1,2,3)]) )  %>%
                arrange(rank, desc(row_sum) ) %>% 
                mutate(row_sum = NULL)


write_tsv(df, args$out)
