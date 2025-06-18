library(argparse)
library(readr)
library(ggraph)
library(tidygraph)

parser <- ArgumentParser(description='plot network from a nodes file and a links file')

parser$add_argument('--nodes', help='nodes file', required='True')
parser$add_argument('--links', help='links file', required='True')
parser$add_argument('--out_f', help='result pdf file', required='True')

args <- parser$parse_args()

print(args)

nodes <- read_tsv(args$nodes)
links <- read_tsv(args$links)

head(nodes)
head(links)


# Create graph 
graph <- tbl_graph(nodes = nodes,  edges = links, directed = FALSE)
graph
# plot using ggraph
pdf(args$out_f, width=8, height=5)
ggraph(graph, layout = 'kk') + 
    	geom_edge_link(aes(colour = r>0, alpha = -log(pvalue, 10), width=abs(r)) ) + 
	scale_edge_width_continuous(range = c(0.2, 2)) +
    	geom_node_point(aes(size = abundance, colour=phylum, shape=belong)) +
	geom_node_text(aes(label=tax_name), size=3, repel = TRUE) +
	theme(legend.position="top", legend.direction = "vertical")
dev.off()


