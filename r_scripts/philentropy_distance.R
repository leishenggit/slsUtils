library(tidyverse)
library(philentropy)

Args <- commandArgs()
dat_f = Args[6]

dat <- read_tsv(dat_f) %>% 
    rename_at(vars(1), funs(return('feature'))) %>%
    gather('sample','expression', -1) %>%
    spread(feature, expression) %>%
    column_to_rownames(var='sample')

class(dat)
as_tibble(dat)

method_d = ifelse(length(Args)==7,  Args[7], "euclidean")
if(method_d == 'jsd'){
	res <- distance(dat, "jensen-shannon", est.prob = "empirical")
}else{
	res <- distance(dat, method_d, est.prob = NULL)
}

rownames(res) <- rownames(dat)
colnames(res) <- rownames(dat)

write.csv(res, paste("philentropy", dat_f, method_d, 'csv', sep="."))

#1] "euclidean"         "manhattan"         "minkowski"         "chebyshev"         "sorensen"          "gower"            
#[7] "soergel"           "kulczynski_d"      "canberra"          "lorentzian"        "intersection"      "non-intersection" 
#[13] "wavehedges"        "czekanowski"       "motyka"            "kulczynski_s"      "tanimoto"          "ruzicka"          
#[19] "inner_product"     "harmonic_mean"     "cosine"            "hassebrook"        "jaccard"           "dice"             
#[25] "fidelity"          "bhattacharyya"     "hellinger"         "matusita"          "squared_chord"     "squared_euclidean"
#[31] "pearson"           "neyman"            "squared_chi"       "prob_symm"         "divergence"        "clark"            
#[37] "additive_symm"     "kullback-leibler"  "jeffreys"          "k_divergence"      "topsoe"            "jensen-shannon"   
#[43] "jensen_difference" "taneja"            "kumar-johnson"     "avg" 