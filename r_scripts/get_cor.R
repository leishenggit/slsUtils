library(argparse)
suppressMessages(library(tidyverse))
library(Hmisc)

parser <- ArgumentParser(description='plot network from a OTU file')


parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--top', type="integer", help='top N features, default=35', default=35)
parser$add_argument('--cor_method', help='correlation method, default=spearman', default='spearman')

args <- parser$parse_args()

print(args)

dat <- read_tsv(args$input)
N <- args$top
cor_method <- args$cor_method

top <- dat %>% 
		mutate(total = rowSums(dat[,-1])) %>%
		top_n(N, total) %>% 
		arrange(desc(total))


df <- as.data.frame( top[,-c(1,ncol(top))] )
row.names(df) <- top[[1]]
x=t(df)
res <- rcorr(x, type = cor_method) #相关系数与P值
cor_ref <- paste(args$input, args$cor_method, 'csv', sep='.')
cor_ref_p <- paste(args$input, args$cor_method, 'p.csv', sep='.')
write.csv(res$r, cor_ref)
write.csv(res$P, cor_ref_p)


