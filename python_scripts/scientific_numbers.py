#!/home/shileisheng/anaconda3/bin/python
import argparse
import gzip


def as_num(x):
	try:
		y = float(x)
	except:
		y = 0.8
	z = '{:.12f}'.format(y)
	return(z)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A program for converting scientific counting strings to numbers')
	parser.add_argument('--input', help='one file including scientific counting strings', type=str, required=True)
	parser.add_argument('--cols', help='cols do not need converting, default is [1]', type=int, nargs="+", default=[1])
	parser.add_argument('--sep', help='seperator of fields, default is tab', type=str, choices=[' ',';',',','\t'], default='\t')
	parser.add_argument('--gzip',  help='whether input file is gziped ?', action="store_true")
	parser.add_argument('--head',  help='whether input file have header ?', action="store_true")
	args = parser.parse_args()
	#print(args)
	input_file = args.input
	cols = [i-1 for i in args.cols]
	if args.gzip:
		with gzip.open(input_file, "rt") as f:
			lst = [line.strip().split(args.sep) for line in f]
	else:
		with open(input_file) as f:
			lst = [line.strip().split(args.sep) for line in f]
	if args.head:
		print('\t'.join(lst[0]))
		del lst[0]
	for line in lst:
		val = [line[i] if i in cols else as_num(line[i]) for i in range(len(line))]
		print(args.sep.join(list(map(str, val))))

