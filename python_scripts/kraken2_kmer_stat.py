#!/home/shileisheng/anaconda3/bin/python
import argparse

if __name__ == '__main__':
	#paras set 
	parser = argparse.ArgumentParser(description = 'A program for compute matched k-mer for a reads')
	parser.add_argument('--input', help='kraken2 out file', type=str, required=True)
	parser.add_argument('--kmer_length', help='k-mer length for kraken2 database, default=35', type=int, default=35)
	args = parser.parse_args()
	#print(args)
	input_file = args.input
	kmer_length = args.kmer_length
	with open(input_file) as f: content = [l.strip().split('\t') for l in f]
	aligned = [l for l in content if l[0]=='C']
	del content
	head = ['read','k-mer_total', 'aligned_kmer','taxid']
	print('\t'.join(head))
	for l in aligned:
		kmer_stat = [i.split(':') for i in l[4].split()]
		aligned_kmer = sum([int(i[1]) for i in kmer_stat if i[0] != '0'])
		kmer_total = sum([int(i[1]) for i in kmer_stat])
		rel = [l[1], str(kmer_total), str(aligned_kmer), l[2]]
		print('\t'.join(rel))
		