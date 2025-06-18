library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Process depth file(s) to compute coverge at different depth')

parser$add_argument('fs', metavar='file', nargs='+', help='samtools depth file')
field_group <- parser$add_mutually_exclusive_group(required='True')
field_group$add_argument('--effect_depth', type="integer", nargs=2, help='depth range need to calculate')
field_group$add_argument('--effect_depth_s', help='depths to calculate coverage', type="integer", nargs="+")
parser$add_argument('--out', help='output filename', required='True')

args <- parser$parse_args()

print(args)

get_res <- function(fname, depths){
  raw_data <- read_tsv(fname, col_names = c("chr", "position", "depth"))
  
  cal <- function(effect_depth, df){
    data.m = df %>%
        group_by(chr) %>%
        mutate(chr_len = max(position)) %>% 
        filter(depth >= effect_depth) %>% 
        mutate(N=n()) %>%
        summarise(coverage = unique(N/chr_len)) %>% 
        mutate(depth = effect_depth)
  }
  
  res <- lapply(depths, cal, raw_data)
  bind_rows(res)
}

if(is.null(args$effect_depth_s)){
	effect_depths <- seq(args$effect_depth[1], args$effect_depth[2])
}else{
	effect_depths <- args$effect_depth_s
}

lst = lapply(args$fs, get_res, effect_depths)
names(lst) <- str_replace(args$fs,  '.*[/]', '')

raw_data = bind_rows(lst, .id = "Sample")

write_tsv(raw_data, args$out)

