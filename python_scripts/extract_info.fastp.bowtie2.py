#!/software/biosoft/software/python/python3/bin/python
import re
import sys
import os
from multiprocessing import Pool

def get_info(fname):
	dir = os.popen('dirname '+fname).readline().split()[0]
	rel = [dir.split('/')[-1]]
	with open(fname) as f: lst = [l.strip() for l in f]
	#start
	total_reads_lst = [0]
	total_bases_lst = [0]
	for idx, l in enumerate(lst): #total reads
		m = re.match(r'total reads:\s+([0-9]+)', l)
		if m:
			reads = int(m.group(1))
			total_reads_lst.append(reads)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #total bases
		m = re.match(r'total bases:\s+([0-9]+)', l)
		if m:
			bases = int(m.group(1))
			total_bases_lst.append(bases)
			del lst[:idx]
			break
	for idx, l in enumerate(lst):
		m = re.match(r'([0-9]+) (.*?) were paired; of these:', l)
		if m:
			p_high_quality = int(m.group(1))
			del lst[:idx]
			break
	for idx, l in enumerate(lst):
		m = re.match(r'([0-9]+) (.*?) were unpaired; of these:', l)
		if m:
			s_high_quality = int(m.group(1))
			del lst[:idx]
			break
	for idx, l in enumerate(lst):
		m = re.match(r'([0-9]+) paired reads -pair-, ([0-9]+) single reads', l)
		if m:
			p_clean = int(m.group(1))
			s_clean = int(m.group(2))
			break
	total_reads = max(total_reads_lst)
	total_bases = max(total_bases_lst)
	low_quality = total_reads - p_high_quality - s_high_quality
	clean_reads = p_clean + s_clean
	##human
	s_sortmerna, p_sortmerna = dir+'/shr.log', dir+'/phr.log'
	with open(s_sortmerna) as f: lst = [l.strip() for l in f]
	for  l in lst: #total reads
		m = re.match(r'Total reads = ([0-9]+)', l)
		if m:s_sortmerna_in = int(m.group(1))
	with open(p_sortmerna) as f: lst = [l.strip() for l in f]
	for  l in lst: #total reads
		m = re.match(r'Total reads = ([0-9]+)', l )
		if m:p_sortmerna_in = int(m.group(1)) / 2
	human_s, human_p = s_high_quality - s_sortmerna_in, p_high_quality - p_sortmerna_in
	#sortmerna
	sortmerna_s, sortmerna_p = s_high_quality - human_s - s_clean, p_high_quality - human_p - p_clean
	#add into rel
	rel.extend( [total_bases, total_reads, low_quality, human_s, human_p, sortmerna_s, sortmerna_p, s_clean, p_clean, clean_reads] )
	return rel


if __name__ == "__main__":
	head = ["Sample","total_bases", "total_reads", "low_quality", "human_s", "human_p", "sortmerna_s", "sortmerna_p", "shnr.bm", "phnr.bm", "clean_reads"]
	print('\t'.join(head))
	#multiprocessing
	p = Pool(processes=30)
	multi_res = [p.apply_async(get_info, args = (f,)) for f in sys.argv[1:] ]
	p.close()
	p.join()
	#output
	for res in multi_res:
		rel = res.get()
		print('\t'.join(map(str, rel)))

