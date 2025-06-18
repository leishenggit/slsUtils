library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='extract shared cols from some files and saved')

parser$add_argument('fs', metavar='file', nargs='+', help='files to do intersection')
parser$add_argument('--cols', help='cols that must select, default=1', nargs='+', type="integer", default=1)

args <- parser$parse_args()
print(args)

dat.lst <- lapply(args$fs, read_tsv)

names(dat.lst) <- args$fs


lst <- lapply(dat.lst, colnames)

overlop <- reduce(lst, intersect)

save_dat <- function(x, fname, overlop_col, cols){
  df <- x %>% select(cols, overlop_col)
  write_tsv(df, paste0(fname, '.intersect'))
}

mapply( save_dat, dat.lst, names(dat.lst), MoreArgs = list(overlop_col = overlop, cols = args$cols) )
