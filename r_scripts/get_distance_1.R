
Args <- commandArgs()

dat_f = Args[6]
method_d = ifelse(length(Args)==7,  Args[7], "euclidean")

otu_abundance = read.csv(dat_f, header = T, row.names = 1, sep = '\t', check.names = F)
res <- dist(t(otu_abundance), method_d)

write.csv( as.matrix(res), paste(dat_f, method_d, 'csv', sep="."))

