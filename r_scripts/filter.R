library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Process kraken report file(s)')

parser$add_argument('fs', metavar='file',  help='OUT-like file')
parser$add_argument('--out', help='output filename', required='True')
parser$add_argument('--min', help='min abundance, default=0.01', type="double", default=0.01)
parser$add_argument('--min_n', help='Number of samples that greater than the min abundance, default=1', type="integer", default=1)

args <- parser$parse_args()

print(args)


get_features <- function(dat, cut.off, N){
  
  tmp = dat %>% 
    gather('sample', 'abundance', -1) %>% 
    filter(abundance > cut.off) %>% #相对丰度最低超过阈值
    group_by_at(1) %>% 
    summarise(n=n()) %>% #超过最低相对丰度的样本个数
    filter(n>=N)
  
  res = dat %>% filter(dat[[1]] %in% tmp[[1]])
  
  return(res)
}

dat <- read_tsv(args$fs)

res <- get_features(dat, args$min, args$min_n)

write_tsv(res, args$out)

