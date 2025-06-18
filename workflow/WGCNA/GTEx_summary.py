#!/histor/sun/wujinyu/sls/software/python3/bin/python3
from collections import defaultdict
import argparse
import sys


def getRe(t_col, tissue):
	sample, col = defaultdict(list), defaultdict(list)
	with open("/histor/sun/maofb/shileisheng/oncobase/GTEx_Data_V6_Annotations_SampleAttrDS.txt") as f:
		f.readline()
		for line in f:
			l = line.strip().split("\t")
			if l[t_col] != "":
				sample[l[t_col]].append(l[0])#每个组织包含哪些样本号
	if tissue not in sample:
		print("Your inquery tissue seems does not exist ...")
		exit()
	with open("/histor/sun/maofb/shileisheng/oncobase/GTEx_Analysis_v6p_RNA-seq_RNA-SeQCv1.1.8_gene_rpkm") as f:
		f.readline()
		f.readline()#跳过前2行无用信息
		head = f.readline().strip().split("\t")#样本号存入head列表
		for i in range(2,len(head)):
			if head[i] in sample[tissue]: col[tissue].append(i)#该组织包含哪些列
		#打印该组织对应的列索引
		#print(tissue, len(col[tissue]), col[tissue])
		rel = [ head[i] for i in col[tissue] ]
		print('gene', '\t'.join(rel), sep='\t')
		for line in f:
			l = line.strip().split("\t")
			expr = [l[c] for c in col[tissue]] #取出该组织包含的列
			print(l[0], '\t'.join(expr), sep='\t')
	return sample
 

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = 'A program for extracted tissue expression data')
	parser.add_argument('tissue', help='Please input a tissue name', type=str)
	parser.add_argument('--col', help='Please input the tissue col number', type=int, choices=[5,6], default=6)
	parser.add_argument('-v', '--verbose', help='print details', action="store_true")
	args = parser.parse_args()
	#get data
	sample = getRe(args.col, args.tissue)
	if args.verbose:
		#打印每个组织对应的样本号数目和样本号
		sys.stderr.write('\t'.join(['tissue','sample_count', 'sample_ids'])+'\n')
		for k in sample: sys.stderr.write(k+'\t'+str(len(sample[k]))+'\t'.join(sample[k]))
		
