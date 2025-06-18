#!/histor/sun/maofb/anaconda3/envs/R4.0.2/bin/Rscript
library(tidyverse)

num_seq = read_tsv('num_seq.txt')

get_res <- function(in_f, out_f, num_seq){
  x = read_tsv(in_f)
  y = x %>% gather('Sample','relab', -1) %>% left_join(num_seq) %>% mutate(reads = round(relab * after_remove_host)) %>% select(-3,-4) %>% spread(Sample,reads, fill = 0 )
  write_tsv(y, out_f)
}

get_res('salmon.gene.tpm.relab', 'salmon.gene.tpm.txt', num_seq )


