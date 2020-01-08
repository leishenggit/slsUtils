#!/home/shileisheng/anaconda3/bin/python
import argparse

def check_rank(taxid, high_rank_taxid, taxid_path):
	up_taxids = taxid_path[taxid].split(':')[:-1]
	for taxid in  up_taxids:
		if taxid in high_rank_taxid: return True
	return False

if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for fix rank problem in a taxonomy file')
	parser.add_argument('--low_rank', help='A specified rank file like as /home/shileisheng/cvg/taxonomy_raw/tax.last.samples.Comparison-ex.txt', type=str, required=True)
	parser.add_argument('--high_rank', help='A specified rank file like as /home/shileisheng/cvg/taxonomy_raw/tax.last.samples.Comparison-ex.txt, but rank is higher than first input file', type=str, required=True)
	args = parser.parse_args()
	low_rank_file = args.low_rank
	high_rank_file = args.high_rank
	#print(args)
	with open(low_rank_file) as f: content = [l.strip().split('\t') for l in f]
	del content[0]
	rel = {l[0]:l for l in content}
	low_rank_taxid = rel.keys()
	with open(high_rank_file) as f: content = [l.strip().split('\t') for l in f]
	high_rank_taxid = [l[0] for l in content[1:]]
	rank = content[1][1]
	for l in content: print('\t'.join(l))
	#refrence info 
	with open('/home/shileisheng/reference/taxonomy.tbl') as f: content = [l.strip().split('\t') for l in f]
	taxid_path = {l[0]:l[3] for l in content}
	del content
	#start check rank
	for taxid in low_rank_taxid:
		if not check_rank(taxid, high_rank_taxid, taxid_path):
			rel[taxid][1] = rank
			rel[taxid][2] = 'fake name'
			print('\t'.join(rel[taxid]))


