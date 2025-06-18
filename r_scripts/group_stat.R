library(tidyverse)

#========================= group stat ========================================
get_dat <- function(g, line, meta.info){
  live = meta.info %>% filter(group_2 %in% g)
  live.sam = intersect(colnames(line), live$Sample)
  res = line %>% select(live.sam) %>% gather("Sample","abundance")
  return(res[[2]])
}

group_abundance_stat <- function(line, meta.info, rank_dat){
  tmp <- function(g, line, meta.info, tax_rank_dat){
    live <- get_dat(g, line, meta.info)
    occurence <- length( live[live > 0] ) / length( live )
    occurence_all <- length( live[live > 0] ) / 95
    rank_m <- round( mean(get_dat(g, tax_rank_dat, meta.info)) )
    return(data.frame(mean_abundance = mean(live), median_abundance = median(live), Occurence = occurence, Occurence_all = occurence_all, rank_mean = rank_m, Group = g))
  }
  
  tax_rank_dat <- rank_dat %>% filter(rank_dat[[1]] %in% line[[1]])
  
  bind_rows( lapply(unique( meta.info$group_2 ), tmp, line, meta.info, tax_rank_dat) )
}

dat_f = '../beta/salmon.gene.relab.txt.1e-04.1'
res_f = 'gene.groups.stat.txt'

dat <- read_tsv(dat_f) 
rank_dat <- dat %>% mutate_at(-1, function(x)rank(x))
lst <- split(dat, list(dat[[1]]))
meta.info <- read_tsv('../meta.txt')

res <- bind_rows( lapply(lst, group_abundance_stat, meta.info, rank_dat), .id="feature")
write_csv(res, res_f)

