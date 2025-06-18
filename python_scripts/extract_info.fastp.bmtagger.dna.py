#!/software/biosoft/software/python/python3/bin/python
import re
import argparse
import os
from multiprocessing import Pool

def get_info(fname):
	dir = os.popen('dirname '+fname).readline().split()[0]
	rel = [dir.split('/')[-1]]
	with open(fname) as f: lst = [l.strip() for l in f]
	try:
		for idx, l in enumerate(lst): # clean_reads
			m = re.match(r'([0-9]+) paired reads -pair-, ([0-9]+) single reads', l)
			if m:
				p_clean = int(m.group(1))
				s_clean = int(m.group(2))
				break
		#fastp info
		qc_info_f  = dir + '/' +dir.split('/')[-1] +'.e'
		if not os.path.exists(qc_info_f):
			print(qc_info_f,' is not exists')
			return []
		with open(qc_info_f) as f: lst = [l.strip() for l in f]
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
		total_reads = max(total)
		clean_reads = p_clean + s_clean
		##human
		s_bmtagger, p_bmtagger  = dir+'/s_bmtagger.out', dir+'/p_bmtagger.out'
		if not os.path.exists(s_bmtagger) or not os.path.exists(p_bmtagger):
			print(s_bmtagger,' is not exists')
			return []
		bmtagger_s = int(os.popen('wc -l '+s_bmtagger).readline().split()[0])
		bmtagger_p = int(os.popen('wc -l '+p_bmtagger).readline().split()[0])
		#s_high_quality and p_high_quality
		low_quality = total_reads - bmtagger_s - bmtagger_p - clean_reads
		#add into rel
		rel.extend( [total_reads, low_quality, duplication_rate, insert_size_peak, merged_reads, merged_reads_ratio, bmtagger_s, bmtagger_p, s_clean, p_clean, clean_reads] )
		return rel
	except:
		print(fname,"something is wrong:")
		return []


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A program for extract info from qc file')
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--log', help='qc file(s)', type=str, nargs="+")
	taxid_group.add_argument('--log_list_f', help='qc file path, one line one sample', type=str)
	parser.add_argument('--out', help='output file', type=str, required=True)
	args = parser.parse_args()
	#
	if args.log:
		log_fs = args.log
	else:
		with open(args.log_list_f) as f: log_fs = [l.strip() for l in f]
	#multiprocessing
	p = Pool(processes=30)
	multi_res = [p.apply_async(get_info, args = (f,)) for f in log_fs]
	p.close()
	p.join()
	#output
	head = ["Sample", "total_reads", "low_quality", "duplication_rate", "insert_size_peak", "merged_reads", "merged_reads_ratio", "bmtagger_s", "bmtagger_p", "shnr.bm", "phnr.bm", "clean_reads"]
	with open(args.out,'w') as ref:
		ref.write('\t'.join(head)+'\n')
		for res in multi_res:
			rel = res.get()
			if len(rel) > 1: ref.write('\t'.join(map(str, rel))+'\n')

