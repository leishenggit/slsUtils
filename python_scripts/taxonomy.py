#!/home/shileisheng/anaconda3/bin/python
import argparse

def get_level_name(taxid, rank, taxid_rank, taxid_name, taxid_path):
    res = 'NA'
    for i in taxid_path[taxid].split(':'): 
        if taxid_rank[i] == rank: res = taxid_name[i]
    return res

if __name__ == "__main__":
    #paras set 
    parser = argparse.ArgumentParser(description = 'A program for assign level info for input taxid(s), output in the taxonomy order')
    taxid_group = parser.add_mutually_exclusive_group(required=True)
    taxid_group.add_argument('--taxid', help='extract result which taxpath include the specified taxid(s)', type=str, nargs="+")
    taxid_group.add_argument('--taxid_f', help='extract result which taxpath include the specified taxid(s) in the file, one line one taxid', type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rank', help='assign specified taxonomy level result, eg.superkingdom kingdom phylum class order family genus species', type=str, nargs="+")
    group.add_argument('--all', help='assign all available taxonomy level result', action="store_true")
    args = parser.parse_args()
    #print(args)
    if args.taxid:
        target_taxid = args.taxid
    else:
        with open(args.taxid_f) as f: target_taxid = [l.strip() for l in f]
    #reads meta info
    with open('/home/shileisheng/reference/taxonomy.tbl') as f: content = [l.strip().split('\t') for l in f]
    taxid_rank = {l[0]:l[1] for l in content}
    taxid_name = {l[0]:l[2] for l in content}
    taxid_path = {l[0]:l[3] for l in content}
    #get level name
    if args.all:
        for taxid in target_taxid:
            name_detail = [taxid_name[i] for i in taxid_path[taxid].split(':')]
            rank_detail = [taxid_rank[i] for i in taxid_path[taxid].split(':')]
            rel = [taxid, '\t'.join(name_detail)]
            print('\t'.join(rel))
    else:
        head = list(args.rank)
        head.insert(0, '#TAXONOMY')
        print('\t'.join(head))
        for taxid in target_taxid:
            #for rank in args.rank: print(rank, get_level_name(taxid, rank, taxid_rank, taxid_name, taxid_path))
            level_name = [get_level_name(taxid, rank, taxid_rank, taxid_name, taxid_path) for rank in args.rank]
            print(taxid+'\t'+'\t'.join(level_name))
            


