#!/home/shileisheng/anaconda3/bin/python
import argparse

def get_level_name(taxid, rank, taxid_rank, taxid_name, taxid_path, name):
	res = 'NA'
	if taxid_path.get(taxid):
		for i in taxid_path[taxid].split(':'):
			if taxid_rank[i] == rank: res = taxid_name[i] if name else i
	return res


if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for assign level info for input taxid(s), output in the taxonomy order')
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--taxid', help='extract result which taxpath include the specified taxid(s)', type=str, nargs="+")
	taxid_group.add_argument('--taxid_f', help='extract result which taxpath include the specified taxid(s) in the file, one line one taxid', type=str)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--rank', help='assign specified taxonomy level result, eg.superkingdom kingdom phylum class order family genus species', type=str, nargs="+")
	group.add_argument('--all', help='assign all available taxonomy level result', action="store_true")
	parser.add_argument('--get_id', help='return taxid rather than taxname', action="store_true")
	parser.add_argument('--taxonomy_table', help='taxonomy info table. default is /home/shileisheng/reference/taxonomy.tbl', type=str, default='/home/shileisheng/reference/taxonomy.tbl')
	args = parser.parse_args()
	name = False if args.get_id else True 
	#print(args)
	if args.taxid:
		target_taxid = args.taxid
	else:
		with open(args.taxid_f) as f: target_taxid = [l.strip() for l in f]
	#reads meta info
	with open(args.taxonomy_table) as f: content = [l.strip().split('\t') for l in f]
	taxid_rank = {l[0]:l[1] for l in content}
	taxid_name = {l[0]:l[2] for l in content}
	taxid_path = {l[0]:l[3] for l in content}
	#get level name
	if args.all:
		for taxid in target_taxid:
			if taxid_path.get(taxid):
				name_detail = [taxid_name[i] for i in taxid_path[taxid].split(':')]
				rel = [taxid, '\t'.join(name_detail)]
				print('\t'.join(rel))
	else:
		head = ['taxid','tax_name','tax_rank']
		head.extend(list(args.rank))
		print('\t'.join(head))
		for taxid in target_taxid:
			level_name = [get_level_name(taxid, rank, taxid_rank, taxid_name, taxid_path, name) for rank in args.rank]
			tax_name = taxid_name.get(taxid, 'NA')
			tax_rank = taxid_rank.get(taxid, 'NA')
			print(taxid+'\t'+ tax_name+'\t'+tax_rank+'\t'+'\t'.join(level_name))


