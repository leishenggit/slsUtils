#!/software/biosoft/software/python/python3/bin/python
import re
import sys
import os
from multiprocessing import Pool

def get_info(fname):
	dir_s = os.popen('dirname '+fname).readline().split()[0]
	rel = [dir_s.split('/')[-1]]
	with open(fname) as f: lst = [l.strip() for l in f if l.strip() ]
	#start
	for idx, l in enumerate(lst): #total reads
		m = re.match(r'number of reads = ([0-9,]+)', l)
		if m:
			total_reads = m.group(1).replace(',', '')
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #number of mapped reads
		m = re.match(r'number of mapped reads = ([0-9,]+) [(](.*)[)]', l)
		if m:
			mapped_reads = m.group(1).replace(',', '')
			mapped_ratio = m.group(2)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #number of bases
		m = re.match(r'number of sequenced bases = ([0-9,]+)', l)
		if m:
			total_base = m.group(1).replace(',', '')
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #Duplication rate
		m = re.match(r'number of duplicated reads [(]flagged[)] = (.*)', l)
		if m:
			duplication_reads = m.group(1).replace(',', '')
			del lst[:idx]
			break
	#add into rel
	rel.extend( [total_reads, mapped_reads, mapped_ratio, total_base, duplication_reads] )
	return rel


if __name__ == "__main__":
	head = ["Sample", "clean_reads", "mapped_reads", "mapped_ratio", "clean_base", "duplication_reads"]
	print('\t'.join(head))
	#for f in sys.argv[1:]:
	#	rel = get_info(f)
	#	print('\t'.join(map(str, rel)))
	#sys.exit()
	#multiprocessing
	p = Pool(processes=30)
	multi_res = [p.apply_async(get_info, args = (f,)) for f in sys.argv[1:] ]
	p.close()
	p.join()
	#output
	for res in multi_res:
		rel = res.get()
		print('\t'.join(map(str, rel)))

