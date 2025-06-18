library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='gene count')

parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--meta', help='file include two columns, first column is sample and second column is group', required='True')
parser$add_argument('--out', help='output file name', type="character", required='True')
parser$add_argument('--sample', help='count by sample', action='store_true')

args <- parser$parse_args()
print(args)

dat <- read_tsv(args$input)
meta <- read_tsv(args$meta)
out_f <- args$out


gs <- split(meta, meta[,2])

if(args$sample){
	get_dat <- function(g, dat){
		re <- dat %>% 
			select(1,ncol(dat), as.vector(g[[1]])) %>%
			filter_at(-c(1,2), any_vars(.>0)) %>%
			gather('Sample', 'TPM', -c(1,2)) %>% 
			filter(TPM > 0) %>% 
			group_by_at(c(2,3)) %>%
			summarise(N=n())
		return(re)
	}
}else{
	get_dat <- function(g, dat){
		re <- dat %>% 
			select(1,ncol(dat), as.vector(g[[1]])) %>%
			filter_at(-c(1,2), any_vars(.>0)) %>%
			gather('Sample', 'TPM', -c(1,2)) %>% 
			filter(TPM > 0) %>% 
			group_by_at(2) %>%
			summarise(N=n())
		return(re)
	}
}

df.m <- bind_rows( lapply(gs, get_dat, dat), .id='Group')
write_tsv(df.m, out_f)

