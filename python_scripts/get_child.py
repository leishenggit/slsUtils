#!/usr/bin/env python
import argparse


def get_child_taxid(taxid, taxonomy):
    child_taxids = []
    for l in taxonomy:
        if taxid in l[3].split(':')[:-1]:
            child_idx = l[3].split(':').index(taxid)
            child_taxids.extend(l[3].split(':')[child_idx+1:])
    return set(child_taxids)


if __name__ == "__main__":
    #paras set 
    parser = argparse.ArgumentParser(description = 'A program for extract all chuild taxid for specified taxid ids')
    taxid_group = parser.add_mutually_exclusive_group(required=True)
    taxid_group.add_argument('--taxid_f', help='one file contain taxid, one line one taxid', type=str)
    taxid_group.add_argument('--taxid', help='one or more taxids', type=str, nargs='+')
    parser.add_argument('--taxonomy_f', help='taxonomy table file, /home/shileisheng/reference/taxonomy.tbl', type=str, default='/home/shileisheng/reference/taxonomy.tbl')
    parser.add_argument('--rank', help='extract specified taxonomy level result', type=str, nargs="+")
    args = parser.parse_args()
    #read the taxonomy info
    with open(args.taxonomy_f) as f: taxonomy = [l.strip().split('\t') for l in f]
    taxid_rank = {l[0]:l[1] for l in taxonomy}
    taxid_name = {l[0]:l[2] for l in taxonomy}
    taxid_path = {l[0]:l[3] for l in taxonomy}
    #read the target taxid
    if args.taxid_f:
        with open(args.taxid_f) as f: taxids = [l.strip() for l in f]
    else:
        taxids = args.taxid
    #start compute result
    for taxid in taxids:
        child_taxids = get_child_taxid(taxid, taxonomy) #extract all taxid below specific taxid
        for i in child_taxids: 
            if args.rank:
                if taxid_rank[i] in args.rank:
                    l = [taxid, taxid_rank[taxid], taxid_name[taxid], i, taxid_rank[i], taxid_name[i], taxid_path[i]]
                    print('\t'.join(l))
            else:
                l = [taxid, taxid_rank[taxid], taxid_name[taxid], i, taxid_rank[i], taxid_name[i], taxid_path[i]]
                print('\t'.join(l))

