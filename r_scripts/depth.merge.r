#!/pnas/limk_group/shilsh/software/anaconda3/envs/R3.6/bin/Rscript
library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Process depth file(s)')

parser$add_argument('fs', metavar='file', nargs='+', help='samtools depth file')
parser$add_argument('--region_size', type="integer", help='window size(bp), default=1000', default=1000)
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)


get_res <- function(fname, region_size){
  raw_data <- read_tsv(fname, col_names = c("chr", "position", "depth"))
  data.m = raw_data %>%
        mutate(position = ceiling(position/region_size)) %>%
        group_by(chr, position) %>%
        summarise(depth = mean(depth)) %>%
	mutate(window_size = region_size) 
  
}

lst = lapply(args$fs, get_res, args$region_size)
names(lst) <-  str_replace(args$fs,  '.*[/]', '')

raw_data = bind_rows(lst, .id = "Sample")

write_tsv(raw_data, args$out)

