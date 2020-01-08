#!/home/shileisheng/anaconda3/bin/python
from Bio import SeqIO
from collections import defaultdict
import argparse

if __name__ == '__main__':
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for split single-end reads and paired-end reads into 2 file from a fastq file')
	parser.add_argument('--input', help='one fasta or fastq file', type=str, required=True)
	parser.add_argument('--out_s', help='output file of single-end reads', type=str, required=True)
	parser.add_argument('--out_p', help='output file of paired-end reads', type=str, required=True)
	args = parser.parse_args()
	#print(args)
	input_file = args.input
	output_s = args.out_s
	output_p = args.out_p
	output = {1:output_s, 2:output_p}
	read_count = defaultdict(lambda : 0)
	for r in SeqIO.parse(input_file, 'fastq'): read_count[r.id] += 1
	single = (r for r in SeqIO.parse(input_file, 'fastq') if read_count[r.id] == 1 )
	count = SeqIO.write(single, output_s, "fastq")
	print("Saved %i records from %s to %s" % (count, input_file, output_s) )
	paired = (r for r in SeqIO.parse(input_file, 'fastq') if read_count[r.id] == 2 )
	count = SeqIO.write(paired, output_p, "fastq")
	print("Saved %i records from %s to %s" % (count, input_file, output_p) )
