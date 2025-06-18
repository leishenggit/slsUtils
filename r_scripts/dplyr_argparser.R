library(tidyverse)
library(argparse)

parser <- ArgumentParser(description='Plot module result')

parser$add_argument('fs', metavar='files', nargs='+', help='file like netsig.mentha.CGC.txt')
parser$add_argument('--metric', nargs='+', help='the metric to plot,such as accuracy,precision', required=T)

args <- parser$parse_args()

dat <- bind_rows( lapply(args$fs, read_tsv) ) %>% rename(method=attr_1, network=attr_2, dataset=attr_3)

my_plot <- function(dat, m){
	expr <- sym(m)
	res = dat %>%
		  group_by(method, dataset) %>%
		  summarise(sd=sd(!!expr), median = median(!!expr))
	
	write_tsv(res, paste0(m, ".sd.median"))

	pdf(file = paste0(m, ".pdf"))


	pic <- ggplot(res, aes(x = method, y = median, fill = dataset)) + 
	  geom_bar(stat = "identity", position = "dodge") + 
	  geom_errorbar(aes(ymax = median + sd, ymin = median -  sd), 
                position = position_dodge(0.9), width = 0.15) + 
	  scale_fill_brewer(palette = "Paired") +
	  theme(legend.title = element_blank(),
        	panel.grid = element_blank(),
	        panel.background = element_rect(fill = "white",colour = "black"),
        	axis.text = element_text(colour = "black"),
	        axis.ticks = element_line(colour = "black"),
        	legend.position = "top")
	print(pic)

	dev.off()
}

mapply(my_plot, list(dat), args$metric)


