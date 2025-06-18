library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='a script to do log transformation')

parser$add_argument('fs', metavar='file', nargs='+', help='files to do log transformation')
parser$add_argument('--cols', help='cols that do not need to log, default=1', nargs='+', type="integer", default=1)

args <- parser$parse_args()
print(args)


log_f <- function(fname){
	dat <- read_tsv(fname)
	df <- dat %>% mutate_at(-c(args$cols), function(x)ifelse(x>0,log(x,2), 0) )
	write_tsv(df, paste0(fname, '.log2'))
}

lapply(args$fs, log_f)

