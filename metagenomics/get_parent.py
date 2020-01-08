#!/home/shileisheng/anaconda3/bin/python
import argparse


if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for extract all parent taxid for specified taxid ids')
	parser.add_argument('--taxonomy_f', help='taxonomy table file, default is /home/shileisheng/reference/taxonomy.tbl', type=str, default='/home/shileisheng/reference/taxonomy.tbl')
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--taxid', help='extract result which taxpath include the specified taxid(s)', type=str, nargs="+")
	taxid_group.add_argument('--taxid_f', help='extract result which taxpath include the specified taxid(s) in the file, one line one taxid', type=str)
	parser.add_argument('--rank', help='extract specified taxonomy level result', type=str, nargs="+")
	args = parser.parse_args()

	#print(args)
	with open(args.taxonomy_f) as f:content = [l.strip().split('\t') for l in f]
	taxid_rank = {l[0]:l[1] for l in content}
	taxid_name = {l[0]:l[2] for l in content}
	taxid_path = {l[0]:l[3] for l in content}
	#get target taxid
	if args.taxid:
		target_taxid = args.taxid
	else:
		with open(args.taxid_f) as f: target_taxid = [l.strip() for l in f]
	#start compute result
	for taxid in target_taxid:
		up_taxids = taxid_path[taxid].split(':')[:-1]
		if args.rank: 
			ranked_up_taxid = [i for i in up_taxids if taxid_rank[i] in args.rank]
		else:
			ranked_up_taxid = up_taxids
		if len(ranked_up_taxid) == 0 : print("warning:", taxid, "has no parent at specified rank")
		for i in ranked_up_taxid:
			l = [taxid, taxid_rank[taxid], taxid_name[taxid], i, taxid_rank[i], taxid_name[i]]
			print('\t'.join(l))
