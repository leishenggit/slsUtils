library(phyloseq)

Args <- commandArgs()
dat_f = Args[6]

method_d = ifelse(length(Args)==7,  Args[7], "euclidean")

otu_abundance = read.csv(dat_f, header = T, row.names = 1, sep = '\t', check.names = F)
OTU = otu_table( as.matrix(otu_abundance), taxa_are_rows=T )
res <- distance(OTU, method_d)

write.csv( as.matrix(res), paste("phyloseq", dat_f, method_d, 'csv', sep="."))

##=========method:
#UniFrac1     UniFrac2        DPCoA          JSD     vegdist1     vegdist2 
#  "unifrac"   "wunifrac"      "dpcoa"        "jsd"  "manhattan"  "euclidean" 
#   vegdist3     vegdist4     vegdist5     vegdist6     vegdist7     vegdist8 
# "canberra"       "bray" "kulczynski"    "jaccard"      "gower"   "altGower" 
#   vegdist9    vegdist10    vegdist11    vegdist12    vegdist13    vegdist14 
# "morisita"       "horn"  "mountford"       "raup"   "binomial"       "chao" 
#  vegdist15   betadiver1   betadiver2   betadiver3   betadiver4   betadiver5 
#      "cao"          "w"         "-1"          "c"         "wb"          "r" 
# betadiver6   betadiver7   betadiver8   betadiver9  betadiver10  betadiver11 
#        "I"          "e"          "t"         "me"          "j"        "sor" 
#betadiver12  betadiver13  betadiver14  betadiver15  betadiver16  betadiver17 
#        "m"         "-2"         "co"         "cc"          "g"         "-3" 
#betadiver18  betadiver19  betadiver20  betadiver21  betadiver22  betadiver23 
#        "l"         "19"         "hk"        "rlb"        "sim"         "gl" 
#betadiver24        dist1        dist2        dist3   designdist 
#        "z"    "maximum"     "binary"  "minkowski"        "ANY" 
