#!/home/shileisheng/anaconda3/bin/python
from Bio import SeqIO
import argparse

if __name__ == '__main__':
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for extract reads from fasta or fastq file')
	parser.add_argument('--input', help='one fasta or fastq file', type=str, required=True)
	field_group = parser.add_mutually_exclusive_group(required=True)
	field_group.add_argument('--id', help='specifying read ID on the command line', type=str, nargs="+")
	field_group.add_argument('--id_f', help='specifying read ID in a file, one id one line', type=str)
	parser.add_argument('--out', help='output file', type=str, required=True)
	parser.add_argument('--format', help='file format of the input file, default=fastq', type=str,default='fastq')
	parser.add_argument('--reverse', help='filter out the reads in id file', action="store_true")
	args = parser.parse_args()
	#print(args)
	input_file = args.input
	output_file = args.out
	input_format = args.format
	if args.id_f:
		wanted = set(line.strip().split('\t')[0] for line in open(id_file))
		print("Found %i unique identifiers in %s" % (len(wanted), id_file))
	else:
		wanted = set(args.id)
		print("Found %i unique identifiers" % len(wanted))
	if args.reverse:
		records = (r for r in SeqIO.parse(input_file, input_format) if r.id not in wanted)
		count = SeqIO.write(records, output_file, "fastq")
		print("Saved %i records from %s to %s" % (count, input_file, output_file) )
	else:
		records = (r for r in SeqIO.parse(input_file, input_format) if r.id in wanted)
		count = SeqIO.write(records, output_file, "fastq")
		print("Saved %i records from %s to %s" % (count, input_file, output_file) )
		if count < len(wanted):
			print("Warning %i IDs not found in %s" % (len(wanted)-count, input_file))