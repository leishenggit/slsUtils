library(argparse)
suppressMessages(library(tidyverse))

parser <- ArgumentParser(description='Boxplot')

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
		filter_at(-1, any_vars(.>0)) %>%
		gather('Sample', 'TPM',-1) %>% 
		filter(TPM > 0) %>% 
		group_by(Sample) %>%
		summarise(N=n())
	return(re)
}
df.m <- bind_rows( lapply(gs, get_dat, dat), .id='Group')
write_tsv(df.m, paste0(out_f,".txt"))
#作图
pdf(out_f, width = width, height = height)
ggplot(df.m, aes(Group, N, fill=Group)) + geom_boxplot()
dev.off()

