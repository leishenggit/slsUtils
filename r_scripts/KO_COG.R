library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='KO_COG merge')

parser$add_argument('--input', help='gene_KO file', required='True')
parser$add_argument('--out', help='output file name', type="character", required='True')

args <- parser$parse_args()
print(args)

dat <- read_tsv(args$input)
out_f <- args$out

res <- dat %>% 
	gather('Sample','TPM',-c(1, ncol(dat))) %>% 
	group_by_at(c(2,3))  %>% 
	summarise(TPM = sum(TPM)) %>% 
	ungroup() %>% 
	spread(Sample, TPM, fill=0)

write_tsv(res, out_f)
