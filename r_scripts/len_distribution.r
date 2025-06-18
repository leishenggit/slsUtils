library(ggplot2)
library(argparse)

parser <- ArgumentParser(description='plot length distribution')

parser$add_argument('fs', metavar='file', nargs='+', help='files with two columns')
parser$add_argument('--frac', type="double", help='frac of data to draw,default=1', default=1)
parser$add_argument('--bins', type="integer", help='number of bins to draw,default=50', default=50)
parser$add_argument('--width', type="double", help='width of the plot, default=7', default=7)
parser$add_argument('--height', type="double", help='height of the plot, default=7', default=7)

args <- parser$parse_args()

print(args)


plot_len_dist <- function(fname, frac, N_bins){
    raw_dat <- read.csv(fname, header = T, sep = '\t', check.names = F, fileEncoding = "utf-8")
    colnames(raw_dat) <- c('feature','len')
	N = round(nrow(raw_dat) * frac)
	dat <- raw_dat[order(raw_dat[,2]), ][1:N, ]
    pdf(paste(fname,'pdf',sep='.'),  width=args$width, height=args$height)
    #histogram
    pic <- ggplot(raw_dat, aes(len))+
            geom_histogram(bins = N_bins)+
            theme_bw()
    print(pic)
    dev.off()
    cat('Finish', fname)
}

mapply(plot_len_dist, args$fs, args$frac, args$bins)
