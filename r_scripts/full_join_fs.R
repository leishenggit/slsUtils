library(tidyverse)
library(argparse)

parser <- ArgumentParser(description='full_join many otu table files')
parser$add_argument('fs', metavar='file', nargs='+', help='OTU table files')
parser$add_argument('--out', help='output filename', required='True')
args <- parser$parse_args()
print(args)

merge_df <- function(df1, df2){
  z = bind_rows(df1, df2)
}

get_dat <- function(f){
    x = read_tsv(f) %>% gather('Sample','Reads', -1) %>% filter(Reads > 0)
}

dat <- lapply(args$fs, get_dat)

res <- Reduce(merge_df, dat)

write_tsv(res, args$out)

#/home/shileisheng/anaconda3/envs/R3.6/bin/Rscript  full_join_fs.R LuJ_resample/*.txt --out all_otu.txt