library(vegan)
library(dplyr)

Args <- commandArgs()

dis_mtx_f = Args[6]
meta_info_f = Args[7]
group_var = Args[8]
d_method = Args[9]
out_f = Args[10]
sample_col = 1

#距离矩阵文件
dis_mtx <- as.matrix( read.csv(dis_mtx_f, row.names = 1, check.names = FALSE) )
#样本分组文件
meta.info <- read.csv(meta_info_f, check.names = F, sep = '\t')
meta.info <- meta.info %>% filter(meta.info[[sample_col]] %in% c(row.names(dis_mtx )) )

##PERMANOVA 分析（所有组间比较，即整体差异）
#adonis_result <- adonis(dis_mtx ~ meta.info[[group_var]], meta.info , permutations = 999)

#将主要的统计结果转化为数据框的类型
#otuput <- data.frame(adonis_result$aov.tab, check.names = FALSE, stringsAsFactors = FALSE)

#不同组间比较
ad <- function(zu, dis_mtx, meta_info, group_v, d_method){
  gs <- paste(zu, collapse= ', ')
  
  expr <- sym(group_v)
  #filter samples
  samples <- meta_info %>% filter(!!expr %in% zu)
  dis <- dis_mtx[as.vector(samples[[sample_col]]),  as.vector(samples[[sample_col]]) ]
  ##PERMANOVA 分析
  adonis_result <- adonis(dis ~ samples[[group_v]], samples, permutations = 999)
  #将主要的统计结果转化为数据框的类型
  otuput <- data.frame(adonis_result$aov.tab, check.names = FALSE, stringsAsFactors = FALSE)
  res <- otuput %>% mutate(Group = gs, Distance = d_method)
}

mtx <- combn(unique( meta.info[[group_var]] ), 2)
my_comparisons <- split(mtx, col(mtx))


res <- lapply(my_comparisons, ad, dis_mtx, meta.info, group_var, d_method )
df <- bind_rows(res)
df <- df %>% distinct(Group, .keep_all = T)
write.csv(df, out_f)

