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
	total = [0]
	for idx, l in enumerate(lst): #total reads
		m = re.match(r'total reads:\s+([0-9]+)', l)
		if m:
			total_reads = int(m.group(1))
			total.append(total_reads)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #Duplication rate
		m = re.match(r'Duplication rate: (.*)', l)
		if m:
			duplication_rate = m.group(1)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): # Insert size peak
		m = re.match(r'Insert size peak \(evaluated by paired-end reads\): (.*)', l)
		if m:
			insert_size_peak = m.group(1)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): # merged reads
		m = re.match(r'Read pairs merged: ([0-9]+)', l)
		if m:
			merged_reads = int(m.group(1))
			merged_reads_ratio = lst[idx+1].split(':')[1].strip()
			del lst[:idx]
			break
	for idx, l in enumerate(lst): # clean_reads
		m = re.match(r'([0-9]+) paired reads -pair-, ([0-9]+) single reads', l)
		if m:
			p_clean = int(m.group(1))
			s_clean = int(m.group(2))
			break
	total_reads = max(total)
	clean_reads = p_clean + s_clean
	##human
	s_bmtagger, p_bmtagger  = dir+'/s_bmtagger.out', dir+'/p_bmtagger.out'
	bmtagger_s = int(os.popen('wc -l '+s_bmtagger).readline().split()[0])
	bmtagger_p = int(os.popen('wc -l '+p_bmtagger).readline().split()[0])
	#sortmerna
	s_sortmerna, p_sortmerna = dir+'/shr.log', dir+'/phr.log'
	with open(s_sortmerna) as f: lst = [l.strip() for l in f]
	for  l in lst: #total reads
		m = re.match(r'Total reads = ([0-9]+)', l)
		if m:
			s_sortmerna_in = int(m.group(1))
			sortmerna_s = s_sortmerna_in - s_clean
			break
	with open(p_sortmerna) as f: lst = [l.strip() for l in f]
	for  l in lst: #total reads
		m = re.match(r'Total reads = ([0-9]+)', l )
		if m:
			p_sortmerna_in = int(m.group(1)) / 2
			sortmerna_p = p_sortmerna_in - p_clean
			break
	#s_high_quality and p_high_quality
	s_high_quality, p_high_quality = bmtagger_s + s_sortmerna_in, bmtagger_p + p_sortmerna_in
	low_quality = total_reads - p_high_quality - s_high_quality
	#add into rel
	rel.extend( [total_reads, low_quality, duplication_rate, insert_size_peak, merged_reads, merged_reads_ratio, bmtagger_s, bmtagger_p, sortmerna_s, sortmerna_p, s_clean, p_clean, clean_reads] )
	return rel


if __name__ == "__main__":
	head = ["Sample", "total_reads", "low_quality", "duplication_rate", "insert_size_peak", "merged_reads", "merged_reads_ratio", "bmtagger_s", "bmtagger_p", "sortmerna_s", "sortmerna_p", "shnr.bm", "phnr.bm", "clean_reads"]
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

