from functools import reduce
import itertools
import sys
import argparse


def jiaoji(a, b=None):
	if not b:
		return set(a)
	c = list(set(a).intersection(set(b)))
	return c

def overlop_gene_2(all_gene):
	files = list(all_gene.keys())
	print('source'+'\t'+'\t'.join(files))
	for f in files:
		print(f+'\t'+'\t'.join([str(len(jiaoji(all_gene[f], all_gene[i]))) for i in files]))


def overlop_gene(all_gene):
	files = list(all_gene.keys())
	N = len(files)
	for i in range(1, N+1):
		for zuhe in itertools.combinations(files, i):
			re = set(reduce(jiaoji, [all_gene[file] for file in zuhe]))
			print('\t'.join(zuhe), len(re), sep='\t')
			print('\t'.join(re))


def test():
	a=[2,2,3,4,5]
	b=[2,5,8]
	c=[1,2,3]
	print('a:', a)
	print('b:', b)
	print('c:', c)
	#交集
	print("a,b 交集:", list(set(a).intersection(set(b))))
	#并集
	print("a,b 并集:",list(set(a).union(set(b))))
	#差集: b中有而a中没有
	print("b,a 差集:", list(set(b).difference(set(a))))
	#reduce get jiaoji of multiple lists 
	print ('a,b,c 交集:', reduce(jiaoji, [a,b,c]))



if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input', nargs='+', type=str, help='one or more file contain genes')
	parser.add_argument('--head', help='whether drop the first line', action="store_true")
	parser.add_argument('--col', help='col number of the gene, default=1',  type=int, default=1)
	parser.add_argument('--mode', help='overlop mode. mode 1: any overlop sets will output; mode 2: ovelop one set to other sets. default=1',  type=int, choices=[1,2], default=1)
	parser.add_argument('--test', help='run the test function', action="store_true")
	args = parser.parse_args()
	if args.test: 
		test()
		sys.exit()
	col = args.col - 1
	all_gene = {}
	for file in args.input:
		with open(file) as f: all_gene[file] = [l.strip().split('\t')[col] for l in f]
	if args.head:
		for file in all_gene: del all_gene[file][0]
	if args.mode == 1:
		overlop_gene(all_gene)
	elif args.mode == 2:
		overlop_gene_2(all_gene)

