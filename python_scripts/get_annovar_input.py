import sys
from collections import defaultdict

def merge_region(content):
	hits = defaultdict( set )
	# add the range 
	for l in content:
		chromo = l[0]
		feature_range = range(int(l[3]), int(l[4])+1)
		if feature_range:
			# keep track of unique hit positions in this protein
			hits[chromo].update(feature_range)
	return hits

if __name__=="__main__":
	fasta, gtf = sys.argv[1], sys.argv[2] #fasta file and gtf file
	with open(fasta) as f: seq = [l.strip() for l in f]
	seq_name = seq.pop(0).split()
	chr = seq_name[0][1:]
	sequence = ''.join(seq) #the fasta seq
	del seq
	with open(gtf, ) as f:temp = [l.strip().split('\t') for l in f]
	content = list(filter(lambda x:x[0] == chr, temp))
	del temp
	hits = merge_region(content) #merge regions
	#start to generate annovar input format file
	for pos in sorted(hits[chr]):
		ref_base = sequence[pos-1].upper()
		base =  list(set(['A','T','C','G']).difference(set(ref_base)))
		for alt_base in base:
			rel = [chr, str(pos), str(pos), ref_base, alt_base]
			print('\t'.join(rel))
			
