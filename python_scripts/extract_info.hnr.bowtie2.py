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
	total_reads, bbdukf_filter, bbdukf_filter_ratio, flash_combined, flash_uncombined, flash_combined_ratio,TrimmomaticPE_p, TrimmomaticPE_1s, TrimmomaticPE_2s, TrimmomaticPE_filter = 'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'
	for idx, l in enumerate(lst): #total reads
		m = re.match(r'Input:\s+([0-9]+) reads', l)
		if m:
			total_reads = int(m.group(1))/2
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #BBDukF
		m = re.match(r'Total Removed:\s+([0-9]+) reads\s+[(](.*?)[)]', l) 
		if m:
			bbdukf_filter = int(m.group(1))/2  #BBDukF Total Removed and ratio
			bbdukf_filter_ratio = m.group(2)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #FLASH
		m = re.match(r"\[FLASH\]\s+Combined pairs:\s+([0-9]+)", l) 
		if m:
			flash_combined = int(m.group(1))
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #FLASH
		m = re.match(r"\[FLASH\]\s+Uncombined pairs:\s+([0-9]+)", l)
		if m:
			flash_uncombined = m.group(1)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #FLASH
		m = re.match(r"\[FLASH\]\s+Percent combined:\s+(.*)", l)
		if m:
			flash_combined_ratio = m.group(1)
			del lst[:idx]
			break
	for idx, l in enumerate(lst): #TrimmomaticPE
		match = re.match(r"Input Read Pairs:\s+[0-9]+\s+Both Surviving: ([0-9]+).*Forward Only Surviving: ([0-9]+).*Reverse Only Surviving: ([0-9]+).*Dropped: ([0-9]+)", l, re.I)
		if match:
			TrimmomaticPE_p, TrimmomaticPE_1s, TrimmomaticPE_2s, TrimmomaticPE_filter = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
			break
	rel.extend([total_reads, bbdukf_filter, bbdukf_filter_ratio, flash_combined, flash_uncombined, flash_combined_ratio, TrimmomaticPE_p, TrimmomaticPE_1s, TrimmomaticPE_2s, TrimmomaticPE_filter])
	# bowtie2
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
	# clean_reads
	for idx, l in enumerate(lst): # clean_reads
		m = re.match(r'([0-9]+) paired reads -pair-, ([0-9]+) single reads', l)
		if m:
			p_clean = int(m.group(1))
			s_clean = int(m.group(2))
			break
	# sortmerna
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
	# human
	human_s, human_p = s_high_quality - s_sortmerna_in, p_high_quality - p_sortmerna_in
	#add into rel
	rel.extend( [human_s, human_p] )
	rel.extend( [sortmerna_s, sortmerna_p] )
	rel.extend( [s_clean , p_clean] )
	rel.append( s_clean + p_clean )
	return rel


if __name__ == "__main__":
	head = ["Sample", "total_reads", "bbdukf_filter", "bbdukf_filter_ratio", "flash_combined", "flash_uncombined", "flash_combined_ratio", "TrimmomaticPE_p", "TrimmomaticPE_1s", "TrimmomaticPE_2s", "TrimmomaticPE_filter", "bmtagger_s_filter", "bmtagger_p_filter", "sortmerna_s_filter", "sortmerna_p_filter", "shnr.bm", "phnr.bm", "clean_reads"]
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

