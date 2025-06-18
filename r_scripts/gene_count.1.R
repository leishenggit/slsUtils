library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='gene count group by sample')

parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--meta', help='file include two columns, first column is sample and second column is group', required='True')
parser$add_argument('--out', help='output file name', type="character", required='True')


args <- parser$parse_args()
print(args)

dat <- read_tsv(args$input)
meta <- read_tsv(args$meta)
out_f <- args$out


gs <- split(meta, meta[,2])

get_dat <- function(g, dat){
	re <- dat %>% 
		select(1, as.vector(g[[1]])) %>%
		filter_at(-1, any_vars(.>0)) %>%
		gather('Sample', 'TPM', -1) %>% 
		filter(TPM > 0) %>% 
		group_by(Sample) %>%
		summarise(N=n())
	return(re)
}


df.m <- bind_rows( lapply(gs, get_dat, dat), .id='Group')
write_tsv(df.m, out_f)

