library(argparse)
suppressMessages(library(tidyverse))
library(Hmisc)

parser <- ArgumentParser(description='plot network from a OTU file')

parser$add_argument('--input_1', help='OTU-like file', required='True')
parser$add_argument('--input_2', help='OTU-like file', required='True')
parser$add_argument('--taxonomy', help='file include OTU taxonomy level info', required='True')
parser$add_argument('--top', type="integer", help='top N features, default=35', default=35)
parser$add_argument('--cor_method', help='correlation method, default=spearman', default='spearman')
parser$add_argument('--p_cutoff', help='cutoff of pvalue, default=0.05', type="double", default=0.05)
parser$add_argument('--r_cutoff', help='correlation method, default=0.2', type="double", default=0.2)

args <- parser$parse_args()

print(args)

dat_1 <- read_tsv(args$input_1)
dat_2 <- read_tsv(args$input_2)
taxonomy <- read_tsv(args$taxonomy)
N <- args$top
cor_method <- args$cor_method

taxonomy <- taxonomy %>%  rename_at(ncol(taxonomy), function(x)return("tax_name"))

top_1 <- dat_1 %>% mutate(total = rowMeans(dat_1[,-1])) %>% top_n(N, total)
top_2 <- dat_2 %>% mutate(total = rowMeans(dat_2[,-1])) %>% top_n(N, total)

belong_1 <- top_1 %>% select(1) %>% mutate(belong=args$input_1)
belong_2 <- top_2 %>% select(1) %>% mutate(belong=args$input_2)
overlop <- paste(args$input_1, args$input_2, sep='.')
write_tsv(bind_rows(belong_1, belong_2), overlop)

tmp <- function(g, N){
	ifelse(N>1, 'Shared', g)
}
groups <- bind_rows(belong_1, belong_2) %>% group_by_at(1) %>% mutate(N = n()) %>% ungroup()
groups <- groups %>% mutate(belong = mapply(tmp, groups$belong, groups$N) )


top <- left_join(dat_1 %>% filter(dat_1[[1]] %in% groups[[1]]), dat_2 %>% filter(dat_2[[1]] %in% groups[[1]]))
top <- top %>% mutate(total = rowMeans(top[,-1]))

df <- as.data.frame( top[,-c(1,ncol(top))] )
row.names(df) <- top[[1]]
x=t(df)
res <- rcorr(x, type = cor_method) #相关系数与P值

nodes <- data.frame(tax_name=top[[1]], abundance=top$total) # 节点
nodes <- nodes %>% left_join(groups) %>% left_join(taxonomy)


mtx_df <- function(mtx){
  mtx[lower.tri(mtx)] <- NA
  diag(mtx) <- NA
  df <- as.data.frame(mtx)
  df$from <- row.names(df)
  df.m <- df %>%  gather('to','r',-ncol(df)) %>% filter(!is.na(r))
}

links <- mtx_df(res$r) # 边
ps <- mtx_df(res$P) %>% rename(pvalue = r) # P value
links <- links %>% left_join(ps) %>% filter(pvalue < args$p_cutoff, abs(r) > args$r_cutoff)


links_f <- paste(args$input_1, args$input_2, args$cor_method, 'link.tsv', sep='.')
write_tsv(links, links_f)

nodes <- nodes %>% filter(tax_name %in% c(links$from, links$to))
nodes_f <- paste(args$input_1, args$input_2, args$cor_method, 'node.tsv', sep='.')
write_tsv(nodes, nodes_f)

