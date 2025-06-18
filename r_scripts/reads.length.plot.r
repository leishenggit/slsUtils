# get paras from CMD
Args <- commandArgs()
if(length(Args) < 8) {
	print("please input a reads length count file, a number for bins and length cutoff")
	q()
}
print(Args)
print('--------------------------------------------')
fname <- Args[6]
print(fname)
bins <- as.numeric(Args[7])
print(bins)
length_cutoff <- as.numeric(Args[8])
print(length_cutoff)


#histogram
myplot_histogram <- function(my_data, mytitle, mycol, myxlab, bins="Sturges"){
  return_v = hist(x=my_data, breaks=bins, font.lab = 2, main = NULL, xlab = myxlab, col=mycol, freq = T)
  segments(16569, 0, 16569, max(return_v$counts), col="red")
  title(main = mytitle)
  #print(return_v$breaks)
  #print(my_data.frame(Breaks=return_v$breaks[-1], Counts=return_v$counts))
}

pdf(file = paste(fname, "hist.pdf", sep="."))
my_data = read.table(fname, head=T, sep = "\t")
my_title = unlist(strsplit(fname, ".", fixed=TRUE))[1]
x = my_data[,4]
myplot_histogram(x[x < length_cutoff], my_title, "lightblue", "reads length", bins)
dev.off()




