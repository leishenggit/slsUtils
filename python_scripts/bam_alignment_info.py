#!/home/shileisheng/anaconda3/bin/python
import argparse
import pysam


def open_file(inputFile):
	if inputFile[-3:] == 'bam':
		bf = pysam.AlignmentFile(inputFile, 'rb')
		return bf
	elif inputFile[-3:] == 'sam':
		bf = pysam.AlignmentFile(inputFile, 'r')
		return bf
	else:
		print('Only SAM and BAM file are expected.')
		print('----------------------------------------')
		parser.print_help()
		exit()


def test(inputFile):
	bf = open_file(inputFile)
	#print(bf.check_index()) #return True if index is present.
	#print(bf.find_introns(bf.fetch("MT", 10, 200)))
	#print(bf.count('MT', 200,300)) #count the number of reads in region
	##count the coverage of genomic positions by reads in region. return four array.arrays of the same length in order A C G T
	#for i in bf.count_coverage('MT', 200,300): print(i,len(i))
	#for x in bf.fetch("MT", 10, 20): print(str(x))  #fetch reads aligned in a region. return an iterator over a collection of reads.
	r = bf.__next__()
	cigar = r.get_cigar_stats()
	print(cigar)
	print(cigar[0][0], cigar[0][1], cigar[0][2], cigar[0][7], cigar[0][8])
	#print('Number of attrs:', len(dir(r)))
	#for attr in dir(r): print(attr, getattr(r, attr, 'None'), sep='\n')


def align_detail(inputFile, length, primary=False):
	bf = open_file(inputFile)
	print('\t'.join(['read_name', 'read_length', 'query_length', 'query_alignment_length', 'query_alignment_start', 'query_alignment_end', 'reference_name', 'target_length', 'target_start','target_end', 'aligned', 'insert', 'deletion', 'equal', 'diff', 'is_duplicate', 'is_secondary', 'is_supplementary', 'mapping_quality']))
	for r in bf: 
		if r.is_unmapped: continue
		if r.query_alignment_length < length: continue
		if primary:
			if r.is_secondary==True or r.is_supplementary==True: continue
		cigar = r.get_cigar_stats()
		print(r.query_name, r.infer_read_length(), r.infer_query_length(), r.query_alignment_length, r.query_alignment_start, r.query_alignment_end, r.reference_name, r.reference_length, r.reference_start, r.reference_end, cigar[0][0], cigar[0][1], cigar[0][2], cigar[0][7], cigar[0][8], r.is_duplicate, r.is_secondary, r.is_supplementary, r.mapping_quality, sep='\t')
	bf.close()


def mapping_stat(inputFile):
	bf = open_file(inputFile)
	head = ['map', 'unmap', 'map_ratio']
	print('\t'.join(head))
	map, unmap = [], []
	for r in bf:
		if not r.is_unmapped:
			map.append(r.query_name)
		else:
			unmap.append(r.query_name)
	a, b = len(set(map)), len(set(unmap))
	print(a, b, a/(a+b))




if __name__=="__main__":
	parser = argparse.ArgumentParser(description = 'A program for extracting alignment related value')
	parser.add_argument('input', help='input file. support format including "SAM" and "BAM"', type=str)
	parser.add_argument('-t', '--test', help='run test function', action="store_true")
	parser.add_argument('-m', '--mapping', help='get mapping ratio', action="store_true")
	parser.add_argument('-l', '--alignment_len', help='consider read that query_alignment_length greater than this number', type=int, default=0)
	parser.add_argument('--primary', help='consider read that is primary aligned', action="store_true")
	args = parser.parse_args()
	#print(vars(args))
	try:
		if args.test: 
			test(args.input)
		elif args.mapping: 
			mapping_stat(args.input)
		else:
			align_detail(args.input, args.alignment_len, args.primary)
	except:
		parser.print_help()
		exit()





