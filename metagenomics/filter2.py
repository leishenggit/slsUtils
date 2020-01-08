#!/home/shileisheng/anaconda3/bin/python
import argparse

def get_up_taxid(target_taxid, taxid_path):
	up_taxids = []
	for taxid in target_taxid:
		up_taxids.extend(taxid_path[taxid].split(':')[:-1])
	return set(up_taxids)

if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for extract info from taxonomy file')
	parser.add_argument('tax_file', help='one taxonomy files like as /home/shileisheng/reference/taxonomy.tbl', type=str)
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--taxid', help='extract result which taxpath include the specified taxid(s)', type=str, nargs="+")
	taxid_group.add_argument('--taxid_f', help='extract result which taxpath include the specified taxid(s) in the file, one line one taxid', type=str)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--up', help='extract upper level of specified taxid(s) result', action="store_true")
	group.add_argument('--low', help='extract lower level of specified taxid(s) result', action="store_true")
	parser.add_argument('--head', help='whether print the header', action="store_true")
	parser.add_argument("--taxid_col",help="taxid column number,default is 1 ", type=int, default=1)
	parser.add_argument('--rank', help='extract specified taxonomy level result', type=str, nargs="+")
	args = parser.parse_args()
	tbl_file = args.tax_file
	target_rank = args.rank
	taxid_col = args.taxid_col - 1 
	#print(args)
	#read the taxonomy info
	with open('/home/shileisheng/reference/taxonomy.tbl') as f: content = [l.strip().split('\t') for l in f]
	taxid_rank = {l[0]:l[1] for l in content}
	taxid_name = {l[0]:l[2] for l in content}
	taxid_path = {l[0]:l[3] for l in content}
	#read content
	with open(tbl_file) as f: content = [l.strip().split('\t') for l in f]
	if args.head: print('\t'.join(content[0]))
	#read the target taxid
	if args.taxid:
		target_taxid = args.taxid
	else:
		with open(args.taxid_f) as f: target_taxid = [l.strip() for l in f]
	#start to get wanted taxid info
	if args.up:
		up_taxids = get_up_taxid(target_taxid, taxid_path)
		if target_rank:
			for l in content:
				if taxid_rank[l[taxid_col]] in target_rank and l[taxid_col] in up_taxids: print('\t'.join(l))
		else:
			for l in content:
				l[taxid_col] in up_taxids: print('\t'.join(l))
	else:
		if target_rank:
			for l in content:
				if taxid_rank[l[taxid_col]] in target_rank and set(target_taxid).intersection(set( taxid_path[l[taxid_col]].split(':')[:-1] )): print('\t'.join(l))
		else:
			for l in content:
				if set(target_taxid).intersection(set( taxid_path[l[taxid_col]].split(':')[:-1] )): print('\t'.join(l))
