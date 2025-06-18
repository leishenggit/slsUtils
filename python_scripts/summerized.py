#!/home/shileisheng/anaconda3/bin/python
import argparse


def summarized(rec, lst, taxid_col, count_col, taxid_path):
	read_count = 0
	#print('\t'.join(rec))
	target_taxid = rec[taxid_col]
	for l in lst:
		path = taxid_path[l[taxid_col]].split(':')
		if target_taxid in path:
			read_count += float(l[count_col])
	rec[count_col] = str(read_count)
	print('\t'.join(rec))


def fill_path(taxid_col, taxid_path, content):
	all_taxid = list(set([l[taxid_col] for l in content]))
	all_taxid_1 = list(all_taxid)
	for taxid in all_taxid:
		up_taxids = taxid_path[taxid].split(':')[:-1]
		for id in up_taxids:
			if id not in all_taxid_1:
				rec = [id, '0']
				content.append(rec)
				all_taxid_1.append(id)

if __name__ == "__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for turning assigned taxid_reads file to summarized taxid_reads file')
	parser.add_argument('file', help='one file inlcude taxid column and assigned reads count column', type=str)
	parser.add_argument("--taxid_col",help="taxid column number,default is 1", type=int, default=1)
	parser.add_argument("--count_col",help="read_count column number,default is 2", type=int, default=2)
	parser.add_argument('--head', help='whether input file has header?', action="store_true")
	args = parser.parse_args()
	file = args.file
	taxid_col = args.taxid_col - 1
	count_col = args.count_col - 1
	#print(args)
	#read the taxonomy info
	with open('/home/shileisheng/reference/taxonomy.tbl') as f: taxonomy = [l.strip().split('\t') for l in f]
	taxid_path = {l[0]:l[3] for l in taxonomy}
	#read file content
	with open(file) as f: content = [l.strip().split('\t') for l in f]
	if args.head:
		print('\t'.join(content[0]))
		del content[0]
	#process non tree info records
	na_tax = []
	for l in content:
		if not taxid_path.get(l[taxid_col]):
			print('\t'.join(l))
			na_tax.append(l)
	content_1 = [l for l in content if l not in na_tax]
	del content
	#fill path when parent nodes of some taxids not show in the file
	fill_path(taxid_col, taxid_path, content_1)
	#finally output
	for l in content_1:
		rec = list(l)
		summarized(rec, content_1, taxid_col, count_col, taxid_path)

