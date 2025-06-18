library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='split file into seperate files by groups')

parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--meta', help='file include two columns, first column is sample and second column is group', required='True')
parser$add_argument('--cols', help='cols that must select, default=1', nargs='+', type="integer", default=1)

args <- parser$parse_args()
print(args)

dat <- read_tsv(args$input)
meta <- read_tsv(args$meta)
cols <- args$cols

gs <- split(meta, meta[,2])

save_dat <- function(g, dat, cols, fname){
	re <- dat %>% 
		select(cols, as.vector(g[[1]])) %>%
		filter_at(as.vector(g[[1]]), any_vars(.>0))
		
	ref <- paste(fname, unique(g[[2]]), sep='.')
	write_tsv(re, ref)
}

lapply(gs, save_dat, dat, cols, args$input)
