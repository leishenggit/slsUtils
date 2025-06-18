#!/usr/bin/Rscript

Args <- commandArgs()

fname = Args[6] 

data = read.csv(fname, header = F, sep = '\t', fileEncoding = "utf-8")

x = as.data.frame ( t(data) )

write.table(x, file = paste(fname, "tr", sep = "."), row.names = F, col.names = F, quote = F, sep="\t")
