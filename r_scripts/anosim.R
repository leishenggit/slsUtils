library(vegan)
library(dplyr)

Args <- commandArgs()

dis_mtx_f = Args[6]
meta_info_f = Args[7]
group_var = Args[8]
d_method = Args[9]
out_f = Args[10]
sample_col = 1


dis_mtx <- as.matrix( read.csv(dis_mtx_f, row.names = 1, check.names = FALSE) )
#读入meta数据
meta.info <- read.csv(meta_info_f, check.names = F, sep = '\t')
meta.info <- meta.info %>% filter(meta.info[[sample_col]] %in% c(row.names(dis_mtx )) )

g2g <- function(zu, meta.info, dis_mtx, group_v, d_method){
  gs <- paste(zu, collapse= ', ')
  
  expr <- sym(group_v)
  
  meta.info.m <- meta.info %>% filter(!!expr %in% zu)
  
  dis_mtx.m <- dis_mtx[as.vector(meta.info.m[[sample_col]]), as.vector(meta.info.m[[sample_col]])]
  dim(dis_mtx.m )
  
  x = anosim(dis_mtx.m, as.vector(meta.info.m[[group_v]]), permutations = 999)
  plot(x, col = c('gray', 'red', 'green', 'blue', 'orange', 'purple'), xlab='', ylab='')
  data.frame(Group = gs, R.value =round( x$statistic, 3), P.value = x$signif, Distance = d_method)
}

mtx <- combn(unique( meta.info[[group_var]] ), 2)
my_comparisons <- split(mtx, col(mtx))

pdf(paste(out_f, 'pdf', sep = '.'), width = 5, height = 4.5)
re <- bind_rows( lapply(my_comparisons, g2g, meta.info, dis_mtx, group_var, d_method) )
dev.off()

write.csv(re, out_f)

