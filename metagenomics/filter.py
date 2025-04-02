#!/home/shileisheng/anaconda3/bin/python
import argparse
#this is a test change

if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for extract info from taxonomy file')
	parser.add_argument('file', help='one file inlcude taxid column', type=str)
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--taxid', help='extract result which taxpath include the specified taxid(s)', type=str, nargs="+")
	taxid_group.add_argument('--taxid_f', help='extract result which taxpath include the specified taxid(s) in the file, one line one taxid', type=str)
	parser.add_argument('--taxonomy', help='reference taxonomy info, default is /home/shileisheng/reference/taxonomy.tbl', type=str, default='/home/shileisheng/reference/taxonomy.tbl')
	parser.add_argument('--rank', help='extract specified taxonomy level result', type=str, nargs="+")
	parser.add_argument("--taxid_col",help="taxid column number,default is 1 ", type=int, default=1)
	parser.add_argument('--head', help='whether ouput file header?', action="store_true")
	args = parser.parse_args()
	file = args.file
	target_rank = args.rank
	taxid_col = args.taxid_col - 1 
	#print(args)
	#read the taxonomy info
	with open(args.taxonomy) as f: taxonomy = [l.strip().split('\t') for l in f]
	taxid_rank = {l[0]:l[1] for l in taxonomy}
	taxid_path = {l[0]:l[3] for l in taxonomy}
	#read file content
	with open(file) as f: content = [l.strip().split('\t') for l in f]
	if args.head:
		print('\t'.join(content[0]))
		del content[0]
	if args.taxid:
		target_taxid = args.taxid
	else:
		with open(args.taxid_f) as f: target_taxid = [l.strip() for l in f]
	for l in content:
		if not taxid_rank.get(l[taxid_col]): continue
		if target_rank:
			if taxid_rank[l[taxid_col]] in target_rank and set(target_taxid).intersection(set(taxid_path[l[taxid_col]].split(':'))): print('\t'.join(l))
		else:
			if set(target_taxid).intersection(set(taxid_path[l[taxid_col]].split(':'))): print('\t'.join(l))
