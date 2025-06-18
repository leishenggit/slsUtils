library(dplyr)
library(readr)
library(tidyr)
library(stringr)

Args <- commandArgs()

fname = Args[6] 
cut.off = as.numeric( Args[7] )
N = as.numeric( Args[8] )

#get satisfied feature 
get_features <- function(dat, cut.off, N){
    tmp = dat %>% 
        gather('sample', 'abundance', -1) %>% 
        filter(abundance > cut.off) %>% #相对丰度最低超过阈值
        group_by_at(1) %>% 
        summarise(n=n()) %>% #超过最低相对丰度的样本个数
        filter(n>=N)
    return(tmp)
}

dat = read_tsv(fname)
dim(dat)

x = get_features(dat, cut.off, N)
dim(x)

dat = dat %>% filter(dat[[1]] %in% x[[1]])

#save data
write_tsv(dat, str_c(fname, cut.off, N, sep = '.'))

