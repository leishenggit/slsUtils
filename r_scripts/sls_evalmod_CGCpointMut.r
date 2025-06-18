library(precrec)
library(pROC)
suppressMessages(library(dplyr))
library(tidyr)
library(readr)
library(argparse)

#设置参数容器
parser <- ArgumentParser(description='Process some paras')
#设置参数
parser$add_argument('fs', metavar='files', nargs='+', help='input files')
parser$add_argument('--method', help='data from which network algorithm, such as "hotnet2"', required=TRUE)
parser$add_argument('--source', help='data source ,such as "GeneMANIA"', required=TRUE)
parser$add_argument('--type', help='data type ,such as "CGCpointMut"', required=TRUE)
parser$add_argument('--out', help='output file, default is "$method.$source.$type.txt"')
#获取参数
args <- parser$parse_args()

out_f = ifelse(is.null(args$out), paste(args$method, args$source, args$type, 'txt', sep='.'), args$out)

do_evalmod <- function(f, label){
	dat <- read.table(f, head=T, sep="\t")
	if( length( unique(dat[[label]])) > 1){
		obj <- evalmod(scores = as.numeric(dat[,"Score"]),labels = dat[,label], mode="basic")
	}
}

precrec_obj <- lapply(args$fs, do_evalmod, args$type)
names(precrec_obj) <- args$fs
res <- lapply(precrec_obj, attr, 'eval_summary')

df <- bind_rows(res, .id='cancer') %>% 
	select(cancer, evaltypes, meanvals) %>% 
	mutate(cancer = sub('.*[/]','',cancer)) %>% 
	spread(evaltypes, meanvals) %>% 
	mutate(attr_1 = args$method,  attr_2=args$source, attr_3 = args$type)

#=======get AUC =================
get_auc <- function(f, label){
	dat <- read.table(f, head=T, sep="\t")
	if( length( unique(dat[[label]])) != 2){
	return( data.frame() )
	}
	rocobj <- roc(dat[[label]], dat$Score)
	return( data.frame(AUC=auc(rocobj)) )
}

auc_res <- lapply(args$fs, get_auc, args$type)
names(auc_res) <- args$fs
auc_df <- bind_rows(auc_res , .id='cancer')

res <- df %>% left_join(auc_df)

write_tsv(res, out_f)
