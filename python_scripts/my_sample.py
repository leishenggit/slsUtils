import time
from multiprocessing import Pool, Manager
import numpy as np
import argparse



def my_sample(sample_num, sample_cycle, replace, dat):
	with open(dat) as f : content = [line for line in f]
	idx = list(range(len(content)))
	total_reads = [content[i:i+4] for i in idx[::4]]#divide to 4 lines/reads
	total_reads_num = len(total_reads)
	for i in range(sample_cycle):
		print("random sample", sample_num, "from", total_reads_num, "for cycle ", i+1)
		ref = '_'.join([dat, str(sample_num), str(i+1)])
		f = open(ref, 'w')
		#print("open", ref, "success")
		sample = list(np.random.choice(range(total_reads_num), sample_num, replace=replace))
		for idx in sample: 
			for l in total_reads[idx]:
				f.write(l)
		f.close()


if __name__=="__main__":
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for random sample')
	parser.add_argument('input', nargs='+', help='one or more fastq file', type=str)
	parser.add_argument('--sample_cycle', help='sample how many times, default=10', type=int, default=10)
	parser.add_argument('--replace', help='wether put back sampling, default=False', type=bool, default=False)
	parser.add_argument('--sample_num', help='each times choose how many items, default=10000', type=int, default=1000)
	args = parser.parse_args()
	#print(args)
	#start time point
	start = time.time()
	#multiprocessing
	p = Pool()
	for dat in args.input:
		#for i in range(10): print(total_reads[i])
		p.apply_async(my_sample, args = (args.sample_num, args.sample_cycle, args.replace, dat))
	p.close()
	p.join()
	#get the programm's time use
	end = time.time()
	print("use time ",(end-start)/3600,"hour")
	