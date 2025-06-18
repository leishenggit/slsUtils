#!/home/shileisheng/anaconda3/bin/python
import argparse
import pysam



def test(inputFile, outputFile, count_m):
    right = []
    bf_in = pysam.AlignmentFile(inputFile)
    for r in bf_in:
        cigar = r.get_cigar_stats()
        if cigar[0][0] <= count_m: right.append(r.query_name)
    reads_name = set(right)
    del right
    print("There are", len(reads_name), "paired-end/merged reads removed due to the Cigar threshold of (-m)", count_m, "from", inputFile)
    bf_in = pysam.AlignmentFile(inputFile)
    if inputFile[-3:] == 'bam':
        bf_out = pysam.AlignmentFile(outputFile, 'wb', template=bf_in)
    else:
        bf_out = pysam.AlignmentFile(outputFile, 'w', template=bf_in)
    for r in bf_in:
        if r.query_name in reads_name: continue
        bf_out.write(r)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = 'A program for filter alignment in BAM file')
    parser.add_argument('-i', '--input', help='input file.', type=str, required=True)
    parser.add_argument('-o', '--output', help='output file.', type=str, required=True)
    parser.add_argument('-m', '--count_m', help='cutoff for cigar M. default=0', type=int, default=0)
    args = parser.parse_args()
    try:
        test(args.input, args.output, args.count_m)
    except:
        parser.print_help()
        exit()
