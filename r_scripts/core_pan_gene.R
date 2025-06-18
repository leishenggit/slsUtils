library(tidyverse)

Args <- commandArgs()
input_f = Args[6]
width = as.numeric(Args[7])
height = as.numeric(Args[8])

get_gene <- function(n, df){
    zu <- bind_cols( lapply(1:30, function(x) sample(2:ncol(df), n)) )

    #zu <- combn(2:ncol(df), n)
  
  tmp <- function(cols, df){
    core_gene <- df[cols] %>% filter_all(all_vars(.>0))
    pan_gene <- df[cols] %>% filter_all(any_vars(.>0))
    return(data.frame(N=n, zu=str_c(cols, collapse = ":"), core=nrow(core_gene), pan=nrow(pan_gene)))
  }
  
  lst <- lapply(as.data.frame(zu), tmp, df)
  bind_rows(lst)
}


#gene<- data.frame(gene=letters[1:10], samA=sample(0:10,10,T),samB=sample(0:10,10,T),samC=sample(0:10,10,T))
gene <- read_tsv(input_f)
dat <- bind_rows( lapply(1:(ncol(gene)-1), get_gene, gene) )
write_tsv(dat, paste0(input_f,'.core-pan.res'))

pdf(paste0(input_f,'.core-pan.pdf'), width=width, height=height)
ggplot(dat, aes(factor(N), core))+
  geom_boxplot(fill="#DA5724")+
  labs(x='Number of samples', y='Number of non-redundant genes',title='Core gene')+
  theme_bw()+
  theme(axis.title = element_text(size = 14),axis.text = element_text(size = 8))

ggplot(dat, aes(factor(N), pan))+
  geom_boxplot(fill= "#8A7C64")+
  labs(x='Number of samples', y='Number of non-redundant genes',title='Pan gene')+
  theme_bw()+
  theme(axis.title = element_text(size = 14),axis.text = element_text(size = 8))
dev.off()

