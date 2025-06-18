#!/home/shileisheng/anaconda3/bin/python
from multiprocessing import Pool
import sys
import gzip

def out(fastq):
	if fastq[-3:] == ".gz": 
		with gzip.open(fastq, 'rt') as f: content = [l.strip() for l in f]
	else:
		with open(fastq) as f: content = [l.strip() for l in f]
	ref = open(fastq + '.concatenate', 'w')
	for i in range(0,len(content),8):
		r1 = content[i:i+4]
		r2 = content[i+4:i+8]
		seq = 'NNNNNN'.join([r1[1], r2[1]])
		r1[1] = seq
		for l in r1: ref.write(l+'\n')
	ref.close()


if __name__ == "__main__":
	#multiprocessing
	p = Pool(processes=10)
	for f in sys.argv[1:]:
		p.apply_async(out, args = (f,))
	p.close()
	p.join()
