#!/home/shileisheng/anaconda3/bin/python
import re
import sys
import os


if __name__ == "__main__":
	head = ["filename", "total_reads", "bbdukf_filter", "bbdukf_filter_ratio", "flash_combined", "flash_uncombined", "flash_combined_ratio", "TrimmomaticPE_p", "TrimmomaticPE_1s", "TrimmomaticPE_2s", "TrimmomaticPE_filter", "bmtagger_s_filter", "bmtagger_p_filter", "sh.bm", "ph.bm", "clean_reads"]
	print('\t'.join(head))
	for fname in sys.argv[1:]:
		dir = os.popen('dirname '+fname).readline().split()[0]
		with open(fname) as f:
			rel = [fname.split('/')[-2] ]
			total_reads, bbdukf_filter, bbdukf_filter_ratio, flash_combined, flash_uncombined, flash_combined_ratio = 'NA','NA','NA','NA','NA','NA'
			for l in f:
				#BBDukF
				m = re.match(r'Input:\s+([0-9]+) reads', l)
				if m: total_reads = int(m.group(1))/2 #total reads
				m = re.match(r'Total Removed:\s+([0-9]+) reads\s+[(](.*?)[)]', l)
				if m: bbdukf_filter = int(m.group(1))/2  #BBDukF Total Removed and ratio
				if m: bbdukf_filter_ratio = m.group(2)
				#FLASH
				m = re.match(r"\[FLASH\]\s+Combined pairs:\s+([0-9]+)", l)
				if m: flash_combined = m.group(1) 
				m = re.match(r"\[FLASH\]\s+Uncombined pairs:\s+([0-9]+)", l)
				if m: flash_uncombined = m.group(1) 
				m = re.match(r"\[FLASH\]\s+Percent combined:\s+(.*)", l)
				if m: flash_combined_ratio = m.group(1) 
				#TrimmomaticPE
				match = re.match(r"Input Read Pairs:\s+[0-9]+\s+Both Surviving: ([0-9]+).*Forward Only Surviving: ([0-9]+).*Reverse Only Surviving: ([0-9]+).*Dropped: ([0-9]+)", l, re.I)
				if match: TrimmomaticPE_p, TrimmomaticPE_1s, TrimmomaticPE_2s, TrimmomaticPE_filter = match.group(1), match.group(2), match.group(3), match.group(4) 
		rel.extend( [total_reads, bbdukf_filter, bbdukf_filter_ratio, flash_combined, flash_uncombined, flash_combined_ratio, TrimmomaticPE_p, TrimmomaticPE_1s, TrimmomaticPE_2s, TrimmomaticPE_filter] )
		#bmtagger
		s_bmtagger, p_bmtagger = dir+'/s_bmtagger.out', dir+'/p_bmtagger.out'
		s_filter_out = os.popen('wc -l '+s_bmtagger).readline().split()[0]
		p_filter_out = os.popen('wc -l '+p_bmtagger).readline().split()[0]
		rel.extend( [s_filter_out, p_filter_out] )
		#final reads
		sh, ph = dir+'/sh.bm', dir+'/ph.bm'
		sh_count = int( os.popen('wc -l '+sh).readline().split()[0] ) / 4
		ph_count = int( os.popen('wc -l '+ph).readline().split()[0] ) / 8
		rel.extend( [sh_count , ph_count] )
		rel.append( sh_count+ph_count )
		print('\t'.join(map(str, rel)))
