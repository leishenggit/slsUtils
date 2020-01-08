#!/home/shileisheng/anaconda3/bin/python
import argparse
from Bio import SeqIO

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A program for get reads length from fasta or fastq file')
	parser.add_argument('--input', help='one fasta or fastq file', type=str, required=True)
	parser.add_argument('--format', help='file format of the input file, default=fastq', type=str,default='fastq')
	args = parser.parse_args()
	#print(args)
	input_file = args.input
	input_format = args.format
	for rec in SeqIO.parse(input_file, input_format):
		print(rec.id, len(rec),sep='\t')
