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
	# clean_reads
	for idx, l in enumerate(lst): # clean_reads
		m = re.match(r'([0-9]+) paired reads -pair-, ([0-9]+) single reads', l)
		if m:
			phnr_count = int(m.group(1))
			shnr_count = int(m.group(2))
			break
	#bmtagger
	s_bmtagger, p_bmtagger = dir+'/s_bmtagger.out', dir+'/p_bmtagger.out'
	s_filter_out = int(os.popen('wc -l '+s_bmtagger).readline().split()[0])
	p_filter_out = int(os.popen('wc -l '+p_bmtagger).readline().split()[0])
	rel.extend( [s_filter_out, p_filter_out] )
	#sortmerna
	s_sortmerna, p_sortmerna = TrimmomaticPE_1s + TrimmomaticPE_2s + flash_combined - shnr_count - s_filter_out, TrimmomaticPE_p - phnr_count - p_filter_out
	#add into rel
	rel.extend( [s_sortmerna, p_sortmerna] )
	rel.extend( [shnr_count , phnr_count] )
	rel.append( shnr_count+phnr_count )
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

