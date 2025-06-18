#!/home/shileisheng/anaconda3/envs/R3.6/bin/Rscript
library(readr)
library(dplyr)

Args <- commandArgs()

fname = Args[6]
otu = Args[7]


dat = read_tsv(fname)

if(otu == 'otu'){
    dat <- dat %>% mutate_at(-1, function(.).=./sum(.)) %>% mutate_at(-1, function(.)ifelse(is.na(.), 0, .) )
}else{
    dat <- dat %>% mutate_all(function(.).=./sum(.)) %>% mutate_all(function(.)ifelse(is.na(.), 0, .) )
}

write_tsv(dat, paste(fname, "relab", sep = "."))

