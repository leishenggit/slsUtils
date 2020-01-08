#!/home/shileisheng/anaconda3/bin/python
import argparse


## 设置命令行参数
def setArgs():
	parser = argparse.ArgumentParser(description="功能：根据列名来抽取文件中指定的列")
	parser.add_argument("file",help="数据文件")
	field_group = parser.add_mutually_exclusive_group(required=True)
	field_group.add_argument('--field', help='命令行指定需要抽取的列', type=str, nargs="+")
	field_group.add_argument('--field_f', help='文件指定需要抽取的列', type=str)
	parser.add_argument("--col",help="关键词在文件中的列序号，默认为 1 ", type=int, default=1)
	parser.add_argument('--number', help='指定的列是否按照数字来匹配，默认按照列的名称匹配', action="store_true")
	return parser.parse_args()

if __name__ == "__main__":
	## 获得参数
	args = setArgs()
	idx = args.col-1
	try:
		if args.field:
			sample = args.field
		else:
			with open(args.field_f) as f: sample = [l.strip().split('\t')[idx] for l in f]
		if args.number:
			cols = [int(i)-1 for i in sample]
		else:
			with open(args.file) as f: head = f.readline().strip().split('\t')
			cols= [i for k in sample for i,v in enumerate(head) if v==k]
		with open(args.file) as f:
			for line in f: 
				l = line.strip().split('\t')
				rel = [l[c] for c in cols]
				print('\t'.join(rel))
	except:
		exit()
