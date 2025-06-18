library(venn)
library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Venn plot')

parser$add_argument('--input', help='OTU-like file', required='True')
parser$add_argument('--meta', help='file include two columns, first column is sample and second column is group', required='True')
parser$add_argument('--out', help='output file name', type="character", required='True')
parser$add_argument('--width', help='width for the plot, default=7', type="double", default=7)
parser$add_argument('--height', help='height for the plot, default=7', type="double", default=7)

args <- parser$parse_args()
print(args)

dat <- read_tsv(args$input)
meta <- read_tsv(args$meta)
out_f <- args$out
width <- args$width
height <- args$height

gs <- split(meta, meta[,2])

get_dat <- function(g, dat){
	re <- dat %>% 
		select(1, as.vector(g[[1]])) %>%
		filter_at(-1, any_vars(.>0))
		
	return(re[[1]])
}

venn_list <- lapply(gs, get_dat, dat)
str(venn_list)
#my_name <- unlist( lapply(gs, function(x){unique(x[[2]])}) )
#names(venn_list) <- my_name
#作图
pdf(out_f, width = width, height = height)
venn(venn_list, zcolor = 'style')
dev.off()

