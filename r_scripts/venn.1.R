library(venn)
library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Venn plot')

parser$add_argument('--input',  nargs='+', help='two or more files which contain features(such as gene)', required='True')
parser$add_argument('--names',  nargs='+', help='two or more group names which corresponding input files')
parser$add_argument('--out', help='output file name', type="character", required='True')
parser$add_argument('--width', help='width for the plot, default=7', type="double", default=7)
parser$add_argument('--height', help='height for the plot, default=7', type="double", default=7)

args <- parser$parse_args()
print(args)

out_f <- args$out
width <- args$width
height <- args$height

lst <- lapply(args$input, function(f){dat=read_tsv(f, col_names = F);dat[[1]]} ) 

str(lst)

if(length(args$names) > 0 ){
	names(lst) <- args$names
}else{
	names(lst) <- args$input
}
str(lst)

#作图
pdf(out_f, width = width, height = height)
venn(lst, zcolor = 'style')
dev.off()

