#!/home/shileisheng/anaconda3/bin/python
import argparse


def setArgs():
	parser = argparse.ArgumentParser(description="功能：根据两个文件中的关联列来抽取第一个文件中指定的行")
	parser.add_argument("file",help="数据文件 1")
	field_group = parser.add_mutually_exclusive_group(required=True)
	field_group.add_argument('--field', help='命令行指定需要抽取的关键词', type=str, nargs="+")
	field_group.add_argument('--field_f', help='文件指定需要抽取的关键词', type=str)
	parser.add_argument("--col1",help="关联列在文件 1 中的列序号，默认为 1 ", type=int, default=1)
	parser.add_argument("--col2",help="关联列在文件 2 中的列序号，默认为 1 ", type=int, default=1)
	parser.add_argument('--reverse', help='反向输出，输出指定关键词以外的数据', action="store_true")
	parser.add_argument('--head', help='数据文件 1 是否有文件头', action="store_true")
	return parser.parse_args()

if __name__ == "__main__":
	## 获得参数
	args = setArgs()
	idx1, idx2 = args.col1-1, args.col2-1
	try:
		if args.field:
			sample = args.field
		else:
			with open(args.field_f) as f: ids = [l.strip().split('\t')[idx2] for l in f]
			sample = list( set(ids) )
		with open(args.file) as f:
			if args.head: print(f.readline().strip())
			for line in f:
				l = line.strip().split('\t')
				if args.reverse:
					if l[idx1] not in sample: print('\t'.join(l))
				else:
					if l[idx1] in sample: print('\t'.join(l))
	except:
		exit()