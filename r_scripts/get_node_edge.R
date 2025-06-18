library(argparse)
suppressMessages(library(tidyverse))
library(Hmisc)

parser <- ArgumentParser(description='plot network from a OTU file')

parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--taxonomy', help='file include OTU taxonomy level info', required='True')
parser$add_argument('--top', type="integer", help='top N features, default=35', default=35)
parser$add_argument('--cor_method', help='correlation method, default=spearman', default='spearman')
parser$add_argument('--p_cutoff', help='cutoff of pvalue, default=0.05', type="double", default=0.05)
parser$add_argument('--r_cutoff', help='correlation method, default=0.2', type="double", default=0.2)

args <- parser$parse_args()

print(args)

dat <- read_tsv(args$input)
taxonomy <- read_tsv(args$taxonomy)
N <- args$top
cor_method <- args$cor_method

taxonomy <- taxonomy %>%  rename_at(ncol(taxonomy), function(x)return("tax_name"))


top <- dat %>% 
		mutate(total = rowMeans(dat[,-1])) %>%
		top_n(N, total) %>% 
		arrange(desc(total))


df <- as.data.frame( top[,-c(1,ncol(top))] )
row.names(df) <- top[[1]]
x=t(df)
res <- rcorr(x, type = cor_method) #相关系数与P值

nodes <- data.frame(tax_name=top[[1]], abundance=top$total) # 节点
nodes <- nodes %>% left_join(taxonomy)


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


links_f <- paste(args$input, args$cor_method, 'link.tsv', sep='.')
write_tsv(links, links_f)

nodes <- nodes %>% filter(tax_name %in% c(links$from, links$to))
nodes_f <- paste(args$input, args$cor_method, 'node.tsv', sep='.')
write_tsv(nodes, nodes_f)

